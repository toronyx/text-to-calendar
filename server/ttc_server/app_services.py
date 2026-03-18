from fastapi import Request
from ttc_server.services.llm_service import LLMService


def get_llm_service(request: Request) -> LLMService:
    return request.app.state.llm_service
