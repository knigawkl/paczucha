from datetime import datetime
from dateutil import tz

def shift_timezone(d: datetime, from_zone = tz.tzutc(), to_zone = tz.tzlocal()):
    utc = d.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone)
