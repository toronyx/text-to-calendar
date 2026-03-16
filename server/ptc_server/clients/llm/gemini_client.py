import logging
from typing import Iterator
from google import genai

from ptc_server.clients.llm.llm_client import LLMClient, LLMException
from ptc_server.config import GEMINI_API_KEY, GEMINI_MODEL_NAME

logger = logging.getLogger(__name__)


class GeminiException(LLMException):
    def __init__(self, message: str):
        super().__init__(message)


class GeminiClient(LLMClient):
    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or GEMINI_API_KEY
        if not self.api_key:
            raise GeminiException("GEMINI_API_KEY not found in environment.")
        self.model_name = model_name or GEMINI_MODEL_NAME
        self.client = genai.Client(api_key=self.api_key)

    def stream_model_response(self, prompt: str) -> Iterator[str]:
        logger.info(f"Request to Gemini API (stream), prompt: {prompt}")
        response_stream = self.client.models.generate_content_stream(model=self.model_name, contents=prompt)
        try:
            for chunk in response_stream:
                logger.info(f"Streaming Gemini response: {chunk.text}")
                yield chunk.text
        except (genai.errors.ServerError, genai.errors.ClientError) as e:
            logger.error(f"Error communicating with Gemini: {e}")
            raise GeminiException(f"Error communicating with Gemini: {e}") from e

    def get_model_response(self, prompt: str) -> str:
        logger.info(f"Request to Gemini API (non-stream), prompt: {prompt}")
        try:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt)
        except (genai.errors.ServerError, genai.errors.ClientError) as e:
            logger.error(f"Error communicating with Gemini: {e}")
            raise GeminiException(f"Error communicating with Gemini: {e}") from e
        logger.info(f"Gemini response: {response.text}")
        return response.text
