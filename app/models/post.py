from datetime import datetime
import uuid
from sqlmodel import Relationship, SQLModel, Field


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id :uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    description: str
    users_id: uuid.UUID = Field(foreign_key="users.id")
    created_at:datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="posts")