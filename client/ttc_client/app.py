from ttc_core.models.calendar_event import CalendarEvent
from ttc_core.utils.date_utils import format_date_range
import streamlit as st
import requests
from streamlit.string_util import to_snake_case
from ttc_server.config import TTC_API_URL


@st.cache_data
def create_ics_from_event(event: CalendarEvent) -> str:
    response = requests.post(f"{TTC_API_URL}/calendar_event_to_ics_file/", json=event.model_dump(mode="json"))
    response.raise_for_status()
    return response.text


st.set_page_config(
    page_title="Text to Calendar",
    page_icon=":calendar:",
    menu_items={
        "About": "Tool to convert plaintext into a calendar event!",
        "Report a Bug": "mailto:dev@taurho.co.uk",
    },
)

st.title("📆 Text to Calendar")

user_input = st.text_area(
    "Paste your text below!", placeholder="e.g. take the dog for a walk this evening...", height=150
)

if st.button("Convert to Calendar", type="primary"):
    if user_input.strip():
        try:
            with st.spinner("Creating your event..."):
                response = requests.post(
                    f"{TTC_API_URL}/prompt_to_calendar_event_object/", params={"prompt": user_input}
                )
            response.raise_for_status()

            calendar_event = CalendarEvent.model_validate(response.json())

            st.session_state["calendar_event"] = calendar_event
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter some event details first.")

if "calendar_event" in st.session_state:
    try:
        calendar_event: CalendarEvent = st.session_state["calendar_event"]
        with st.container(horizontal_alignment="center"):
            with st.container(border=True, width="content", horizontal_alignment="left"):
                st.subheader(calendar_event.summary)
                st.text(calendar_event.description, width=400)
                st.text("⏰ " + f"{format_date_range(calendar_event.dtstart, calendar_event.dtend)}")
                st.text("📍 " + calendar_event.location)

        if st.download_button(
            label="Download ICS File",
            data=lambda: create_ics_from_event(calendar_event),
            file_name=f"event_{to_snake_case(calendar_event.summary)}.ics",  # TODO 18-Mar-2026 randomize this name!
            mime="text/calendar",
            type="primary",
        ):
            st.session_state["downloaded"] = True

        if st.session_state.get("downloaded"):
            st.balloons()
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
