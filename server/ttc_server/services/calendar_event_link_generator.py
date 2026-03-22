from urllib.parse import urlencode

from ttc_core.models.calendar_event import CalendarEvent


class CalendarEventLinkGenerator:
    def __init__(self, event: CalendarEvent):
        self.event = event

    def google(self) -> str:
        params = {
            "action": "TEMPLATE",
            "text": self.event.summary,
            "dates": f"{self.event.dtstart.strftime('%Y%m%dT%H%M%SZ')}/{self.event.dtend.strftime('%Y%m%dT%H%M%SZ')}",
            "details": self.event.description,
            "location": self.event.location,
        }
        # urlencode converts the text and spaces and separates keys with &
        return "https://calendar.google.com/calendar/render?" + urlencode(params)

    def yahoo(self) -> str:
        params = {
            "v": "60",
            "title": self.event.summary,
            "st": self.event.dtstart.strftime("%Y%m%dT%H%M%SZ"),
            "et": self.event.dtend.strftime("%Y%m%dT%H%M%SZ"),
            "desc": self.event.description,
            "in_loc": self.event.location,
        }
        return "https://calendar.yahoo.com/?" + urlencode(params)

    def outlook(self) -> str:
        base_url = "https://outlook.live.com/owa/"
        return self._generate_outlook_url(base_url)

    def office365(self) -> str:
        base_url = "https://outlook.office.com/calendar/0/deeplink/compose"
        return self._generate_outlook_url(base_url)

    def _generate_outlook_url(self, base_url: str) -> str:
        params = {
            "path": "/calendar/action/compose",
            "rru": "addevent",
            "subject": self.event.summary,
            "body": self.event.description,
            "startdt": self.event.dtstart,
            "enddt": self.event.dtend,
            "location": self.event.location,
        }
        return f"{base_url}?{urlencode(params)}"
