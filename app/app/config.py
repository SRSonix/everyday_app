from typing import Generator

from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/everyday"

    model_config = {"env_prefix": ""}


def get_settings() -> Settings:
    return Settings()


engine = create_engine(get_settings().database_url)
SessionLocal = sessionmaker(bind=engine)


def get_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
