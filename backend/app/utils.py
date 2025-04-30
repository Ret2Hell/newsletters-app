from datetime import datetime, timedelta, timezone

from app.config import settings


def get_utc_now():
    """
    Get current datetime with the configured timezone offset.

    This function creates a timezone-aware datetime object using the
    TIMEZONE_OFFSET defined in the application settings. This ensures
    consistent datetime handling across the application.

    Returns:
        datetime: Current datetime with the configured timezone
    """
    return datetime.now(timezone(timedelta(hours=settings.TIMEZONE_OFFSET)))
