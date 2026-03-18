from pathlib import Path

import ptc_server
from ptc_server.clients.llm.llm_client import LLMClient


class MockLLMClient(LLMClient):
    def get_model_response(self, prompt: str) -> str:
        response_text_path = Path(ptc_server.mocks.__path__[0]) / "example_model_response.txt"
        response_text = response_text_path.read_text(encoding="utf-8")
        return response_text
