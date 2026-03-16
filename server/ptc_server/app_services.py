from fastapi import Request
from ptc_server.services.llm_service import LLMService


def get_llm_service(request: Request) -> LLMService:
    return request.app.state.llm_service
