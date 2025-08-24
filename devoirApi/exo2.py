from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

fake_users = [
    User(id=1, name="Alice", email="alice@example.com"),
    User(id=2, name="Bob", email="bob@example.com"),
    User(id=3, name="Charlie", email="charlie@example.com"),
]

@app.get("/users", response_model=List[User])
def get_users(page: int = Query(1, ge=1), size: int = Query(20, ge=1)):
    try:
        start = (page - 1) * size
        end = start + size
        return fake_users[start:end]
    except Exception:
        raise HTTPException(status_code=400, detail="Bad types for provided query parameters")
