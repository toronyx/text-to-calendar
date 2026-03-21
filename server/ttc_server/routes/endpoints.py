from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from ttc_core.ics_generator import calendar_to_ics
from ttc_core.models.calendar import Calendar
from ttc_server.app_services import get_llm_service
from ttc_server.config import ICS_PRODID
from ttc_server.services.llm_service import LLMService

router = APIRouter()


@router.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Welcome to the text to calendar API!",
        "version": "0.1.0",
    }


@router.post("/prompt_to_calendar_object/")
def prompt_to_calendar_object(llm_service: Annotated[LLMService, Depends(get_llm_service)], prompt: str) -> Calendar:
    calendar_events = llm_service.calendar_events_from_prompt(prompt)
    calendar = Calendar(prodid=ICS_PRODID, method=None, events=calendar_events)
    return calendar


@router.post("/calendar_to_ics_file/")
def calendar_to_ics_file(calendar: Calendar):
    ics_data = calendar_to_ics(calendar)

    generated_files_dir = Path(__file__).parent.parent / "generated"
    generated_files_dir.mkdir(exist_ok=True)
    filename = datetime.now().strftime("calendar_%Y%m%dT%H%M%SZ.ics")
    file_path = generated_files_dir / filename
    file_path.write_text(ics_data, encoding="utf-8")
    return FileResponse(path=file_path, media_type="text/calendar", filename=filename)
