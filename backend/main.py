from collections.abc import Sequence
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

users: list[User] = [
    User(name="Sienna", accent="lime", income=Decimal(3000), expenses=Decimal(2000)),
    User(name="Nikita", accent="sky", income=Decimal(5000), expenses=Decimal(1000)),
]


@app.get("/users")
def list_users() -> list[User]:
    return users


@app.get("/banks")
def list_banks(session: SessionDep) -> list[Bank]:
    bank_records = session.exec(select(BankRecord).order_by(BankRecord.id)).all()
    banks = [Bank.model_validate(rec) for rec in bank_records]
    return banks


# @app.post("/users", status_code=201)
# def create_user(user: User) -> User:
#     users.append(user)
#     return user


@app.get("/imports/{import_id}/transactions")
def get_transactions_by_id(import_id: int, session: SessionDep) -> list[Transaction]:
    import_record = session.get(ImportRecord, import_id)
    if import_record is None:
        raise HTTPException(status_code=404, detail=["Import not found."])

    user = session.get(UserRecord, import_record.user_id)
    bank = session.get(BankRecord, import_record.bank_id)
    if user is None:
        raise HTTPException(
            status_code=500,
            detail=["Please contact your local support admin. User is None."],
        )
    if bank is None:
        raise HTTPException(
            status_code=500,
            detail=["Please contact your local support admin. Bank is None."],
        )

    transaction_record: Sequence[TransactionRecord] = session.exec(
        select(TransactionRecord)
        .where(TransactionRecord.import_id == import_id)
        .order_by(TransactionRecord.transaction_date)
    ).all()

    transactions = [
        Transaction(
            imported_date=import_record.created_at,
            transaction_date=t.transaction_date,
            id=t.id,
            user=user.name,
            merchant=t.merchant,
            amount=t.amount,
            category_id=t.category_id,
            bank_category=t.bank_category,
            ignore=t.ignore,
            bank=bank.code,
        )
        for t in transaction_record
    ]

    return transactions


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
        transactions = PARSERS[db_bank.code].parse(decoded)
    except ParserError as e:
        raise HTTPException(
            status_code=400, detail=e.errors if e.errors else [str(e)]
        ) from e
    except UnicodeDecodeError as e:
        raise HTTPException(
            status_code=400, detail=["File must be UTF-8 encoded"]
        ) from e

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
    return ImportResult(
        filename=file.filename,
        id=import_record_id,
        user=person,
        num_need_category=len(transactions),  # TODO when categorization is done
        num_transactions=len(transactions),
    )
