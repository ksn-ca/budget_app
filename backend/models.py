from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, ConfigDict, computed_field

CENTS = Decimal("0.01")


def to_cents(value: Decimal) -> Decimal:
    return value.quantize(CENTS, rounding=ROUND_HALF_UP)


Money = Annotated[Decimal, AfterValidator(to_cents)]


class User(BaseModel):
    name: str
    accent: Literal["lime", "sky"]
    income: Money
    expenses: Money

    @computed_field
    @property
    def percent_spent(self) -> int:
        if self.income == 0:
            return 0
        return int((self.expenses / self.income * 100).quantize(1, ROUND_HALF_UP))


class Bank(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    code: str


class Kind(StrEnum):
    PURCHASE = "purchase"
    REFUND = "refund"
    CASHBACK = "cashback"


class ParsedTransaction(BaseModel):
    transaction_date: date
    merchant: str
    amount: Money
    bank_category: str | None = None
    ignore: bool = False
    # kind: Kind
    # status: str


class Transaction(ParsedTransaction):
    id: int
    imported_date: datetime
    user: str
    bank: str
    category_id: int | None = None


class ImportResult(BaseModel):
    filename: str
    id: int
    user: str
    num_transactions: int
    num_need_category: int


class Category(BaseModel):
    category_name: str
    category_id: int
