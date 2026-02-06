from fastapi import FastAPI

from app.repeating_tasks.controller import router as repeating_tasks_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(repeating_tasks_router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
