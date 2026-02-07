from datetime import datetime
from app.repeating_tasks.entity import RepeatingTask, TaskCompletion
from typing import Self


class RepeatingTaskGenerator:
    def __init__(self):
        self._id = "task-1"
        self._name = "Exercise"
        self._repeats_every_days = 1
        self._created_at = datetime(2025, 1, 1)
        self._last_done_at = None

    def with_id(self, id: str) -> Self:
        self._id = id
        return self

    def with_repeats_every_days(self, days: int) -> Self:
        self._repeats_every_days = days
        return self

    def with_last_done_at(self, dt: datetime) -> Self:
        self._last_done_at = dt
        return self

    def make(self) -> RepeatingTask:
        return RepeatingTask(
            id=self._id,
            name=self._name,
            repeats_every_days=self._repeats_every_days,
            created_at=self._created_at,
            last_done_at=self._last_done_at,
        )


class TaskCompletionGenerator:
    def __init__(self):
        self._id = "c-1"
        self._task_id = "task-123"
        self._done_at = datetime(2025, 6, 15)

    def with_task_id(self, task_id: str) -> Self:
        self._task_id = task_id
        return self

    def make(self) -> TaskCompletion:
        return TaskCompletion(
            id=self._id,
            task_id=self._task_id,
            done_at=self._done_at,
        )
