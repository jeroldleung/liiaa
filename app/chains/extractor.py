import uuid
from typing import List

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI

from app.schemas.product import Product
from app.schemas.run import RunResult


async def extract_attribute(
    run_id: uuid.UUID, runs_state: dict, input: List[str], api_key: str
):
    llm = ChatOpenAI(
        model="qwen-turbo",
        temperature=0,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=api_key,
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

    runs_state[run_id] = RunResult(
        id=run_id,
        completed=True,
        description="Extraction complete successfully",
        data=val,
    )
