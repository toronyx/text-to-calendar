from datetime import datetime
from pathlib import Path

from ptc_core.ics_generator import calendar_to_ics
from ptc_core.models.calendar import Calendar
from ptc_core.models.calendar_event import CalendarEvent


def test_calendar_to_ics_matches_fixture():
    event = CalendarEvent(
        uid="1@example.com",
        dtstamp=datetime(2026, 3, 16, 12, 0, 0),
        dtstart=datetime(2026, 3, 30, 14, 0, 0),
        dtend=datetime(2026, 3, 30, 16, 0, 0),
        summary="Birthday Party",
        description="Come celebrate my birthday!",
        location="London Eye",
        status="CONFIRMED",
    )
    calendar = Calendar(prodid="-//test//EN", method=None, events=[event])
    output = calendar_to_ics(calendar, prodid="-//test//EN")

    expected_path = Path(__file__).resolve().parents[0] / "fixtures" / "example_calendar.ics"
    expected = expected_path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
    assert output.replace("\r\n", "\n").strip() == expected
