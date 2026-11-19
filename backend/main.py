from decimal import Decimal
from typing import Annotated

from db import SessionDep
from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from models import Bank, ImportResult, Transaction, User
from parsers import PARSERS, ParserError
from sqlmodel import select
from tables import BankRecord, ImportRecord, TransactionRecord, UserRecord

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

banks: list[Bank] = [Bank(val=val, label=bp.label) for val, bp in PARSERS.items()]


users: list[User] = [
    User(name="Sienna", accent="lime", income=Decimal(3000), expenses=Decimal(2000)),
    User(name="Nikita", accent="sky", income=Decimal(5000), expenses=Decimal(1000)),
]

imported_transactions: dict[int, list[Transaction]] = {}


@app.get("/users")
def list_users() -> list[User]:
    return users


@app.get("/banks")
def list_banks() -> list[Bank]:
    return banks


# @app.post("/users", status_code=201)
# def create_user(user: User) -> User:
#     users.append(user)
#     return user


@app.get("/imports/{import_id}/transactions")
def get_transactions_by_id(import_id: int) -> list[Transaction]:
    return imported_transactions.get(import_id, [])


@app.post("/imports", status_code=201)
def upload_csv(
    session: SessionDep,
    file: UploadFile,
    bank: Annotated[str, Form()],
    person: Annotated[str, Form()],
) -> ImportResult:
    db_bank = session.exec(select(BankRecord).where(BankRecord.code == bank)).first()
    if db_bank is None or db_bank.code not in PARSERS:
        raise HTTPException(status_code=400, detail=[f"Unknown Bank: {bank}"])

    db_user = session.exec(select(UserRecord).where(UserRecord.name == person)).first()
    if db_user is None:
        raise HTTPException(status_code=400, detail=[f"Unknown User: {person}"])

    if file.filename is None:
        raise HTTPException(status_code=400, detail=["Invalid File"])

    try:
        raw = file.file.read()
        decoded = raw.decode("utf-8-sig")
        transactions = PARSERS[bank].parse(
            decoded, person, 1
        )  # TODO placeholder, parsers drop import_id after 6c
    except ParserError as e:
        raise HTTPException(
            status_code=400, detail=e.errors if e.errors else [str(e)]
        ) from e
    except UnicodeDecodeError as e:
        raise HTTPException(status_code=400, detail=[str(e)]) from e

    num_need_category: int = sum(1 for t in transactions if t.category_id is None)
    import_record = ImportRecord(
        filename=file.filename, user_id=db_user.id, bank_id=db_bank.id
    )
    session.add(import_record)
    session.flush()
    import_record_id = import_record.id
    db_transactions = [
        TransactionRecord(
            transaction_date=t.transaction_date,
            import_id=import_record_id,
            merchant=t.merchant,
            amount=t.amount,
            bank_category=t.bank_category,
            ignore=t.ignore,
            category_id=None,  # TODO: replace with actual code once categorization is complete
        )
        for t in transactions
    ]
    session.add_all(db_transactions)
    session.commit()
    imported_transactions[import_record_id] = transactions
    return ImportResult(
        filename=file.filename,
        id=import_record_id,
        user=person,
        num_need_category=num_need_category,
        num_transactions=len(transactions),
    )
