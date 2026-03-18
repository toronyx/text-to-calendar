from pathlib import Path

import ttc_server
from ttc_server.clients.llm.llm_client import LLMClient


class MockLLMClient(LLMClient):
    def __init__(self, response: str = None):
        self.response = response

    def get_model_response(self, prompt: str) -> str:
        if self.response:
            return self.response
        response_text_path = Path(ttc_server.mocks.__path__[0]) / "example_model_response.txt"
        response_text = response_text_path.read_text(encoding="utf-8")
        return response_text
