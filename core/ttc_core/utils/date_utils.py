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


def format_nice_time(dt: datetime) -> str:
    """
    e.g. 7:00pm
    """
    return dt.strftime("%I:%M%p").lower().lstrip("0")


def format_date_range(start: datetime, end: datetime) -> str:
    if start.date() == end.date():
        # Monday 16th March 2026 7:00pm - 9:00pm
        return format_nice_date(start) + f", {format_nice_time(start)} - {format_nice_time(end)}"
    else:
        # 16th March 2026, 7:00pm - 21st March 2026, 9:00pm
        return f"{ordinal(start.day)} {start.strftime('%B %Y')}, {format_nice_time(start)} - {ordinal(end.day)} {end.strftime('%B %Y')}, {format_nice_time(end)}"
