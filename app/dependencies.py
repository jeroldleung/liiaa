import os

from fastapi import HTTPException


def get_api_key() -> str:
    key = os.getenv("DASHSCOPE_API_KEY")
    if key is None:
        raise HTTPException(
            status_code=500,
            detail="API key not found in the environment variables.",
        )
    return key
