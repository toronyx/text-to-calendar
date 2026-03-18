from datetime import datetime
import json
import uuid

from ttc_core.models.calendar import Calendar
from ttc_core.models.calendar_event import CalendarEvent
from ttc_core.utils.date_utils import format_nice_date, format_nice_time
from ttc_server.clients.llm.llm_client import LLMClient
from ttc_server.config import DOMAIN_NAME


class LLMParseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class LLMService:
    def __init__(self, client: LLMClient):
        self.client = client

    def calendar_events_from_prompt(self, prompt: str) -> list[CalendarEvent]:
        llm_prompt = f"""
        Convert the following natural language into a JSON calendar event with these fields:
        start, end, summary, description, location.
        start and end should be in compact UTC format: YYYYMMDDTHHMMSSZ
        If the text is describing multiple events, return a list of JSON objects.
        Format everything exactly as JSON. Here is the input:

        {prompt}

        And for reference it is currently {format_nice_date(datetime.now())}, {format_nice_time(datetime.now())}
        """

        output_text = self.client.get_model_response(llm_prompt)
        event_data = self._parse_response_as_json(output_text)
        if isinstance(event_data, dict):
            event_data = [event_data]
        return self._convert_json_to_calendar_events(event_data)

    def _parse_response_as_json(self, output_text: str) -> dict | list[dict]:
        is_list = "[" in output_text and "]" in output_text
        try:
            if is_list:
                json_output = "[" + output_text.split("[")[1].split("]")[0] + "]"
            else:
                json_output = "{" + output_text.split("{")[1].split("}")[0] + "}"
            json_data = json.loads(json_output)
        except json.JSONDecodeError, IndexError:
            raise LLMParseError(f"LLM returned invalid JSON: {output_text}")
        return json_data

    def _convert_json_to_calendar_events(self, json_data: list[dict]) -> list[CalendarEvent]:
        output_list = []
        for element in json_data:
            output_list.append(self._convert_json_to_calendar_event(element))
        return output_list

    def _convert_json_to_calendar_event(self, json_data: dict) -> CalendarEvent:
        json_data["uid"] = f"{uuid.uuid4()}@{DOMAIN_NAME}"
        json_data["dtstamp"] = datetime.now()
        json_data["status"] = "CONFIRMED"

        if "start" not in json_data or "end" not in json_data:
            raise LLMParseError("LLM JSON must include start and end")

        for key in ("start", "end"):
            if isinstance(json_data.get(key), str):
                json_data["dt" + key] = datetime.strptime(json_data[key], "%Y%m%dT%H%M%SZ")
                del json_data[key]

        # TODO 16-Mar-2026 - maybe if no dtend, just default to 1 hr?

        return CalendarEvent(**json_data)
