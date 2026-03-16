from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Welcome to the prompt to calendar API!",
        "version": "0.1.0",
    }
