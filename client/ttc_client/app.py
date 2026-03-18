from ttc_client.helpers import random_placeholder
from ttc_core.models.calendar import Calendar
from ttc_core.utils.date_utils import format_date_range
import streamlit as st
import requests
from ttc_core.utils.name_utils import random_string
from ttc_server.config import TTC_API_URL


@st.cache_data
def create_ics_from_calendar(calendar: Calendar) -> str:
    response = requests.post(f"{TTC_API_URL}/calendar_to_ics_file/", json=calendar.model_dump(mode="json"))
    response.raise_for_status()
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

st.sidebar.header("Features")
st.sidebar.text("When Text to Calendar makes a calendar event, it extracts all kind of useful info, including:")
features = ["Event title", "Description", "Start/end time", "Location"]
st.sidebar.markdown("- " + "\n- ".join(features))
st.sidebar.text("As well as supporting multiple events extracted from a single piece of text!")

if "placeholder" not in st.session_state:
    st.session_state["placeholder"] = random_placeholder()
user_input = st.text_area("Paste your text below!", placeholder=st.session_state["placeholder"], height="content")

if st.button("Convert to Calendar", type="primary"):
    if user_input.strip():
        try:
            with st.spinner("Creating your event..."):
                response = requests.post(f"{TTC_API_URL}/prompt_to_calendar_object/", params={"prompt": user_input})
            response.raise_for_status()

            calendar = Calendar.model_validate(response.json())

            st.session_state["calendar"] = calendar
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter some event details first.")

if "calendar" in st.session_state:
    try:
        calendar: Calendar = st.session_state["calendar"]
        with st.container(horizontal_alignment="center"):
            for calendar_event in calendar.events:
                with st.container(border=True, width="content", horizontal_alignment="left"):
                    st.subheader(str(calendar_event.summary))
                    st.text(str(calendar_event.description), width=400)
                    st.text("⏰ " + f"{format_date_range(calendar_event.dtstart, calendar_event.dtend)}")
                    if calendar_event.location:
                        st.text("📍 " + str(calendar_event.location))

        if st.download_button(
            label="Download ICS File",
            data=lambda: create_ics_from_calendar(calendar),
            file_name=f"{random_string()}.ics",
            mime="text/calendar",
            type="primary",
        ):
            st.session_state["downloaded"] = True

        if st.session_state.get("downloaded"):
            st.balloons()
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
