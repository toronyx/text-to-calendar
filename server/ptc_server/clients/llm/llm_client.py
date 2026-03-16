from abc import ABC, abstractmethod
from typing import Iterator


class LLMClient(ABC):

    @abstractmethod
    def stream_model_response(self, prompt: str) -> Iterator[str]:
        pass

    @abstractmethod
    def get_model_response(self, prompt: str) -> str:
        pass