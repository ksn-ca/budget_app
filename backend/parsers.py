import csv
from collections.abc import Callable
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from io import StringIO
from typing import Any, NamedTuple

from models import Transaction

ParseFn = Callable[[str, str, int], list[Transaction]]
RowMapper = Callable[[dict[str, str]], dict[str, Any]]

WS_COLUMNS = {
    "transaction_type",
    "status",
    "transaction_date",
    "merchant",
    "amount",
    "category",
}

ROGERS_COLUMNS = {
    "Date",
    "Activity Type",
    "Activity Status",
    "Merchant Name",
    "Amount",
    "Merchant Category Description",
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


def _parse_money(amt: str) -> Decimal:
    return Decimal(amt.replace("$", "").replace(",", "").strip())


def register(val: str, label: str):
    def decorator(func: ParseFn) -> ParseFn:
        PARSERS[val] = BankParser(label, func)
        return func

    return decorator


def _parse_csv(
    text: str,
    user: str,
    import_id: int,
    *,
    bank: str,
    required_columns: set[str],
    map_row: RowMapper,
) -> list[Transaction]:
    reader = csv.DictReader(StringIO(text))

    if reader.fieldnames is None:
        raise ParserError("No columns detected")

    missing = required_columns - set(reader.fieldnames)
    if missing:
        raise ParserError(
            f"Required columns are not present: {', '.join(sorted(missing))}"
        )

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
        try:
            transactions.append(
                Transaction(
                    imported_date=imported_at,
                    user=user,
                    import_id=import_id,
                    bank=bank,
                    **map_row(row),
                )
            )
        except ValueError as e:
            errors.append(f"Line {reader.line_num}: {e}")
        except InvalidOperation:
            errors.append(f"Line {reader.line_num}: invalid amount")

    if errors:
        raise ParserError(f"{len(errors)} invalid rows", errors)

    return transactions


@register("auto", "Auto-detect")
def parse_auto(text: str, user: str, import_id: int) -> list[Transaction]:
    raise ParserError("Auto-detect is not supported yet.")


def _map_ws_row(row: dict[str, str]) -> dict[str, Any]:
    return {
        "transaction_date": date.fromisoformat(row["transaction_date"]),
        "merchant": row["merchant"].strip(),
        "amount": _parse_money(row["amount"]),
        "bank_category": row["category"].strip(),
        "ignore": (
            row["transaction_type"].strip().lower() == "payment"
            or row["status"].strip().lower() == "pending"
        ),
    }


def _map_rogers_row(row: dict[str, str]) -> dict[str, Any]:
    return {
        "transaction_date": date.fromisoformat(row["Date"]),
        "merchant": row["Merchant Name"].strip(),
        "amount": _parse_money(row["Amount"]),
        "bank_category": row["Merchant Category Description"].strip(),
        "ignore": (
            row["Activity Type"].strip().lower() == "payment"
            or row["Activity Status"].strip().lower() == "pending"
        ),
    }


@register("ws", "Wealthsimple")
def parse_ws(text: str, user: str, import_id: int) -> list[Transaction]:
    return _parse_csv(
        text,
        user,
        import_id,
        bank="ws",
        required_columns=WS_COLUMNS,
        map_row=_map_ws_row,
    )


@register("rogers", "Rogers Bank")
def parse_rogers(text: str, user: str, import_id: int) -> list[Transaction]:
    return _parse_csv(
        text,
        user,
        import_id,
        bank="rogers",
        required_columns=ROGERS_COLUMNS,
        map_row=_map_rogers_row,
    )


@register("pcf", "PC Financial")
def parse_pcf(text: str, user: str, import_id: int) -> list[Transaction]:
    raise ParserError("Bank is not supported yet.")


@register("mbna", "MBNA")
def parse_mbna(text: str, user: str, import_id: int) -> list[Transaction]:
    raise ParserError("Bank is not supported yet.")
