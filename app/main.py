from fastapi import FastAPI

from app.routers import tasks

app = FastAPI(title="Liiaa", swagger_ui_parameters={"defaultModelsExpandDepth": -1})

app.include_router(tasks.router)
