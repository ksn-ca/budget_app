"""Seed users and banks

Revision ID: 2503c3b3f6a0
Revises: 311e4e479630
Create Date: 2026-11-17 20:14:55.688525

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2503c3b3f6a0"
down_revision: Union[str, Sequence[str], None] = "311e4e479630"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

banks = sa.table(
    "banks",
    sa.column("name", sa.String),
    sa.column("code", sa.String),
)

users = sa.table(
    "users",
    sa.column("name", sa.String),
)

BANK_ROWS = [
    {"name": "Wealthsimple", "code": "ws"},
    {"name": "Rogers Bank", "code": "rogers"},
    {"name": "PC Financial", "code": "pcf"},
    {"name": "MBNA", "code": "mbna"},
]

USER_ROWS = [
    {"name": "Sienna"},
    {"name": "Nikita"},
]


def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(banks, BANK_ROWS)
    op.bulk_insert(users, USER_ROWS)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(users.delete().where(users.c.name.in_([r["name"] for r in USER_ROWS])))
    op.execute(banks.delete().where(banks.c.code.in_([r["code"] for r in BANK_ROWS])))
