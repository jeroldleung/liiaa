import uuid
from typing import Any, List

from pydantic import BaseModel


class TaskRequest(BaseModel):
    action: str
    input: List[str]


class TaskResponse(BaseModel):
    id: uuid.UUID
    completed: bool


class TaskResults(TaskResponse):
    value: List[Any]
