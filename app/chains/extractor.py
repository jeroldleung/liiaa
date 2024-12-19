import os
import uuid
from typing import List

from dotenv import load_dotenv
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI

from app.schemas.product import Product
from app.schemas.task import TaskResults


async def extract_attribute(task_id: uuid.UUID, tasks_state: dict, input: List[str]):
    if not load_dotenv():
        tasks_state[task_id] = TaskResults(
            id=task_id,
            completed=False,
            description="could not load .env file",
            data=None,
        )
        return

    api_key = os.getenv("DASHSCOPE_API_KEY")

    if api_key == None:
        tasks_state[task_id] = TaskResults(
            id=task_id,
            completed=False,
            description="DASHSCOPE_API_KEY does not exist in the .env file",
            data=None,
        )
        return

    llm = ChatOpenAI(
        model="qwen-turbo",
        temperature=0,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
    )
    sys_prompt = SystemMessagePromptTemplate.from_template(
        "You are an expert extraction algorithm."
    )
    user_prompt = HumanMessagePromptTemplate.from_template(
        "Extract the product attribute from the following sku: {sku}"
    )
    prompt = ChatPromptTemplate([sys_prompt, user_prompt])
    extractor = prompt | llm.with_structured_output(Product)

    val = []
    for sku in input:
        res = extractor.invoke(sku)
        val.append(res)

    tasks_state[task_id] = TaskResults(
        id=task_id,
        completed=True,
        description="Extraction task complete successfully",
        data=val,
    )
