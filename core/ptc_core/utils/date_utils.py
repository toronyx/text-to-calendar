from datetime import datetime


def ordinal(n: int) -> str:
    """
    Return ordinal suffix for a day number.
    """
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def format_nice_date(dt: datetime) -> str:
    """
    e.g. "Monday 16th March 2026"
    """
    return dt.strftime("%A ") + ordinal(dt.day) + dt.strftime(" %B %Y")
