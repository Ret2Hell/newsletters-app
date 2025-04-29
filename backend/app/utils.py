from datetime import datetime, timedelta, timezone


def get_utc_now():
    return datetime.now(timezone(timedelta(hours=1)))
