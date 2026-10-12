from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    name: str
    accent: Literal["lime", "sky"]
    income: float
    expenses: float


users: list[User] = [
    User(name="Sienna", accent="lime", income=3000, expenses=2000),
    User(name="Nikita", accent="sky", income=5000, expenses=1000),
]


@app.get("/users")
def list_users() -> list[User]:
    return users


@app.post("/users", status_code=201)
def create_user(user: User) -> User:
    users.append(user)
    return user
