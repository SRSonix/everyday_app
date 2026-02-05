from typing import Protocol

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import get_db_session
from app.repeating_tasks.entity import RepeatingTask
from app.repeating_tasks.models import RepeatingTaskORM


class RepeatingTaskRepository(Protocol):
    def add(self, task: RepeatingTask) -> RepeatingTask: ...


class PostgresRepeatingTaskRepository:
    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    def add(self, task: RepeatingTask) -> RepeatingTask:
        orm_task = RepeatingTaskORM.from_entity(task)
        self.session.add(orm_task)
        self.session.commit()
        self.session.refresh(orm_task)
        return task
