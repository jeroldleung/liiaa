import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from schemas import ProductAttributes

prompt_templates = {}

PROMPTS_DIR_PATH = "./prompts"


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    load_prompts()
    yield
    prompt_templates.clear()


def load_prompts():
    for filename in os.listdir(PROMPTS_DIR_PATH):
        if not filename.endswith(".txt"):
            continue
        file_path = os.path.join(PROMPTS_DIR_PATH, filename)
        with open(file_path, "r") as f:
            prompt = f.read()
        prompt_name = filename[:-4]
        prompt_templates[prompt_name] = prompt


app = FastAPI(
    title="Liiaa",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    lifespan=lifespan,
)


@app.get("/extract_attributes")
async def extract_attributes(sku: str):
    llm = ChatOpenAI(
        model="qwen-turbo",
        temperature=0,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
    )
    prompt = PromptTemplate.from_template(prompt_templates["extractor"])
    extractor = prompt | llm.with_structured_output(ProductAttributes)

    res = extractor.invoke(sku)

    return res
