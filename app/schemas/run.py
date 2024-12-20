import uuid
from typing import Any, List, Optional

from pydantic import BaseModel


class RunRequest(BaseModel):
    input: List[str]


class RunResponse(BaseModel):
    id: uuid.UUID
    completed: bool


class RunResult(RunResponse):
    description: str
    data: Optional[List[Any]]
