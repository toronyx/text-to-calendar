import os

from dotenv import load_dotenv
from ttc_core.file_helper import PROJECT_ROOT


GEMINI_MODEL_NAME = "gemini-2.5-flash"

ICS_PRODID = "-//text-to-calendar//EN"


load_dotenv(PROJECT_ROOT / ".env")  # loads variables from .env into environment


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DOMAIN_NAME = os.getenv("DOMAIN_NAME")
