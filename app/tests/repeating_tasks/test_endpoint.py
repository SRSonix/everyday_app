from fastapi.testclient import TestClient
from httpx import Response

from tests.conftest import assert_valid_iso_datetime, assert_valid_uuid


class TestCreateRepeatingTask:
    def test_returns_201_and_valid_task(self, client: TestClient):
        # when
        response = client.post(
            "/repeating-tasks",
            json={"name": "Exercise", "repeats_every_days": 3},
        )

        # then
        assert response.status_code == 201
        assert_task_body(response.json(), name="Exercise", repeats_every_days=3)

    def test_rejects_empty_name(self, client: TestClient):
        # when
        response = client.post(
            "/repeating-tasks",
            json={"name": "", "repeats_every_days": 1},
        )

        # then
        assert response.status_code == 422

    def test_rejects_zero_days(self, client: TestClient):
        # when
        response = client.post(
            "/repeating-tasks",
            json={"name": "Task", "repeats_every_days": 0},
        )

        # then
        assert response.status_code == 422

    def test_rejects_missing_fields(self, client: TestClient):
        # when
        response = client.post("/repeating-tasks", json={})

        # then
        assert response.status_code == 422


class TestGetAllRepeatingTasks:
    def test_returns_empty_list(self, client: TestClient):
        # when
        response = client.get("/repeating-tasks")

        # then
        assert_ok_paginated(response, expected_count=0)

    def test_returns_200_with_last_done_none(
        self, client: TestClient, seed_repeating_task
    ):
        # given
        seed_repeating_task(name="Exercise", repeats_every_days=3)

        # when
        response = client.get("/repeating-tasks")

        # then
        assert_ok_paginated(response, expected_count=1)
        body = response.json()
        assert body["items"][0]["name"] == "Exercise"
        assert body["items"][0]["last_done_at"] is None

    def test_returns_last_done_after_completion(
        self, client: TestClient, seed_repeating_task, seed_task_completion
    ):
        # given
        task = seed_repeating_task(name="Meditate", repeats_every_days=1)
        seed_task_completion(task.id)

        # when
        response = client.get("/repeating-tasks")

        # then
        assert_ok_paginated(response, expected_count=1)
        body = response.json()
        assert body["items"][0]["last_done_at"] is not None


class TestCompleteTask:
    def test_returns_201(self, client: TestClient, seed_repeating_task):
        # given
        task = seed_repeating_task()

        # when
        response = client.post(f"/repeating-tasks/{task.id}/completions")

        # then
        assert response.status_code == 201
        assert_completion_body(response.json(), task_id=task.id)

    def test_returns_404_for_nonexistent_task(self, client: TestClient):
        # when
        response = client.post("/repeating-tasks/nonexistent-id/completions")

        # then
        assert response.status_code == 404


class TestGetTaskCompletions:
    def test_returns_empty_list(self, client: TestClient, seed_repeating_task):
        # given
        task = seed_repeating_task()

        # when
        response = client.get(f"/repeating-tasks/{task.id}/completions")

        # then
        assert_ok_paginated(response, expected_count=0)

    def test_returns_200(
        self, client: TestClient, seed_repeating_task, seed_task_completion
    ):
        # given
        task = seed_repeating_task()
        seed_task_completion(task.id)
        seed_task_completion(task.id)

        # when
        response = client.get(f"/repeating-tasks/{task.id}/completions")

        # then
        assert_ok_paginated(response, expected_count=2)
        body = response.json()
        assert all(c["task_id"] == task.id for c in body["items"])

    def test_returns_404_for_nonexistent_task(self, client: TestClient):
        # when
        response = client.get("/repeating-tasks/nonexistent-id/completions")

        # then
        assert response.status_code == 404


def assert_ok_paginated(
    response: Response, expected_count: int, expected_page: int = 1
) -> None:
    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == expected_count
    assert body["total"] == expected_count
    assert body["page"] == expected_page


def assert_task_body(body: dict, name: str, repeats_every_days: int) -> None:
    assert body["name"] == name
    assert body["repeats_every_days"] == repeats_every_days
    assert_valid_uuid(body["id"])
    assert_valid_iso_datetime(body["created_at"])
    assert body["last_done_at"] is None


def assert_completion_body(body: dict, task_id: str) -> None:
    assert_valid_uuid(body["id"])
    assert body["task_id"] == task_id
    assert_valid_iso_datetime(body["done_at"])
