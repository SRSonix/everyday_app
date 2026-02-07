from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.repeating_tasks.entity import RepeatingTask, TaskCompletion


class Base(DeclarativeBase):
    pass


class RepeatingTaskORM(Base):
    __tablename__ = "repeating_tasks"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    repeats_every_days: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    @classmethod
    def from_entity(cls, task: RepeatingTask) -> "RepeatingTaskORM":
        return cls(
            id=task.id,
            name=task.name,
            repeats_every_days=task.repeats_every_days,
            created_at=task.created_at,
        )

    def to_entity(self, last_done_at: datetime | None = None) -> RepeatingTask:
        return RepeatingTask(
            id=self.id,
            name=self.name,
            repeats_every_days=self.repeats_every_days,
            created_at=self.created_at,
            last_done_at=last_done_at,
        )


class TaskCompletionORM(Base):
    __tablename__ = "task_completions"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    task_id: Mapped[str] = mapped_column(
        Text, ForeignKey("repeating_tasks.id"), nullable=False
    )
    done_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    @classmethod
    def from_entity(cls, completion: TaskCompletion) -> "TaskCompletionORM":
        return cls(
            id=completion.id,
            task_id=completion.task_id,
            done_at=completion.done_at,
        )

    def to_entity(self) -> TaskCompletion:
        return TaskCompletion(
            id=self.id,
            task_id=self.task_id,
            done_at=self.done_at,
        )
