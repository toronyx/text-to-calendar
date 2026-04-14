from fastapi import Request
from fastapi.responses import JSONResponse
from google import genai
from ttc_server.clients.llm.llm_client import LLMException


async def llm_exception_handler(request: Request, exc: LLMException):
    cause = exc.__cause__
    if isinstance(cause, genai.errors.ClientError):  # add more error types here for other LLMs as needed
        return JSONResponse(
            status_code=422,  # unprocessable
            content={"detail": cause.message},
        )
    elif isinstance(cause, genai.errors.ServerError):  # add more error types here for other LLMs as needed
        return JSONResponse(
            status_code=502,  # upstream service failed
            content={"detail": cause.message},
        )
    return JSONResponse(
        status_code=502,  # upstream service failed
        content={"detail": f"LLM error: {cause}"},
    )
