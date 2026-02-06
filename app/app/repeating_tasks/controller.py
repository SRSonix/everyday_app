from fastapi import APIRouter, Depends

from app.repeating_tasks.schemas import (
    RepeatingTaskCreateRequest,
    RepeatingTaskResponse,
)
from app.repeating_tasks.service import RepeatingTaskService

router = APIRouter()


@router.post("/repeating-tasks", response_model=RepeatingTaskResponse, status_code=201)
def create_repeating_task(
    request: RepeatingTaskCreateRequest,
    service: RepeatingTaskService = Depends(RepeatingTaskService),
) -> RepeatingTaskResponse:
    task = service.add_task(
        name=request.name, repeats_every_days=request.repeats_every_days
    )
    return RepeatingTaskResponse(
        id=task.id,
        name=task.name,
        repeats_every_days=task.repeats_every_days,
        created_at=task.created_at,
        last_run=task.last_run,
    )
