# Rough workings!

import sqlite3
from models import User, Gender, Role


KEYS = ["id", "first", "middle", "last", "gender", "role"]
conn = sqlite3.connect(":memory:")

cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE users (
    id TEXT NOT NULL PRIMARY KEY, 
    first TEXT NOT NULL,
    middle TEXT, 
    last TEXT NOT NULL,
    gender_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY(gender_id) REFERENCES genders(id)
    FOREIGN KEY(role_id) REFERENCES roles(id)
    )"""
)

cursor.execute(
    """CREATE TABLE genders (
    id INTEGER NOT NULL PRIMARY KEY,
    gender TEXT NOT NULL
    )"""
)

cursor.execute(
    """CREATE TABLE roles (
    id INTEGER NOT NULL PRIMARY KEY,
    role TEXT NOT NULL
    )"""
)


cursor.execute("INSERT INTO genders VALUES (1, 'male'), (2, 'female')")


cursor.execute("INSERT INTO roles VALUES (1, 'admin'), (2, 'user'), (3, 'student')")


def get_users() -> list[User]:
    with conn:
        cursor.execute(
            "SELECT u.id, first, middle, last, gender, role FROM users AS u INNER JOIN genders AS g ON g.id=gender_id INNER JOIN roles AS r ON r.id=role_id"
        )
        users = cursor.fetchall()
        print(users)
        return [dict(zip(KEYS, user)) for user in users]


def get_user(user_id: str) -> User:
    with conn:
        cursor.execute(
            """SELECT u.id, first, middle, last, gender 
        FROM users AS u
        INNER JOIN genders WHERE u.id = users_id"""
        )
        user = cursor.fetchone()
        return dict(zip(KEYS, user))


# def insert_user(user: User, gender_id: int):
#     with conn:
#         cursor.execute(
#             "INSERT INTO users VALUES (:id, :first, :middle, :last, :gender_id)",
#             {
#                 "id": str(user.id),
#                 "first": user.first,
#                 "middle": user.middle,
#                 "last": user.last,
#                 "gender_id": gender_id,
#             },
#         )


def insert_user(user: User):
    with conn:
        if user.gender == "male":
            cursor.execute(
                "INSERT INTO users VALUES (:id, :first, :middle, :last, :gender_id, :role_id)",
                {
                    "id": str(user.id),
                    "first": user.first,
                    "middle": user.middle,
                    "last": user.last,
                    "gender_id": 1,
                    "role_id": 1,
                },
            )
        if user.gender == "female":
            cursor.execute(
                "INSERT INTO users VALUES (:id, :first, :middle, :last, :gender_id, :role_id)",
                {
                    "id": str(user.id),
                    "first": user.first,
                    "middle": user.middle,
                    "last": user.last,
                    "gender_id": 2,
                    "role_id": 3,
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


def update_info(
    id: str, first: str, middle: str, last: str, role: str
):  # Make args optional
    with conn:
        cursor.execute("SELECT * FROM roles WHERE role=:role", {"role": role})
        role_id = cursor.fetchone()[0]
        print(role_id)
        # cursor.execute(
        #     "UPDATE users SET first=:first, middle=:middle, last=:last WHERE id=:id",  # <------- Make sql statement dynamic
        #     {"first": first, "middle": middle, "last": last, "id": id},
        # )


user1 = User(
    id="0fe0f9c8-41d4-46c7-9f83-f2c8630fa12f",
    first="John",
    middle="A",
    last="Smith",
    gender=Gender.male,
    role=Role.admin,
)

user2 = User(
    id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
    first="Foo",
    last="Jones",
    gender=Gender.female,
    role=Role.student,
)

insert_user(user1)
insert_user(user2)

# print(get_users())

update_info(user2.id, user2.first, user2.middle, user2.last, user2.role)

# user = get_user("0fe0f9c8-41d4-46c7-9f83-f2c8630fa12f")
# print(user)

# print(check_user_exists("0fe0f9c8-41d4-46c7-9f83-f2c8630fa12f"))

# users = get_users_by_last_name("Jones")
# users = fetch_users()
# print(users)

# update_user_middle_name(user1, "******")

# remove_user(user2)

# users = get_users_by_last_name("Bar")
# print(users)

conn.close()
