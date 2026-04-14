from fastapi import Request
from fastapi.responses import JSONResponse
from google import genai
from ttc_server.clients.llm.llm_client import LLMException


async def llm_exception_handler(request: Request, exc: LLMException):
    cause = exc.__cause__
    if isinstance(cause, genai.errors.ClientError):  # add more error types here for other LLMs as needed
        detail = {
            429: "Gemini API request limit reached!",
        }.get(cause.status_code, f"Gemini Client error {cause}")
        return JSONResponse(
            status_code=422,  # unprocessable
            content={"detail": detail},
        )
    elif isinstance(cause, genai.errors.ServerError):  # add more error types here for other LLMs as needed
        detail = {
            503: "Gemini server is currently overloaded! Try again later.",
        }.get(cause.status_code, f"Gemini Server error {cause}")
        return JSONResponse(
            status_code=502,  # upstream service failed
            content={"detail": detail},
        )
    return JSONResponse(
        status_code=502,  # upstream service failed
        content={"detail": f"LLM error: {cause}"},
    )
