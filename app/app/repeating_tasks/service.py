import uuid
from datetime import datetime, timezone

from fastapi import Depends

from app.repeating_tasks.entity import PaginatedResult, RepeatingTask, TaskCompletion
from app.repeating_tasks.exceptions import TaskNotFoundError
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

    def get_all_tasks(
        self, page: int = 1, page_size: int = 20
    ) -> PaginatedResult[RepeatingTask]:
        offset = (page - 1) * page_size
        return self.repository.get_all_with_last_done(limit=page_size, offset=offset)

    def complete_task(self, task_id: str) -> TaskCompletion:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        completion = TaskCompletion(
            id=str(uuid.uuid4()),
            task_id=task_id,
            done_at=datetime.now(timezone.utc),
        )
        return self.repository.add_completion(completion)

    def get_task_completions(
        self, task_id: str, page: int = 1, page_size: int = 20
    ) -> PaginatedResult[TaskCompletion]:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        offset = (page - 1) * page_size
        return self.repository.get_completions_paginated(
            task_id, limit=page_size, offset=offset
        )
