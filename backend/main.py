from typing import Annotated

from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

from models import User, ImportResult, Bank

from parsers import PARSERS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

banks: list[Bank] = [
    Bank(label="Auto-detect", val="auto"),
    Bank(label="Wealthsimple", val="ws"),
    Bank(label="Rogers Bank", val="rogers"),
    Bank(label="PC Financial", val="pcf"),
    Bank(label="MNBA", val="mnba"),
]


users: list[User] = [
    User(name="Sienna", accent="lime", income=3000, expenses=2000),
    User(name="Nikita", accent="sky", income=5000, expenses=1000),
] 

@app.get("/users")
def list_users() -> list[User]:
    return users


# @app.post("/users", status_code=201)
# def create_user(user: User) -> User:
#     users.append(user)
#     return user

@app.post("/imports", status_code=201)
async def upload_csv(file: UploadFile, bank: Annotated[str, Form()], person: Annotated[str, Form()]) -> ImportResult:
    await file.read()
    return ImportResult(filename=file.filename, id=1, user=person, num_need_category=4, num_transactions=3 )
