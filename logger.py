import sys
from pathlib import Path

from loguru import logger


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def setup_logging():

    logger.remove()

    logger.add(
        sys.stdout,
        level="INFO",
        colorize=True,
        format=(
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "{message}"
        )
    )

    logger.add(
        LOG_DIR / "bot.log",
        level="INFO",
        rotation="10 MB",
        retention="30 days",
        encoding="utf-8",
        serialize=True,
    )

    logger.add(
        LOG_DIR / "errors.log",
        level="ERROR",
        rotation="10 MB",
        retention="30 days",
        encoding="utf-8",
        serialize=True,
    )

    logger.info("Logging initialized")


def log_user_action(
    user_id: int,
    action: str,
    **extra
):

    payload = {
        "user_id": user_id,
        "action": action,
        **extra
    }

    logger.info(payload)


def log_error(error, **extra):

    logger.exception(
        {
            "error": str(error),
            **extra
        }
    )


def get_logger():
    return logger