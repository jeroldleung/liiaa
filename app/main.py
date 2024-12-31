import os
from contextlib import asynccontextmanager
from typing import Any

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from app.dependencies import get_api_key
from app.schemas import ProductAttributes

prompt_templates: dict[str, str] = {}

PROMPTS_DIR_PATH = "app/prompts"


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    load_dotenv()
    load_prompts()
    yield
    prompt_templates.clear()


def load_prompts() -> None:
    for filename in os.listdir(PROMPTS_DIR_PATH):
        if not filename.endswith(".txt"):
            continue
        file_path = os.path.join(PROMPTS_DIR_PATH, filename)
        with open(file_path) as f:
            prompt = f.read()
        prompt_name = filename[:-4]
        prompt_templates[prompt_name] = prompt


app = FastAPI(
    title="Liiaa",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    lifespan=lifespan,
)


@app.get("/attributes")
async def extract_attributes(sku: str, api_key: str = Depends(get_api_key)) -> Any:
    llm = ChatOpenAI(
        model="qwen-turbo",
        temperature=0,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=SecretStr(api_key),
    )
    prompt = PromptTemplate.from_template(prompt_templates["extractor"])
    extractor = prompt | llm.with_structured_output(ProductAttributes)

    res = extractor.invoke({"sku": sku})

    return res
