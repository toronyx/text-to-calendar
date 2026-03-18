# Text to Calendar

## Idea

Throw in some plain text, an LLM will take a look, pull the information into an `.ics` file, and allow you to download it and apply it to a calendar of your choosing.

## Architecture

FastAPI backend with a Streamlit frontend. Probably just hosted as a web server on my laptop but possibly look into proper persistent hosting.

### Rough folder structure

Separated into 3 main folders to reduce coupling

```
text-to-calendar/
├── README.md
├── .env
├── pyproject.toml
├── client/                     # Streamlit frontend
│   └── ttc_client/
│       └── app.py
│
├── core/                       # Shared models / types
│   └── ttc_core/
│       └── models/
│           └── calendar.py
│
├── server/                     # FastAPI backend
│   └── ttc_server/
│       ├── main.py
│       ├── routes/
│       │   └── endpoints.py
│       ├── services/
│       │   ├── event_service.py
│       │   └── ics_generator.py
│       └── clients/
│           └── google_genai_client.py
│
└── tests/                      # Can include unit tests for core and backend
    ├── test_event_service.py
    └── test_ics_generator.py
```
