from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TodoBase(BaseModel):
    title: str
    description: str | None = None


class TodoCreate(TodoBase):
    completed: bool = False


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class TodoResponse(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime | None = None


    model_config = ConfigDict(from_attributes=True)
