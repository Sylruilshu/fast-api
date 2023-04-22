from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    user = "user"
    student = "student"


class Gender(str, Enum):
    male = "male"
    female = "female"


class User(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    first: str
    middle: Optional[str]
    last: str
    gender: Gender
    role: Role


class UserUpdate(BaseModel):
    first: Optional[str]
    middle: Optional[str]
    last: Optional[str]
    role: Optional[Role]
