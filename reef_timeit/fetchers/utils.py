from datetime import datetime


def iso8601_to_datetime(time: str) -> datetime:
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
