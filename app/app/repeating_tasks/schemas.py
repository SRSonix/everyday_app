from datetime import datetime

from pydantic import BaseModel, Field


class RepeatingTaskCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    repeats_every_days: int = Field(ge=1)


class RepeatingTaskResponse(BaseModel):
    id: str
    name: str
    repeats_every_days: int
    created_at: datetime
    last_run: datetime | None
