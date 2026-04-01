<!-- omit in toc --> 
# Text to Calendar

Test it out at [text-to-calendar.taurho.co.uk](https://text-to-calendar.taurho.co.uk)

Basic idea: throw in some plain text, an LLM will take a look, pull the information into a standard `iCalendar` format, and allow you to apply it to a calendar of your choosing.

<photos/videos>

<!-- omit in toc --> 
### Table of contents

- [Why I made it](#why-i-made-it)
- [How it works](#how-it-works)
  - [Features](#features)
    - [Features not yet supported](#features-not-yet-supported)
  - [Tech stack](#tech-stack)
  - [Architecture and Design](#architecture-and-design)
  - [Deployment](#deployment)
  - [The iCalendar format](#the-icalendar-format)
- [TODO: Getting started](#todo-getting-started)
- [TODO: Extensions](#todo-extensions)
- [License](#license)
- [Appendix](#appendix)
  - [Folder structure](#folder-structure)

## Why I made it

Gmail used to have a nifty feature (and maybe still does?) where if you get an email from, say, Trainline, with some train tickets attached, Google would extract those train times and add it straight to your calendar. I have no idea what happened to it.

I love my calendar, and anyone who knows me knows I have EVERYTHING on it, from going to work down to brushing my teeth. So sometimes, I'm going to something and I have this big wall of text about it and I want to add it to my calendar. Usually I would just meticulously put in the information myself, but eventually I decided to make this! Throw in some messy text, get nice tidy calendar events out.

## How it works

So, you paste some text in to the box, press the button, and it'll produce one or multiple calendar events ready to be added to major calendar providers. The events can either be added directly, per-event, or you can download an `.ics` file that contains all the events.

### Features

- Key info about the event(s) will be extracted from the text and shown to the user:
   - Title
   - Description (optional)
   - Start time
   - End time
   - Location (optional)
 - If the text describes multiple events, e.g. an outbound and return train journey, multiple events will be extracted .
 - Each event can be added to any major online calendar provider (Google, Outlook, Apple) with the press of a button.
 - All events can be downloaded as a single `.ics` file, compatible with all major calendar providers.

#### Features not yet supported

 - All day events
 - Recurring events (e.g. weekly, daily)
 - Invitees
 - Support for different timezones

### Tech stack

This app is built in Python, with a FastAPI backend, and Streamlit frontend. The environment is managed with `poetry`. The backend makes calls to Gemini with the `google-genai` package, but the project has been designed such that the LLM is entirely swappable, but more on that in a moment.

It's hosted on a Virtual Machine running Ubuntu with a Caddy reverse proxy. But more on the deployment [later](#deployment).

### Architecture and Design

This app probably didn't _need_ FastAPI at all, it could've easily been a pure Streamlit app, wired straight into the business logic. But for the sake of getting into good development habits, this project is divided into `client` and `server` modules, which both depend on a `core` module for shared models and utilities.

As mentioned earlier, the `client` module (the frontend), is a Streamlit app, which makes `http` requests to the `server` (the backend), which is a FastAPI server.
Setting it up this way makes the two nicely decoupled, meaning you could theoretically scale them independently, and/or deploy them separately. In fact, if multiple people connect to the website at once, Streamlit will have them in separate _sessions_, but the way I've set this up, there will only be **one** FastAPI server.

The backend server makes requests to a generic `LLMClient` which is theoretically anything that takes a prompt and produces a text response; but currently it's a `GeminiClient`, which wraps Google's `google-genai` Python package.

The core logic in this app is that the user-inputted text is passed to an LLM, which is asked to produce a `json` object for each event it sees, with information such as title, start time and end time. The LLM is also passed the current date and time so it can infer info from text such as "5 mins from now". Some basic text parsing is used to interpret the LLM output and ensure it's valid `json`, which is then converted to a Pydantic model containing the info required of an event in the `iCalendar` standard.

Of course not **all** this info is provided by the LLM, `iCalendar` events include all sorts of metadata, for example time of creation, time zone etc. which the app fills in separately. The Pydantic model containing all the event info is then ready for conversion into any desired format. First it's shown on the frontend UI, and then, depending on how the user chooses to interact, it might be converted to a Google Calendar format, or served directly as an `.ics` file.

### Deployment

Originally I deployed this via Render's free tier, but I found the 45s spin up time too annoying for an app that's meant to be quick to use, so after messing around with a few ideas including self hosting from my computer (probably needlessly dangerous), I've instead hosted this on an online VM running Ubuntu. The frontend and backend are run as separate services, but the frontend is the only bit directly exposed, via a Caddy reverse proxy. In this setup, the backend FastAPI server is only communicated with locally, since everything is running on one machine.

My domain DNS records are configured to point to my VM, and the Caddy reverse proxy directs requests under a certain sub-address to this app.

### The iCalendar format

This project is made sooo much easier thanks to the standard `iCalendar` format:
https://icalendar.org/RFC-Specifications/iCalendar-RFC-5545/

`iCalendar` describes a standard format for events thats compatible with all major (and most minor) calendar providers; things like start time, end time, title, description, invitees, etc. Any event can be written to a standard `.ics` file format which can be consumed by Outlook, Apple, Google etc.

Some calendar providers, such as those by Microsoft, Google and Yahoo, also support their own easy way of representing an event without an `ics` file. They each have their own hyperlink format , e.g.

```
https://calendar.google.com/calendar/render?action=TEMPLATE&text=EVENT_TITLE&dates=START/END&details=DESCRIPTION&location=LOCATION
```

Opening one of these immediately creates a calendar event with the given fields already populated with those initial values. Look, [try opening this one](https://calendar.google.com/calendar/render?action=TEMPLATE&text=EVENT_TITLE&dates=START/END&details=DESCRIPTION&location=LOCATION). This is what allows for the "Add to Calendar" button - we simply generate a link with the correct information and it'll immediately open the event creation screen.

## TODO: Getting started 

TODO: How to run, and use.

## TODO: Extensions

## License

This project uses the Apache 2.0 license - see details in the LICENSE file.

## Appendix

### Folder structure

This project is separated into 3 main modules to reduce coupling.
The below is not an exhaustive or necessarily up-to-date structure, but indicates the rough structural motivation.

```
text-to-calendar/
├── README.md
├── .env
├── pyproject.toml
├── client/                     # Streamlit frontend
│   └── ttc_client/
│       ├── app.py
│       ...
│
├── core/                       # Shared models / types
│   └── ttc_core/
│       ├── models/
│       │   └── calendar.py
│       ...
│
├── server/                     # FastAPI backend
│   └── ttc_server/
│       ├── main.py
│       ├── routes/
│       │   └── endpoints.py
│       ├── services/
│       │   ├── event_service.py
│       │   └── ics_generator.py
│       ├── clients/
│       │   └── google_genai_client.py
│       ...
│
└── tests/
    ├── test_event_service.py
    └── test_ics_generator.py
```
