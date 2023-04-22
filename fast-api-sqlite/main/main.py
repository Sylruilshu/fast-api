from sql_functions import (
    get_users,
    get_user,
    insert_user,
    remove_user,
    check_user_exists,
    update_info,
)
from models import User, UserUpdate
from fastapi import FastAPI, HTTPException
import sqlite3


app = FastAPI()

conn = sqlite3.connect("database.db")
cursor = conn.cursor()


@app.get("/")
async def route():
    return {"Hello": "Mundo"}


@app.get("/api/v1/users")
async def fetch_users() -> list[User]:
    return get_users()


@app.post("/api/v1/users")
async def register_user(user: User) -> User:
    if not check_user_exists(user.id):
        insert_user(user)
        return user
    else:
        raise HTTPException(
            status_code=409, detail=f"User with id: {user.id} already exists"
        )


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: str) -> str:
    if check_user_exists(user_id):
        remove_user(user_id)
        return user_id
    else:
        raise HTTPException(
            status_code=404, detail=f"User with id: {user_id} does not exist"
        )


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdate, user_id: str) -> User:
    if check_user_exists(user_id):
        old_user = get_user(user_id)
        if user_update.first is not None:
            new_first = user_update.first
        else:
            new_first = old_user["first"]
        if user_update.middle is not None:
            new_middle = user_update.middle
        else:
            new_middle = old_user["middle"]
        if user_update.last is not None:
            new_last = user_update.last
        else:
            new_last = old_user["last"]
        if user_update.role is not None:
            new_role = user_update.role
        else:
            new_role = old_user["role"]
        gender = old_user["gender"]
        update_info(user_id, new_first, new_middle, new_last, new_role)
        return {
            "id": user_id,
            "first": new_first,
            "middle": new_middle,
            "last": new_last,
            "gender": gender,
            "role": new_role,
        }
    else:
        raise HTTPException(
            status_code=404, detail=f"User with id: {user_id} does not exist"
        )


conn.close()
