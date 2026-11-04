from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, computed_field

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
    label: str
    val: str


class Transaction(BaseModel):
    imported_date: datetime
    transaction_date: date
    user: str
    description: str
    amount: Money
    category_id: int | None = None
    bank_category: str | None = None
    import_id: int


class ImportResult(BaseModel):
    filename: str
    id: int
    user: str
    num_transactions: int
    num_need_category: int


class Category(BaseModel):
    category_name: str
    category_id: int
