from typing import List, Optional

from ptc_core.models.calendar_event import CalendarEvent
from pydantic import BaseModel, Field


class Calendar(BaseModel):
    prodid: str = Field(..., description="Product identifier, e.g., -//My Company//My Calendar App//EN")
    version: str = Field("2.0", description="iCalendar version")
    calscale: str = Field("GREGORIAN", description="Calendar scale")
    method: Optional[str] = "PUBLISH"
    events: List[CalendarEvent] = Field(default_factory=list)
