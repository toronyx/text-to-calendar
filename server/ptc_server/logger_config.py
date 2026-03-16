import logging
from pathlib import Path

LOG_FILE = Path("logs/prompt-to-calendar.log")

def setup_logging():
    LOG_FILE.parent.mkdir(exist_ok=True)

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    ch.setFormatter(ch_formatter)
    logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(logging.INFO)
    fh.setFormatter(ch_formatter)
    logger.addHandler(fh)