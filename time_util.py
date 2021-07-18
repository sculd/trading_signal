import datetime
import pytz
from pytz import timezone

_TIMEZONE_US_EAST_STR = 'US/EASTERN'
_TIMEZONE_US_EAST = timezone(_TIMEZONE_US_EAST_STR)

def epoch_seconds_to_et_datetime(timestamp_seconds):
    t = datetime.datetime.utcfromtimestamp(timestamp_seconds)
    t_utc = pytz.utc.localize(t)
    t_tz = t_utc.astimezone(_TIMEZONE_US_EAST)
    return t_tz

def truncate_utc_timestamp_to_minute(timestamp_seconds):
    t_tz = epoch_seconds_to_et_datetime(timestamp_seconds)
    return t_tz.replace(second=0, microsecond=0)

def epoch_seconds_to_str(timestamp_seconds):
    t = datetime.datetime.utcfromtimestamp(timestamp_seconds)
    t_tz = pytz.utc.localize(t)
    return str(t_tz)

def epoch_seconds_to_et_str(timestamp_seconds):
    t_tz = epoch_seconds_to_et_datetime(timestamp_seconds)
    return t_tz.strftime('%Y-%m-%dT%H:%M:%S%Z')

def epoch_seconds_to_et_date_str(timestamp_seconds):
    t_tz = epoch_seconds_to_et_datetime(timestamp_seconds)
    return t_tz.strftime('%Y-%m-%d')
