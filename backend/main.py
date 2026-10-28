from typing import Annotated

from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from models import Bank, ImportResult, User
from parsers import PARSERS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

banks: list[Bank] = [Bank(val=val, label=bp.label) for val, bp in PARSERS.items()]


users: list[User] = [
    User(name="Sienna", accent="lime", income=3000, expenses=2000),
    User(name="Nikita", accent="sky", income=5000, expenses=1000),
]


@app.get("/users")
def list_users() -> list[User]:
    return users


@app.get("/banks")
def list_banks() -> list[Bank]:
    return banks


# @app.post("/users", status_code=201)
# def create_user(user: User) -> User:
#     users.append(user)
#     return user


@app.post("/imports", status_code=201)
async def upload_csv(
    file: UploadFile, bank: Annotated[str, Form()], person: Annotated[str, Form()]
) -> ImportResult:
    if bank not in PARSERS:
        raise HTTPException(status_code=400, detail=f"Unknown Bank: {bank}")

    raw = await file.read()
    decoded = raw.decode("utf-8-sig")
    temp_id: int = 1
    transactions = PARSERS[bank].parse(decoded, person, temp_id)
    return ImportResult(
        filename=file.filename,
        id=temp_id,
        user=person,
        num_need_category=4,
        num_transactions=len(transactions),
    )
