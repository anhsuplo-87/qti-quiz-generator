import logging
from colorlog import ColoredFormatter

LOG_FORMAT = (
    "%(log_color)s[%(levelname)s]%(reset)s - "
    "%(asctime)s.%(msecs)03d - "
    "%(processName)s: %(message)s"
)

DATE_FORMAT = "%y.%m.%d %H:%M:%S"


def setup_logger(verbose: bool = False) -> logging.Logger:
    """
    Setup root logger for whole application.
    Should be called ONLY ONCE in cli.py
    """

    logger = logging.getLogger("qti_builder")

    # tránh add handler nhiều lần
    if logger.hasHandlers():
        return logger

    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(level)

    formatter = ColoredFormatter(
        LOG_FORMAT,
        datefmt=DATE_FORMAT,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
