from typing import Literal, Annotated
from datetime import date, datetime
from decimal import Decimal

from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    name: str
    accent: Literal["lime", "sky"]
    income: float
    expenses: float

class Transaction(BaseModel):
    imported_date: datetime
    transaction_date: date
    user: str
    description: str
    amount: Decimal 
    category: str | None = None
    import_id: int

class ImportResult(BaseModel):
    filename: str
    id: int
    user: str
    num_transactions: int
    num_need_category: int


users: list[User] = [
    User(name="Sienna", accent="lime", income=3000, expenses=2000),
    User(name="Nikita", accent="sky", income=5000, expenses=1000),
] 

@app.get("/users")
def list_users() -> list[User]:
    return users


# @app.post("/users", status_code=201)
# def create_user(user: User) -> User:
#     users.append(user)
#     return user

@app.post("/imports", status_code=201)
async def upload_csv(file: UploadFile, bank: Annotated[str, Form()], person: Annotated[str, Form()]) -> ImportResult:
    await file.read()
    return ImportResult(filename=file.filename, id=1, user=person, num_need_category=2, num_transactions=3 )
