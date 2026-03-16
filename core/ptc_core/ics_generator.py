from datetime import datetime
from typing import Optional

from ptc_core.models.calendar import Calendar
from ptc_core.models.calendar_event import CalendarEvent
from ptc_server.config import ICS_PRODID


def _format_datetime(dt: datetime) -> str:
    # convert to UTC format for iCalendar
    if dt.tzinfo is not None:
        dt = dt.astimezone(tz=None)
    return dt.strftime("%Y%m%dT%H%M%SZ")


def calendar_event_to_ics(event: CalendarEvent) -> str:
    lines = [
        "BEGIN:VEVENT",
        f"UID:{event.uid}",
        f"DTSTAMP:{_format_datetime(event.dtstamp)}",
        f"DTSTART:{_format_datetime(event.dtstart)}",
        f"DTEND:{_format_datetime(event.dtend)}",
        f"SUMMARY:{event.summary}",
        f"DESCRIPTION:{event.description or ''}",
        f"LOCATION:{event.location or ''}",
        f"STATUS:{event.status or 'CONFIRMED'}",
        "END:VEVENT",
    ]
    return "\r\n".join(lines)


def calendar_to_ics(calendar: Calendar) -> str:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:{calendar.prodid}",
        f"CALSCALE:{calendar.calscale}",
    ]
    if calendar.method:
        lines.append(f"METHOD:{calendar.method}")

    for event in calendar.events:
        lines.append(calendar_event_to_ics(event))

    lines.append("END:VCALENDAR")
    return "\r\n".join(lines)
