from zoneinfo import ZoneInfo

import requests
import streamlit as st
from ttc_client.fastapi_client import FastAPIClient
from ttc_client.helpers import catch_request_errors, get_iana_timezone, random_placeholder
from ttc_core.models.calendar import Calendar
from ttc_core.models.calendar_event import CalendarEvent
from ttc_core.utils.date_utils import format_date_range
from ttc_core.utils.name_utils import random_string
from ttc_server.config import TTC_API_URL


@st.cache_resource
def get_api_client():
    return FastAPIClient(base_url=TTC_API_URL)


client = get_api_client()


def create_ics(calendar_or_event: Calendar | CalendarEvent) -> str:
    if isinstance(calendar_or_event, Calendar):
        endpoint = "calendar_to_ics_file/"
    elif isinstance(calendar_or_event, CalendarEvent):
        endpoint = "calendar_event_to_ics_file/"

    response = catch_request_errors(client.post, endpoint, json=calendar_or_event.model_dump(mode="json"))
    return response.text


st.set_page_config(
    page_title="Text to Calendar",
    page_icon=":calendar:",
    menu_items={
        "About": "Tool to convert plaintext into a calendar event!",
        "Report a Bug": "mailto:dev@taurho.co.uk",
    },
    initial_sidebar_state="collapsed",
)

st.title("📆 Text to Calendar", help="To read more about Text to Calendar, open the sidebar!")

with st.sidebar:
    st.header("Features")
    st.text("When Text to Calendar makes a calendar event, it extracts key info, including:")
    features = ["Event title", "Description", "Start/end time", "Location"]
    st.markdown("- " + "\n- ".join(features))
    st.text("As well as supporting multiple events extracted from a single piece of text!")
    st.markdown("[View on GitHub](https://github.com/toronyx/text-to-calendar/)")

if "placeholder" not in st.session_state:
    st.session_state["placeholder"] = random_placeholder()

user_input = st.text_area(
    "Paste your text below!",
    placeholder=st.session_state["placeholder"],
    help="Paste some text into the box below, and we'll do our best to create a calendar event from it!",
    height="content",
)

iana_timezone = get_iana_timezone()
if st.button("Make it an event", type="primary"):
    if user_input.strip():
        try:
            with st.spinner("Creating your event..."):
                response = catch_request_errors(
                    client.post,
                    "prompt_to_calendar_object/",
                    params={
                        "prompt": user_input,
                        "iana_timezone": iana_timezone,
                    },
                )

            if response:
                st.session_state["calendar"] = Calendar.model_validate(response.json())
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter some event details first.")

if "calendar" in st.session_state:
    try:
        calendar: Calendar = st.session_state["calendar"]
        with st.container(horizontal_alignment="center"):
            for calendar_event in calendar.events:
                col1, col2, col3 = st.columns([2, 5, 3])

                with col2.container(border=True, width="content", horizontal_alignment="left"):
                    st.subheader(str(calendar_event.summary))
                    st.text(str(calendar_event.description), width=300)
                    local_start = calendar_event.dtstart.astimezone(ZoneInfo(iana_timezone))
                    local_end = calendar_event.dtend.astimezone(ZoneInfo(iana_timezone))
                    st.text(f"⏰ {format_date_range(local_start, local_end)}")
                    if calendar_event.location:
                        st.text(f"📍 {calendar_event.location}")
                with col3.container(width="content"):
                    calendar_type = st.selectbox(
                        "Add to calendar",  # collapsed so we don't see this
                        ["Google", "Outlook", "Office365", "Yahoo", "Apple"],
                        label_visibility="collapsed",
                        key=f"{calendar_event.uid}__selectbox",
                    )
                    try:
                        with st.spinner("Getting your link..."):
                            response = catch_request_errors(
                                client.post, "calendar_event_links/", json=calendar_event.model_dump(mode="json")
                            )

                        if response:
                            link_dict: dict = response.json()
                            st.session_state[f"link_dict_{calendar_event.uid}"] = link_dict
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error: {e}")
                    if f"link_dict_{calendar_event.uid}" in st.session_state:
                        link_dict = st.session_state[f"link_dict_{calendar_event.uid}"]
                        link = link_dict.get(calendar_type.lower())
                        if link:
                            st.link_button("Add to calendar", link, type="primary")
                        else:
                            st.download_button(
                                label="Download .ics",
                                data=lambda: create_ics(calendar_event),
                                file_name=f"{random_string()}.ics",
                                mime="text/calendar",
                                type="primary",
                            )

        st.success(
            "Your event is ready! Download and open it to add it to a calendar of your choice,"
            " whether that's Google Calendar, Outlook, iCalendar or whatever else!"
        )

        if st.download_button(
            label="Download Full Calendar (.ics)",
            data=lambda: create_ics(calendar),
            file_name=f"{random_string()}.ics",
            mime="text/calendar",
            type="primary",
        ):
            st.session_state["downloaded"] = True

        if st.session_state.get("downloaded"):
            st.balloons()
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
