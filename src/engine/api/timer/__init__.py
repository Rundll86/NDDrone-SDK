from datetime import datetime

from engine.api.timer.constants import TIME_FORMAT


def now():
    return format(datetime.now())


def format(dt: datetime) -> str:
    return dt.strftime(TIME_FORMAT)
