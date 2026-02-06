import uuid
from datetime import datetime

from fastapi.testclient import TestClient

from app.repeating_tasks.service import RepeatingTaskService


class TestRepeatingTaskService:
    def test_add_task_generates_correct_fields(
        self, repeating_task_service: RepeatingTaskService
    ):
        # when
        result = repeating_task_service.add_task(name="Meditate", repeats_every_days=1)

        # then
        assert len(result.id) == 36
        assert isinstance(result.created_at, datetime)
        assert result.last_run is None

    def test_add_task_passes_correct_values(
        self, repeating_task_service: RepeatingTaskService
    ):
        # when
        result = repeating_task_service.add_task(name="Exercise", repeats_every_days=7)

        # then
        assert result.name == "Exercise"
        assert result.repeats_every_days == 7


class TestRepeatingTaskEndpoint:
    def test_create_repeating_task_returns_201(
        self,
        client: TestClient,
    ):
        # when
        response = client.post(
            "/repeating-tasks",
            json={"name": "Exercise", "repeats_every_days": 3},
        )

        # then
        assert response.status_code == 201
        body = response.json()
        assert body["name"] == "Exercise"
        assert body["repeats_every_days"] == 3
        self._assert_valid_uuid(body["id"])
        self._assert_valid_iso_datetime(body["created_at"])
        assert body["last_run"] is None

    def test_create_repeating_task_rejects_empty_name(self, client: TestClient):
        # when
        response = client.post(
            "/repeating-tasks",
            json={"name": "", "repeats_every_days": 1},
        )

        # then
        assert response.status_code == 422

    def test_create_repeating_task_rejects_zero_days(self, client: TestClient):
        # when
        response = client.post(
            "/repeating-tasks",
            json={"name": "Task", "repeats_every_days": 0},
        )

        # then
        assert response.status_code == 422

    def test_create_repeating_task_rejects_missing_fields(self, client: TestClient):
        # when
        response = client.post("/repeating-tasks", json={})

        # then
        assert response.status_code == 422

    def _assert_valid_uuid(self, uuid_string: str) -> None:
        """Assert that the given string is a valid UUID."""
        assert len(uuid_string) == 36
        uuid.UUID(uuid_string)  # Raises ValueError if invalid

    def _assert_valid_iso_datetime(self, datetime_string: str) -> None:
        """Assert that the given string is a valid ISO datetime string."""
        created_at = datetime.fromisoformat(datetime_string.replace("Z", "+00:00"))
        assert isinstance(created_at, datetime)
