import uuid
from datetime import datetime

import pytest

from app.repeating_tasks.entity import PaginatedResult
from app.repeating_tasks.exceptions import TaskNotFoundError
from app.repeating_tasks.service import RepeatingTaskService
from tests.generator import RepeatingTaskGenerator, TaskCompletionGenerator


class TestAddTask:
    def test_generates_correct_fields(
        self, repeating_task_service: RepeatingTaskService
    ):
        # when
        result = repeating_task_service.add_task(name="Meditate", repeats_every_days=1)

        # then
        assert_is_uuid(result.id)
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
        task_id = "task-123"
        repeating_task_repository_mock.get_by_id.return_value = (
            RepeatingTaskGenerator().with_id(task_id).make()
        )

        # when
        result = repeating_task_service.complete_task(task_id)

        # then
        assert result.task_id == task_id
        assert_is_uuid(result.id)
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
        paginated_task = make_paginated(
            [RepeatingTaskGenerator().with_repeats_every_days(3).make()]
        )
        repeating_task_repository_mock.get_all_with_last_done.return_value = (
            paginated_task
        )

        # when
        result = repeating_task_service.get_all_tasks()

        # then
        assert_paginated(result, expected_count=1)
        assert result.items[0].last_done_at is None

    def test_returns_tasks_with_last_done(
        self,
        repeating_task_service: RepeatingTaskService,
        repeating_task_repository_mock,
    ):
        # given
        last_done = datetime(2025, 6, 15)
        paginated_task = make_paginated(
            [
                RepeatingTaskGenerator()
                .with_repeats_every_days(3)
                .with_last_done_at(last_done)
                .make()
            ]
        )
        repeating_task_repository_mock.get_all_with_last_done.return_value = (
            paginated_task
        )

        # when
        result = repeating_task_service.get_all_tasks()

        # then
        assert_paginated(result, expected_count=1)
        assert result.items[0].last_done_at == last_done


class TestGetTaskCompletions:
    def test_returns_completions_for_existing_task(
        self,
        repeating_task_service: RepeatingTaskService,
        repeating_task_repository_mock,
    ):
        # given
        task_id = "task-123"
        repeating_task_repository_mock.get_by_id.return_value = (
            RepeatingTaskGenerator().with_id(task_id).make()
        )
        repeating_task_repository_mock.get_completions_paginated.return_value = (
            make_paginated([TaskCompletionGenerator().with_task_id(task_id).make()])
        )

        # when
        result = repeating_task_service.get_task_completions(task_id)

        # then
        assert_paginated(result, expected_count=1)
        assert result.items[0].task_id == task_id

    def test_raises_for_nonexistent_task(
        self, repeating_task_service: RepeatingTaskService
    ):
        # when / then
        with pytest.raises(TaskNotFoundError):
            repeating_task_service.get_task_completions("nonexistent-id")


def make_paginated(items: list, page: int = 1, page_size: int = 20) -> PaginatedResult:
    return PaginatedResult(
        items=items, total=len(items), page=page, page_size=page_size
    )


# parses the string as a UUID, failing the test if it's malformed
def assert_is_uuid(value: str) -> None:
    uuid.UUID(value)


def assert_paginated(result: PaginatedResult, expected_count: int) -> None:
    assert len(result.items) == expected_count
    assert result.total == expected_count
