from loguru import logger
from websockets.asyncio.server import ServerConnection
from websockets.exceptions import ConnectionClosed

from app.services import AudioService, ChatService

from .schemas import AudioState, MessageIn, MessageOut, MessageType


class ConnectionHandler:
    audio_service: AudioService = None
    chat_service: ChatService = None

    def __init__(self, websocket: ServerConnection):
        self.websocket = websocket
        self.audio_in: list[bytes] = []

    async def response_text(self, m_out: MessageOut):
        m_out = m_out.model_dump_json(exclude_unset=True)
        await self.websocket.send(m_out)
        logger.debug(f"Message out: {m_out}")

    async def handle_text(self, m_in: str):
        logger.debug(f"Message in: {m_in}")
        m = MessageIn.model_validate_json(m_in)
        if m.type == MessageType.HELLO:
            m_out = MessageOut(
                type=MessageType.HELLO,
                transport="websocket",
                audio_params={"sample_rate": 16000},
            )
            await self.response_text(m_out)
            logger.info("Handshake with client")
        elif m.type == MessageType.LISTEN and m.state == AudioState.START:
            self.audio_in.clear()
        elif m.type == MessageType.LISTEN and m.state == AudioState.STOP:
            if len(self.audio_in) == 0:
                return
            asr_text = ConnectionHandler.audio_service.speech2text(self.audio_in)
            logger.info(f"Client audio message: {asr_text}")
            chat_completion = ConnectionHandler.chat_service.chat_completion(asr_text)
            m_out = MessageOut(
                type=MessageType.TTS,
                state=AudioState.SENTENCE_START,
                text=chat_completion,
            )
            await self.response_text(m_out)
            logger.info(f"Response to client: {chat_completion}")

    async def handle_binary(self, m_in: bytes):
        self.audio_in.append(m_in)

    async def handle_message(self):
        while True:
            try:
                m_in = await self.websocket.recv()
                if isinstance(m_in, str):
                    await self.handle_text(m_in)
                elif isinstance(m_in, bytes):
                    await self.handle_binary(m_in)
            except ConnectionClosed:
                break

    @classmethod
    def inject(cls, audio_service: AudioService, chat_service: ChatService):
        cls.audio_service = audio_service
        cls.chat_service = chat_service

    @staticmethod
    async def instantiate(websocket: ServerConnection):
        if ConnectionHandler.audio_service is None:
            logger.error("Audio Service is not injected")
        print(ConnectionHandler.chat_service)
        if ConnectionHandler.chat_service is None:
            logger.error("Chat Service is not injected")

        # create a handler instance for each websocket connection
        logger.info(f"Connection opened: {websocket.id}")
        connection = ConnectionHandler(websocket)
        await connection.handle_message()
        logger.info(f"Connection closed: {websocket.id}")
