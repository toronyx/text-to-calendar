import random
from streamlit_javascript import st_javascript


def random_placeholder():
    # lower number means more likely
    placeholders = {
        "e.g. take the dog for a walk this evening...": 1,
        "e.g. coffee with lissie tomorrow at 4, and then drinks at 6...": 1,
        "e.g. head to London Paddington for 11am...": 1,
        # "e.g. yoga class every thursday at 9am...": 1, # TODO 18-Mar-2026 we don't support recurrence yet!
        "e.g. dentist appointment at 2:30 next monday...": 1,
        "e.g. feed the cat tomorrow morning, and in the evening...": 1,
        "e.g. go for a run in 30 mins...": 2,
        "e.g. destroy the one ring at Mount Doom next week...": 5,
        "e.g. take over the world from my evil lair on friday afternoon...": 5,
        "e.g. take charlie for a tour of my chocolate factory later today...": 1000,
    }

    items = list(placeholders.keys())
    inverted_weights = [1 / w for w in list(placeholders.values())]
    return random.choices(items, weights=inverted_weights, k=1)[0]


def get_iana_timezone() -> str:
    """
    e.g. America/New_York
    """
    return st_javascript("Intl.DateTimeFormat().resolvedOptions().timeZone")
