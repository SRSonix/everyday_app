from datetime import datetime

import pytest

from app.repeating_tasks.entity import PaginatedResult, RepeatingTask, TaskCompletion
from app.repeating_tasks.exceptions import TaskNotFoundError
from app.repeating_tasks.service import RepeatingTaskService


class TestAddTask:
    def test_generates_correct_fields(
        self, repeating_task_service: RepeatingTaskService
    ):
        # when
        result = repeating_task_service.add_task(name="Meditate", repeats_every_days=1)

        # then
        assert len(result.id) == 36
        assert isinstance(result.created_at, datetime)

    def test_passes_correct_values(self, repeating_task_service: RepeatingTaskService):
        # when
        result = repeating_task_service.add_task(name="Exercise", repeats_every_days=7)

        # then
        assert result.name == "Exercise"
        assert result.repeats_every_days == 7


class TestCompleteTask:
    def test_generates_id_and_timestamp(
        self,
        repeating_task_service: RepeatingTaskService,
        repeating_task_repository_mock,
    ):
        # given
        repeating_task_repository_mock.get_by_id.return_value = RepeatingTask(
            id="task-123",
            name="Exercise",
            repeats_every_days=1,
            created_at=datetime(2025, 1, 1),
        )

        # when
        result = repeating_task_service.complete_task("task-123")

        # then
        assert len(result.id) == 36
        assert result.task_id == "task-123"
        assert isinstance(result.done_at, datetime)

    def test_raises_for_nonexistent_task(
        self, repeating_task_service: RepeatingTaskService
    ):
        # when / then
        with pytest.raises(TaskNotFoundError):
            repeating_task_service.complete_task("nonexistent-id")


class TestGetAllTasks:
    def test_returns_tasks_without_last_done(
        self,
        repeating_task_service: RepeatingTaskService,
        repeating_task_repository_mock,
    ):
        # given
        task = RepeatingTask(
            id="task-1",
            name="Exercise",
            repeats_every_days=3,
            created_at=datetime(2025, 1, 1),
        )
        repeating_task_repository_mock.get_all_with_last_done.return_value = (
            PaginatedResult(items=[task], total=1, page=1, page_size=20)
        )

        # when
        result = repeating_task_service.get_all_tasks()

        # then
        assert len(result.items) == 1
        assert result.items[0].last_done_at is None
        assert result.total == 1

    def test_returns_tasks_with_last_done(
        self,
        repeating_task_service: RepeatingTaskService,
        repeating_task_repository_mock,
    ):
        # given
        task = RepeatingTask(
            id="task-1",
            name="Exercise",
            repeats_every_days=3,
            created_at=datetime(2025, 1, 1),
            last_done_at=datetime(2025, 6, 15),
        )
        repeating_task_repository_mock.get_all_with_last_done.return_value = (
            PaginatedResult(items=[task], total=1, page=1, page_size=20)
        )

        # when
        result = repeating_task_service.get_all_tasks()

        # then
        assert len(result.items) == 1
        assert result.items[0].last_done_at == datetime(2025, 6, 15)


class TestGetTaskCompletions:
    def test_returns_completions_for_existing_task(
        self,
        repeating_task_service: RepeatingTaskService,
        repeating_task_repository_mock,
    ):
        # given
        repeating_task_repository_mock.get_by_id.return_value = RepeatingTask(
            id="task-123",
            name="Exercise",
            repeats_every_days=1,
            created_at=datetime(2025, 1, 1),
        )
        completions = [
            TaskCompletion(id="c-1", task_id="task-123", done_at=datetime(2025, 6, 15)),
        ]
        repeating_task_repository_mock.get_completions_paginated.return_value = (
            PaginatedResult(items=completions, total=1, page=1, page_size=20)
        )

        # when
        result = repeating_task_service.get_task_completions("task-123")

        # then
        assert len(result.items) == 1
        assert result.items[0].task_id == "task-123"
        assert result.total == 1

    def test_raises_for_nonexistent_task(
        self, repeating_task_service: RepeatingTaskService
    ):
        # when / then
        with pytest.raises(TaskNotFoundError):
            repeating_task_service.get_task_completions("nonexistent-id")
