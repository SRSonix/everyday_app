import json
from pathlib import Path

from app.repeating_tasks.entity import RepeatingTask

DATABASE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "database"
DATABASE_FILE = DATABASE_DIR / "repeating_tasks.json"


class RepeatingTaskRepository:
    def __init__(self, database_file: Path = DATABASE_FILE):
        self.database_file = database_file

    def _read_all(self) -> list[dict]:
        if not self.database_file.exists():
            return []
        with open(self.database_file, "r") as f:
            return json.load(f)

    def _write_all(self, tasks: list[dict]) -> None:
        self.database_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.database_file, "w") as f:
            json.dump(tasks, f, indent=2)

    def add(self, task: RepeatingTask) -> RepeatingTask:
        tasks = self._read_all()
        tasks.append(task.model_dump())
        self._write_all(tasks)
        return task
