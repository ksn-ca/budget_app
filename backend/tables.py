from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import DateTime, func
from sqlmodel import Field, SQLModel


class ImportRecord(SQLModel, table=True):
    __tablename__ = "imports"

    id: int | None = Field(default=None, primary_key=True)
    filename: str
    user_id: int = Field(foreign_key="users.id")
    bank_id: int = Field(foreign_key="banks.id")
    created_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )


class BankRecord(SQLModel, table=True):
    __tablename__ = "banks"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    code: str = Field(unique=True)


class UserRecord(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    name: str


class CategoryRecord(SQLModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)


class TransactionRecord(SQLModel, table=True):
    __tablename__ = "transactions"

    id: int | None = Field(default=None, primary_key=True)
    transaction_date: date
    import_id: int = Field(foreign_key="imports.id", index=True, ondelete="CASCADE")
    merchant: str
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    category_id: int | None = Field(
        default=None, foreign_key="categories.id", ondelete="SET NULL"
    )
    bank_category: str | None = None
    ignore: bool = False
