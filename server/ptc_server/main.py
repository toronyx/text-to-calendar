from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from ptc_server.clients.llm.gemini_client import GeminiClient
from ptc_server.logger_config import setup_logging
from ptc_server.mocks.mock_llm_client import MockLLMClient
from ptc_server.routes.endpoints import router
from ptc_server.services.llm_service import LLMService

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.llm_service = LLMService(GeminiClient())
    try:
        yield  # app runs here
    finally:
        pass  # do any cleanup


app = FastAPI(title="Job Hunt Automation API", lifespan=lifespan)

app.include_router(router)
