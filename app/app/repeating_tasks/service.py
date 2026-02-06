import uuid
from datetime import datetime, timezone

from fastapi import Depends

from app.repeating_tasks.entity import RepeatingTask
from app.repeating_tasks.repository import (
    PostgresRepeatingTaskRepository,
    RepeatingTaskRepository,
)


class RepeatingTaskService:
    def __init__(
        self,
        repository: RepeatingTaskRepository = Depends(PostgresRepeatingTaskRepository),
    ):
        self.repository = repository

    def add_task(self, name: str, repeats_every_days: int) -> RepeatingTask:
        task = RepeatingTask(
            id=str(uuid.uuid4()),
            name=name,
            repeats_every_days=repeats_every_days,
            created_at=datetime.now(timezone.utc),
        )
        return self.repository.add(task)
