import csv
from collections.abc import Callable
from io import StringIO
from typing import NamedTuple

from models import Transaction

ParseFn = Callable[[str, str, int], list[Transaction]]


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
    return [1, 2, 3, 4, 5, 6, 9]


@register("rogers", "Rogers Bank")
def parse_rogers(text: str, user: str, import_id: int) -> list[Transaction]:
    raise NotImplementedError


@register("pcf", "PC Financial")
def parse_pcf(text: str, user: str, import_id: int) -> list[Transaction]:
    raise NotImplementedError


@register("mnba", "MNBA")
def parse_mnba(text: str, user: str, import_id: int) -> list[Transaction]:
    raise NotImplementedError
