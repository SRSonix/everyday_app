from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class RepeatingTask(BaseModel):
    id: str
    name: str
    repeats_every_days: int
    created_at: datetime
    last_done_at: datetime | None = None


class TaskCompletion(BaseModel):
    id: str
    task_id: str
    done_at: datetime


class PaginatedResult(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
