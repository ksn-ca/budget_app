from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel


class User(BaseModel):
    name: str
    accent: Literal["lime", "sky"]
    income: float
    expenses: float


class Bank(BaseModel):
    label: str
    val: str


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
