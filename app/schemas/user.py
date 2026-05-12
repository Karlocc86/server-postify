import uuid
from datetime import datetime

from sqlmodel import SQLModel


class UserCreate(SQLModel):
    username: str
    name: str
    lastname: str
    email: str
    password: str


class UserRead(SQLModel):
    id: uuid.UUID
    username: str
    name: str
    lastname: str
    email: str
    created_at: datetime