import asyncio
import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from websockets.asyncio.server import ServerConnection, serve


async def chat(websocket: ServerConnection):
    client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"))
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

    async def handshake():
        msg_from_device = json.loads(await websocket.recv())
        msg_to_device = {
            "type": "hello",
            "transport": "websocket",
            "audio_params": {"sample_rate": 16000},
        }
        if "type" in msg_from_device and "hello" == msg_from_device["type"]:
            await websocket.send(json.dumps(msg_to_device))

    async def stream_llm_response(
        client: OpenAI,
        messages: list[dict[str, str]],
    ) -> str:
        response = ""
        for chunk in client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            modalities=["text"],
            stream=True,
        ):
            text = chunk.choices[0].delta.content
            if text is not None:
                response += text
                await websocket.send(text)
        return response

    await handshake()
    async for msg in websocket:
        messages.append({"role": "user", "content": msg})
        response = await stream_llm_response(client, messages)
        messages.append({"role": "assistant", "content": response})


async def main():
    async with serve(chat, "0.0.0.0", 8000) as server:
        await server.serve_forever()


if __name__ == "__main__":
    assert load_dotenv(), "Failed to load environment variables"
    asyncio.run(main())
