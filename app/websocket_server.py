from loguru import logger
from websockets.asyncio.server import serve

from .router import Router


class WebsocketServer:
    @staticmethod
    async def start():
        async with serve(Router.route, "0.0.0.0", 8000) as server:
            logger.success("Server started")
            await server.serve_forever()
