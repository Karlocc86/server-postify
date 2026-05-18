



from datetime import datetime
import uuid

from sqlmodel import SQLModel


class PostCreate(SQLModel):
    description: str
    users_id: uuid.UUID


class PostRead(SQLModel):
    id: uuid.UUID
    users_id: uuid.UUID
    description: str
    created_at: datetime

class PostUpdate(SQLModel):
    description: str
    users_id: uuid.UUID

class PostDelete(SQLModel):
    id: uuid.UUID

