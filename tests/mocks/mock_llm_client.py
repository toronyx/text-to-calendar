from ptc_server.clients.llm.llm_client import LLMClient


class MockLLMClient(LLMClient):
    def __init__(self, response: str):
        self._response = response

    def get_model_response(self, prompt: str) -> str:
        return self._response
