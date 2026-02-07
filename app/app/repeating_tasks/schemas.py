from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from app.repeating_tasks.entity import RepeatingTask, TaskCompletion

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int


class RepeatingTaskCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    repeats_every_days: int = Field(ge=1)


class RepeatingTaskResponse(BaseModel):
    id: str
    name: str
    repeats_every_days: int
    created_at: datetime
    last_done_at: datetime | None

    @classmethod
    def from_entity(cls, task: RepeatingTask) -> "RepeatingTaskResponse":
        return cls(
            id=task.id,
            name=task.name,
            repeats_every_days=task.repeats_every_days,
            created_at=task.created_at,
            last_done_at=task.last_done_at,
        )


class TaskCompletionResponse(BaseModel):
    id: str
    task_id: str
    done_at: datetime

    @classmethod
    def from_entity(cls, completion: TaskCompletion) -> "TaskCompletionResponse":
        return cls(
            id=completion.id,
            task_id=completion.task_id,
            done_at=completion.done_at,
        )
