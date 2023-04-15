from fastapi import FastAPI, HTTPException
from models import User, Gender, Role
from typing import List
from uuid import UUID, uuid4


app = FastAPI()

db: List[User] = [
    # User(
    #     id=uuid4(),
    #     first_name="Jemma",
    #     last_name="Smith",
    #     gender=Gender.female,
    #     roles=[Role.student]
    # ),
    User(
        id=UUID("ea474970-3f8c-45f2-b625-45dd289dd2e3"),
        first_name="Jemma",
        last_name="Smith",
        gender=Gender.female,
        roles=[Role.student],
    ),
    User(
        id=UUID("76d7fc2b-cfa2-4b6f-a3a6-f3cff241ecdb"),
        first_name="Alex",
        last_name="Jones",
        gender=Gender.male,
        roles=[Role.admin, Role.user],
    ),
]


@app.get("/")
async def route():
    return {"Hello": "Mundo"}


@app.get("/api/v1/users")
async def fetch_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404, detail=f"User with id: {user_id} does not exist."
    )
