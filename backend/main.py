from decimal import Decimal
from typing import Annotated

from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from models import Bank, ImportResult, Transaction, User
from parsers import PARSERS, ParserError

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
async def upload_csv(
    file: UploadFile, bank: Annotated[str, Form()], person: Annotated[str, Form()]
) -> ImportResult:
    if bank not in PARSERS:
        raise HTTPException(status_code=400, detail=[f"Unknown Bank: {bank}"])

    raw = await file.read()
    decoded = raw.decode("utf-8-sig")
    temp_id: int = 1
    try:
        transactions = PARSERS[bank].parse(decoded, person, temp_id)
    except ParserError as e:
        raise HTTPException(
            status_code=400, detail=e.errors if e.errors else [str(e)]
        ) from e
    num_need_category: int = sum(1 for t in transactions if t.category_id is None)
    imported_transactions[temp_id] = transactions
    return ImportResult(
        filename=file.filename,
        id=temp_id,
        user=person,
        num_need_category=num_need_category,
        num_transactions=len(transactions),
    )
