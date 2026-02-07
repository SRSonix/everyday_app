from fastapi import APIRouter, Depends, HTTPException

from app.repeating_tasks.exceptions import TaskNotFoundError
from app.repeating_tasks.schemas import (
    PaginatedResponse,
    RepeatingTaskCreateRequest,
    RepeatingTaskResponse,
    TaskCompletionResponse,
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
    return RepeatingTaskResponse.from_entity(task)


@router.get("/repeating-tasks", response_model=PaginatedResponse[RepeatingTaskResponse])
def get_all_repeating_tasks(
    page: int = 1,
    page_size: int = 20,
    service: RepeatingTaskService = Depends(RepeatingTaskService),
) -> PaginatedResponse[RepeatingTaskResponse]:
    result = service.get_all_tasks(page=page, page_size=page_size)
    return PaginatedResponse[RepeatingTaskResponse](
        items=[RepeatingTaskResponse.from_entity(task) for task in result.items],
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    )


@router.post(
    "/repeating-tasks/{task_id}/completions",
    response_model=TaskCompletionResponse,
    status_code=201,
)
def complete_task(
    task_id: str,
    service: RepeatingTaskService = Depends(RepeatingTaskService),
) -> TaskCompletionResponse:
    try:
        completion = service.complete_task(task_id)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskCompletionResponse.from_entity(completion)


@router.get(
    "/repeating-tasks/{task_id}/completions",
    response_model=PaginatedResponse[TaskCompletionResponse],
)
def get_task_completions(
    task_id: str,
    page: int = 1,
    page_size: int = 20,
    service: RepeatingTaskService = Depends(RepeatingTaskService),
) -> PaginatedResponse[TaskCompletionResponse]:
    try:
        result = service.get_task_completions(task_id, page=page, page_size=page_size)
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")

    return PaginatedResponse[TaskCompletionResponse](
        items=[TaskCompletionResponse.from_entity(c) for c in result.items],
        total=result.total,
        page=result.page,
        page_size=result.page_size,
    )
