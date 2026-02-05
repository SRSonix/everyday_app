from datetime import datetime

from pydantic import BaseModel


class RepeatingTask(BaseModel):
    id: str
    name: str
    repeats_every_days: int
    created_at: datetime
    last_run: datetime | None = None
