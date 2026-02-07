from fastapi.testclient import TestClient

from tests.conftest import assert_valid_iso_datetime, assert_valid_uuid


class TestCreateRepeatingTask:
    def test_returns_201(self, client: TestClient):
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
        assert_valid_uuid(body["id"])
        assert_valid_iso_datetime(body["created_at"])
        assert body["last_done_at"] is None

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
    def test_returns_200_with_last_done_none(
        self, client: TestClient, seed_repeating_task
    ):
        # given
        seed_repeating_task(name="Exercise", repeats_every_days=3)

        # when
        response = client.get("/repeating-tasks")

        # then
        assert response.status_code == 200
        body = response.json()
        assert len(body["items"]) == 1
        assert body["items"][0]["name"] == "Exercise"
        assert body["items"][0]["last_done_at"] is None
        assert body["total"] == 1
        assert body["page"] == 1

    def test_returns_last_done_after_completion(
        self, client: TestClient, seed_repeating_task, seed_task_completion
    ):
        # given
        task = seed_repeating_task(name="Meditate", repeats_every_days=1)
        seed_task_completion(task.id)

        # when
        response = client.get("/repeating-tasks")

        # then
        body = response.json()
        assert len(body["items"]) == 1
        assert body["items"][0]["last_done_at"] is not None


class TestCompleteTask:
    def test_returns_201(self, client: TestClient, seed_repeating_task):
        # given
        task = seed_repeating_task()

        # when
        response = client.post(f"/repeating-tasks/{task.id}/completions")

        # then
        assert response.status_code == 201
        body = response.json()
        assert_valid_uuid(body["id"])
        assert body["task_id"] == task.id
        assert_valid_iso_datetime(body["done_at"])

    def test_returns_404_for_nonexistent_task(self, client: TestClient):
        # when
        response = client.post("/repeating-tasks/nonexistent-id/completions")

        # then
        assert response.status_code == 404


class TestGetTaskCompletions:
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
        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 2
        assert body["page"] == 1
        assert body["page_size"] == 20
        assert len(body["items"]) == 2
        assert all(c["task_id"] == task.id for c in body["items"])

    def test_returns_404_for_nonexistent_task(self, client: TestClient):
        # when
        response = client.get("/repeating-tasks/nonexistent-id/completions")

        # then
        assert response.status_code == 404
