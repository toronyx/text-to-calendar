import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from ttc_core.file_helper import PROJECT_ROOT

LOG_FILE = Path(PROJECT_ROOT / "logs" / "server.log")


def setup_logging():
    LOG_FILE.parent.mkdir(exist_ok=True)

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Rotating file handler
    fh = TimedRotatingFileHandler(
        LOG_FILE,
        when="midnight",  # rotate daily
        interval=1,
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(name)
        logger.addHandler(fh)
