from datetime import datetime, timedelta, timezone

from app.config import settings


def get_utc_now():
    return datetime.now(timezone(timedelta(hours=settings.TIMEZONE_OFFSET)))
