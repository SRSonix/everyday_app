from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy.orm import DeclarativeBase

from app.repeating_tasks.entity import RepeatingTask


class Base(DeclarativeBase):
    pass


class RepeatingTaskORM(Base):
    __tablename__ = "repeating_tasks"

    id = Column[str](Text, primary_key=True)
    name = Column[str](Text, nullable=False)
    repeats_every_days = Column[int](Integer, nullable=False)
    created_at = Column[datetime](DateTime, nullable=False)
    last_run = Column[datetime](DateTime, nullable=True)

    @classmethod
    def from_entity(cls, task: RepeatingTask) -> "RepeatingTaskORM":
        return cls(
            id=task.id,
            name=task.name,
            repeats_every_days=task.repeats_every_days,
            created_at=task.created_at,
            last_run=task.last_run,
        )
