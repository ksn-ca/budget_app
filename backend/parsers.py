from models import Transaction
import csv
from io import StringIO

def parse_auto(text: str, user: str, import_id: int) -> list[Transaction]:
    raise NotImplementedError

def parse_ws(text: str, user: str, import_id: int) -> list[Transaction]:
    reader = csv.DictReader(StringIO(text))
    

def parse_rogers(text: str, user: str, import_id: int) -> list[Transaction]:
    raise NotImplementedError

def parse_pcf(text: str, user: str, import_id: int) -> list[Transaction]:
    raise NotImplementedError

def parse_mnba(text: str, user: str, import_id: int) -> list[Transaction]:
    raise NotImplementedError


PARSERS = {
    "auto": parse_auto,
    "ws": parse_ws,
    "rogers": parse_rogers,
    "pcf": parse_pcf,
    "mnba": parse_mnba,
}
