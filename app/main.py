from fastapi import FastAPI

from app.routers import runs

app = FastAPI(title="Liiaa", swagger_ui_parameters={"defaultModelsExpandDepth": -1})

app.include_router(runs.router)
