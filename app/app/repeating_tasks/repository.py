from typing import Protocol

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import get_db_session
from app.repeating_tasks.entity import PaginatedResult, RepeatingTask, TaskCompletion
from app.repeating_tasks.models import RepeatingTaskORM, TaskCompletionORM


class RepeatingTaskRepository(Protocol):
    def add(self, task: RepeatingTask) -> RepeatingTask: ...
    def get_by_id(self, task_id: str) -> RepeatingTask | None: ...
    def get_all_with_last_done(
        self, limit: int, offset: int
    ) -> PaginatedResult[RepeatingTask]: ...
    def add_completion(self, completion: TaskCompletion) -> TaskCompletion: ...
    def get_completions_paginated(
        self, task_id: str, limit: int, offset: int
    ) -> PaginatedResult[TaskCompletion]: ...


class PostgresRepeatingTaskRepository:
    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    def add(self, task: RepeatingTask) -> RepeatingTask:
        orm_task = RepeatingTaskORM.from_entity(task)
        self.session.add(orm_task)
        self.session.commit()
        self.session.refresh(orm_task)
        return task

    def get_by_id(self, task_id: str) -> RepeatingTask | None:
        orm_task = self.session.get(RepeatingTaskORM, task_id)
        if orm_task is None:
            return None
        return orm_task.to_entity()

    def get_all_with_last_done(
        self, limit: int, offset: int
    ) -> PaginatedResult[RepeatingTask]:
        last_done_subquery = (
            self.session.query(
                TaskCompletionORM.task_id,
                func.max(TaskCompletionORM.done_at).label("last_done_at"),
            )
            .group_by(TaskCompletionORM.task_id)
            .subquery()
        )

        base_query = self.session.query(
            RepeatingTaskORM, last_done_subquery.c.last_done_at
        ).join(
            last_done_subquery,
            RepeatingTaskORM.id == last_done_subquery.c.task_id,
            isouter=True,
        )

        total = base_query.count()
        rows = base_query.offset(offset).limit(limit).all()

        items = [
            orm_task.to_entity(last_done_at=last_done_at)
            for orm_task, last_done_at in rows
        ]

        page = offset // limit + 1
        return PaginatedResult(items=items, total=total, page=page, page_size=limit)

    def add_completion(self, completion: TaskCompletion) -> TaskCompletion:
        orm_completion = TaskCompletionORM.from_entity(completion)
        self.session.add(orm_completion)
        self.session.commit()
        self.session.refresh(orm_completion)
        return completion

    def get_completions_paginated(
        self, task_id: str, limit: int, offset: int
    ) -> PaginatedResult[TaskCompletion]:
        base_query = self.session.query(TaskCompletionORM).filter(
            TaskCompletionORM.task_id == task_id
        )

        total = base_query.count()
        rows = (
            base_query.order_by(TaskCompletionORM.done_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        items = [row.to_entity() for row in rows]

        page = offset // limit + 1
        return PaginatedResult(items=items, total=total, page=page, page_size=limit)
