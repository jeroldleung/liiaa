import uuid

from fastapi import APIRouter, BackgroundTasks, Depends

from app.chains.extractor import extract_attribute
from app.dependencies import Settings, get_settings
from app.schemas.task import TaskRequest, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

actions = {"extraction": extract_attribute}
tasks_state = {}


@router.get("/")
async def list_all_tasks():
    return list(tasks_state.values())


@router.get("/actions")
async def list_all_available_actions():
    return list(actions.keys())


@router.post("/create")
async def create_a_task(
    r: TaskRequest, bg_task: BackgroundTasks, settings: Settings = Depends(get_settings)
):
    task_id = uuid.uuid4()
    bg_task.add_task(
        actions[r.action], task_id, tasks_state, r.input, settings.dashscope_api_key
    )
    return TaskResponse(id=task_id, completed=False)
