from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.app import create_app
from app.repeating_tasks.repository import RepeatingTaskRepository
from app.repeating_tasks.service import RepeatingTaskService


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def repeating_task_repository_mock() -> RepeatingTaskRepository:
    mock = MagicMock(spec=RepeatingTaskRepository)
    mock.add.side_effect = lambda task: task
    return mock


@pytest.fixture
def repeating_task_service(repeating_task_repository_mock: RepeatingTaskRepository) -> RepeatingTaskService:
    return RepeatingTaskService(repository=repeating_task_repository_mock)
