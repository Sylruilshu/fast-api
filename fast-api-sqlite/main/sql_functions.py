from models import User
import sqlite3


KEYS = ["id", "first", "middle", "last", "gender", "role"]
ROLE_TO_ID = {"admin": 1, "user": 2, "student": 3}
GENDER_TO_ID = {"male": 1, "female": 2}

conn = sqlite3.connect("database.db")
cursor = conn.cursor()


def get_users() -> list[User]:
    with conn:
        cursor.execute(
            """
            SELECT 
                u.id, first, middle, last, gender, role
            FROM 
                users as u
                INNER JOIN genders AS g ON g.id=gender_id 
                INNER JOIN roles AS r ON r.id=role_id
            """
        )
        users = cursor.fetchall()
        return [dict(zip(KEYS, user)) for user in users]


def get_user(user_id: str) -> User:
    with conn:
        cursor.execute(
            """
            SELECT 
                u.id, first, middle, last, gender, role 
            FROM 
                users as u
                INNER JOIN genders AS g ON g.id=gender_id 
                INNER JOIN roles AS r ON r.id=role_id
            WHERE 
                u.id=:id
            """,
            {"id": user_id},
        )
        user = cursor.fetchone()
        return dict(zip(KEYS, user))


def insert_user(user: User):
    with conn:
        role_id = ROLE_TO_ID[user.role]
        gender_id = GENDER_TO_ID[user.gender]
        cursor.execute(
            "INSERT INTO users VALUES (:id, :first, :middle, :last, :gender_id, :role_id)",
            {
                "id": str(user.id),
                "first": user.first,
                "middle": user.middle,
                "last": user.last,
                "gender_id": gender_id,
                "role_id": role_id,
            },
        )


def remove_user(user_id: str):
    with conn:
        cursor.execute("DELETE FROM users WHERE id=:id", {"id": f"{user_id}"})


def check_user_exists(user_id: str) -> bool:
    with conn:
        cursor.execute("SELECT * FROM users WHERE id=:id", {"id": f"{user_id}"})
        result = cursor.fetchone()
    if result:
        return True
    else:
        return False


def update_info(id: str, first: str, middle: str, last: str, role: str):
    with conn:
        role_id = ROLE_TO_ID[role]
        cursor.execute(
            """
            UPDATE 
                users 
            SET 
                first=:first, middle=:middle, last=:last, role_id=:role_id 
            WHERE 
                id=:id
            """,
            {
                "id": id,
                "first": first,
                "middle": middle,
                "last": last,
                "role_id": role_id,
            },
        )
