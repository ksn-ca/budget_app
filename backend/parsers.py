import csv
from collections.abc import Callable
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from io import StringIO
from typing import NamedTuple

from models import Transaction

ParseFn = Callable[[str, str, int], list[Transaction]]

WS_COLUMNS = {
    "transaction_type",
    "status",
    "transaction_date",
    "merchant",
    "amount",
    "category",
}


class ParserError(ValueError):
    """CSV does not meet the correct format"""

    def __init__(self, message: str, errors: list[str] | None = None):
        super().__init__(message)
        self.errors = errors or []


class BankParser(NamedTuple):
    label: str
    parse: ParseFn


PARSERS: dict[str, BankParser] = {}


def register(val: str, label: str):
    def decorator(func: ParseFn) -> ParseFn:
        PARSERS[val] = BankParser(label, func)
        return func

    return decorator


@register("auto", "Auto-detect")
def parse_auto(text: str, user: str, import_id: int) -> list[Transaction]:
    raise NotImplementedError


@register("ws", "Wealthsimple")
def parse_ws(text: str, user: str, import_id: int) -> list[Transaction]:
    reader = csv.DictReader(StringIO(text))

    if reader.fieldnames is None:
        raise ParserError("No columns detected")

    cols = set(reader.fieldnames)
    if not WS_COLUMNS <= cols:
        diff = WS_COLUMNS - cols
        diff_sorted = ", ".join(sorted(diff))
        raise ParserError(f"Required columns are not present: {diff_sorted}")

    imported_at = datetime.now()
    transactions: list[Transaction] = []
    errors: list[str] = []
    for row in reader:
        if None in row.values():
            errors.append(f"Line {reader.line_num}: the row is not complete")
            continue
        if None in row:
            errors.append(
                f"Line {reader.line_num}: the row has more values than headers"
            )
            continue
        if (
            row["transaction_type"].strip() == "Payment"
            or row["status"].strip() == "Pending"
        ):
            continue
        try:
            transaction = Transaction(
                imported_date=imported_at,
                transaction_date=date.fromisoformat(row["transaction_date"]),
                user=user,
                description=row["merchant"].strip(),
                amount=Decimal(row["amount"]),
                import_id=import_id,
                bank_category=row["category"].strip(),
            )
            transactions.append(transaction)

        except ValueError as e:
            errors.append(f"Line {reader.line_num}: {e}")
        except InvalidOperation:
            errors.append(f"Line {reader.line_num}: invalid amount")

    if errors:
        raise ParserError(f"{len(errors)} invalid rows", errors)

    return transactions


@register("rogers", "Rogers Bank")
def parse_rogers(text: str, user: str, import_id: int) -> list[Transaction]:
    raise NotImplementedError


@register("pcf", "PC Financial")
def parse_pcf(text: str, user: str, import_id: int) -> list[Transaction]:
    raise NotImplementedError


@register("mnba", "MNBA")
def parse_mnba(text: str, user: str, import_id: int) -> list[Transaction]:
    raise NotImplementedError
