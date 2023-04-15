from fastapi import FastAPI, HTTPException
from models import User, UserUpdate, Gender, Role
from typing import List
from uuid import UUID


app = FastAPI()

db: List[User] = [
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
async def fetch_user():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user_id == user.id:
            db.remove(user)
            return

    raise HTTPException(
        status_code=404, detail=f"User with id: {user_id} does not exist"
    )


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdate, user_id: UUID):
    for user in db:
        if user_id == user.id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return f"User: {user.id} info updated"

    raise HTTPException(
        status_code=404, detail="User with id: {user_id} does not exist"
    )


# {
#   "id": "ea474970-3f8c-45f2-b625-45dd289dd2e3",
#   "first_name": "FOO",
#   "last_name": "BAZ",
#   "middle_name": "BAR",
#   "gender": "female",
#   "roles": []
# }
