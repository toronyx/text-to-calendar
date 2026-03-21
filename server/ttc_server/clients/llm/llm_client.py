from abc import ABC, abstractmethod


class LLMException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class LLMClient(ABC):
    @abstractmethod
    def get_model_response(self, prompt: str) -> str:
        pass
