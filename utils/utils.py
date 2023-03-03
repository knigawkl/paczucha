"""Utility functions."""
from datetime import datetime
from dateutil import tz

def shift_timezone(event_datetime: datetime, from_zone=tz.tzutc(), to_zone=tz.tzlocal()):
    """Shift datetime from timezone from_zone to timezone to_zone."""
    utc = event_datetime.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)
