import uuid
from datetime import datetime, timezone
from typing import Callable, Iterator
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from app.main import create_app
from app.config import get_db_session
from app.repeating_tasks.models import Base, RepeatingTaskORM, TaskCompletionORM
from app.repeating_tasks.repository import RepeatingTaskRepository
from app.repeating_tasks.service import RepeatingTaskService


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:17") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def postgres_url(postgres_container) -> str:
    return postgres_container.get_connection_url()


@pytest.fixture(scope="session")
def db_setup(postgres_url: str):
    engine = create_engine(postgres_url)
    Base.metadata.create_all(engine)


@pytest.fixture
def db_session(db_setup, postgres_url: str) -> Iterator[Session]:
    engine = create_engine(postgres_url)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.execute(delete(TaskCompletionORM))
    session.execute(delete(RepeatingTaskORM))
    session.commit()
    session.close()


@pytest.fixture
def app(db_session: Session) -> FastAPI:
    application = create_app()

    def override_get_db_session():
        yield db_session

    application.dependency_overrides[get_db_session] = override_get_db_session
    return application


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def repeating_task_repository_mock() -> RepeatingTaskRepository:
    mock = MagicMock(spec=RepeatingTaskRepository)
    mock.add.side_effect = lambda task: task
    mock.get_by_id.return_value = None
    mock.add_completion.side_effect = lambda completion: completion
    return mock


@pytest.fixture
def repeating_task_service(
    repeating_task_repository_mock: RepeatingTaskRepository,
) -> RepeatingTaskService:
    return RepeatingTaskService(repository=repeating_task_repository_mock)


@pytest.fixture
def seed_repeating_task(db_session: Session) -> Callable[..., RepeatingTaskORM]:
    def _seed(
        name: str = "Exercise",
        repeats_every_days: int = 3,
    ) -> RepeatingTaskORM:
        task = RepeatingTaskORM(
            id=str(uuid.uuid4()),
            name=name,
            repeats_every_days=repeats_every_days,
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        return task

    return _seed


@pytest.fixture
def seed_task_completion(db_session: Session) -> Callable[..., TaskCompletionORM]:
    def _seed(task_id: str) -> TaskCompletionORM:
        completion = TaskCompletionORM(
            id=str(uuid.uuid4()),
            task_id=task_id,
            done_at=datetime.now(timezone.utc),
        )
        db_session.add(completion)
        db_session.commit()
        db_session.refresh(completion)
        return completion

    return _seed


def assert_valid_uuid(uuid_string: str) -> None:
    assert len(uuid_string) == 36
    uuid.UUID(uuid_string)


def assert_valid_iso_datetime(datetime_string: str) -> None:
    parsed = datetime.fromisoformat(datetime_string.replace("Z", "+00:00"))
    assert isinstance(parsed, datetime)
