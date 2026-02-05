from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from app.app import create_app
from app.config import get_db_session
from app.repeating_tasks.models import Base, RepeatingTaskORM
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
def db_session(db_setup, postgres_url: str) -> Session:
    engine = create_engine(postgres_url)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
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
    return mock


@pytest.fixture
def repeating_task_service(repeating_task_repository_mock: RepeatingTaskRepository) -> RepeatingTaskService:
    return RepeatingTaskService(repository=repeating_task_repository_mock)
