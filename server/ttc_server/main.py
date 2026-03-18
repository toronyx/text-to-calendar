from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from ttc_server.clients.llm.gemini_client import GeminiClient
from ttc_server.logger_config import setup_logging
from ttc_server.mocks.mock_llm_client import MockLLMClient
from ttc_server.routes.endpoints import router
from ttc_server.services.llm_service import LLMService

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.llm_service = LLMService(GeminiClient())
    try:
        yield  # app runs here
    finally:
        pass  # do any cleanup


app = FastAPI(title="Text to Calendar API", lifespan=lifespan)

app.include_router(router)
