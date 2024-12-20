import uuid

from fastapi import APIRouter, BackgroundTasks, Depends

from app.chains.extractor import extract_attribute
from app.dependencies import EnvVar, get_env_var
from app.schemas.run import RunRequest, RunResponse

router = APIRouter(prefix="/runs", tags=["runs"])

runs_state = {}


@router.get("/")
async def list_all_runs():
    return list(runs_state.values())


@router.post("/extract")
async def extract_product_attributes_from_sku(
    run: RunRequest, bg_task: BackgroundTasks, env: EnvVar = Depends(get_env_var)
):
    run_id = uuid.uuid4()
    bg_task.add_task(
        extract_attribute, run_id, runs_state, run.input, env.dashscope_api_key
    )
    return RunResponse(id=run_id, completed=False)
