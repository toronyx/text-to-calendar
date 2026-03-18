from pathlib import Path

import ptc_server
import pytest

from ptc_server.services.llm_service import LLMService, LLMParseError
from ptc_server.mocks.mock_llm_client import MockLLMClient


def test_parse_response_as_json_with_example_model_response():
    example_path = Path(ptc_server.mocks.__path__[0]) / "example_model_response.txt"
    response_text = example_path.read_text(encoding="utf-8")

    service = LLMService(MockLLMClient(""))
    parsed = service._parse_response_as_json(response_text)

    assert parsed["start"] == "20260330T140000Z"
    assert parsed["end"] == "20260330T160000Z"
    assert parsed["summary"] == "Birthday Party"
    assert parsed["description"] == "Come celebrate my birthday!"
    assert parsed["location"] == "London Eye"


def test_convert_json_to_calendar_event_adds_fields_and_parses_datetimes():
    service = LLMService(MockLLMClient(""))
    event_data = {
        "start": "20260330T140000Z",
        "end": "20260330T160000Z",
        "summary": "Birthday Party",
        "description": "Come celebrate my birthday!",
        "location": "London Eye",
    }

    calendar_event = service._convert_json_to_calendar_event(event_data)

    assert calendar_event.summary == "Birthday Party"
    assert calendar_event.description == "Come celebrate my birthday!"
    assert calendar_event.location == "London Eye"
    assert hasattr(calendar_event, "uid")
    assert calendar_event.status == "CONFIRMED"
    assert calendar_event.dtstart.isoformat().startswith("2026-03-30T14:00")
    assert calendar_event.dtend.isoformat().startswith("2026-03-30T16:00")


def test_parse_response_as_json_raises_for_invalid_json():
    service = LLMService(MockLLMClient("not json"))
    with pytest.raises(LLMParseError):
        service._parse_response_as_json("not json")
