from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime


class CalendarEvent(BaseModel):
    uid: str = Field(..., description="Unique identifier for the event")
    dtstamp: datetime = Field(..., description="Timestamp when the event object was created")
    dtstart: datetime = Field(..., description="Event start datetime")
    dtend: datetime = Field(..., description="Event end datetime")
    summary: str = Field(..., description="Short title of the event")
    description: Optional[str] = Field(None, description="Long description of the event")
    location: Optional[str] = Field(None, description="Event location")
    status: Optional[str] = Field("CONFIRMED", description="Event status")
