import datetime
from typing import Tuple


MAGIC_WORDS = (
    "now",
    "week start",
    "this week start",
    "this week end",
    "week end",
    "this week end",
    "current week end",
    "next week start",
    "next week end",
    "last week start",
    "last week end",
    "last month start",
    "last month end",
    "2 weeks ago start",
    "2 weeks ago end",
)


def _datetime_from_string_or_magic_words(
    time_str: str | datetime.datetime | None,
) -> datetime.datetime:
    """Helper function to convert string magic words to datetime.

    Args:
        time_str: string of magic words like "last week start" or "last month start"

    Returns:
        datetime.datetime
    """
    if isinstance(time_str, str) is False:
        return time_str

    time_str = time_str.lower()

    if time_str == "now":
        return datetime.datetime.now(tz=datetime.timezone.utc)
    if time_str in ("week start", "this week start", "current week start"):
        now = datetime.datetime.now(datetime.timezone.utc)
        start_of_week = now - datetime.timedelta(days=now.weekday())
        return start_of_week
    if time_str in ("week end", "this week end", "current week end"):
        now = datetime.datetime.now(datetime.timezone.utc)
        start_of_week = now - datetime.timedelta(days=6 - now.weekday())
        return start_of_week
    if time_str == "next week start":
        seven_days_ahead = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(days=7)
        start_of_week = seven_days_ahead - datetime.timedelta(
            days=seven_days_ahead.weekday()
        )
        return start_of_week
    if time_str == "next week end":
        seven_days_ahead = datetime.datetime.now(
            datetime.timezone.utc
        ) + datetime.timedelta(days=7)
        end_of_week = seven_days_ahead + datetime.timedelta(
            days=6 - seven_days_ahead.weekday()
        )
        return end_of_week
    if time_str == "last week start":
        seven_days_ago = datetime.datetime.now(
            datetime.timezone.utc
        ) - datetime.timedelta(days=7)
        start_of_week = seven_days_ago - datetime.timedelta(
            days=seven_days_ago.weekday()
        )
        return start_of_week
    if time_str == "last week end":
        seven_days_ago = datetime.datetime.now(
            datetime.timezone.utc
        ) - datetime.timedelta(days=7)
        end_of_week = seven_days_ago + datetime.timedelta(
            days=6 - seven_days_ago.weekday()
        )
        return end_of_week
    if time_str == "last month start":
        one_month_ago = datetime.datetime.now(
            datetime.timezone.utc
        ) - datetime.timedelta(days=30)
        start_of_month = one_month_ago - datetime.timedelta(days=one_month_ago.day - 1)
        return start_of_month
    if time_str == "last month end":
        one_month_ago = datetime.datetime.now(
            datetime.timezone.utc
        ) - datetime.timedelta(days=30)
        end_of_month = one_month_ago + datetime.timedelta(days=30 - one_month_ago.day)
        return end_of_month
    if time_str == "2 weeks ago start":
        two_weeks_ago = datetime.datetime.now(
            datetime.timezone.utc
        ) - datetime.timedelta(days=14)
        start_of_two_weeks = two_weeks_ago - datetime.timedelta(
            days=two_weeks_ago.weekday()
        )
        return start_of_two_weeks
    if time_str == "2 weeks ago end":
        two_weeks_ago = datetime.datetime.now(
            datetime.timezone.utc
        ) - datetime.timedelta(days=14)
        end_of_two_weeks = two_weeks_ago + datetime.timedelta(
            days=13 - two_weeks_ago.weekday()
        )
        return end_of_two_weeks

    # if time_str is a datetime, return it
    return datetime.datetime.strptime(time_str.replace("Z", ""), "%Y-%m-%dT%H:%M:%S")


def convert_strings_to_datetime(
    time_min: str | datetime.datetime | None, time_max: str | datetime.datetime | None
) -> Tuple[datetime.datetime, datetime.datetime]:
    """Helper function to convert string timestamps to datetime for comparison.

    Args:
        time_min: Optional start time in ISO format (e.g. "2025-02-20T10:00:00Z") or datetime.datetime
        time_max: Optional end time in ISO format (e.g. "2025-02-20T10:00:00Z") or datetime.datetime

    Returns:
        time_min_dt: datetime.datetime
        time_max_dt: datetime.datetime
    """
    if time_min is None:
        seven_days_ago = datetime.datetime.now(
            datetime.timezone.utc
        ) - datetime.timedelta(days=7)
        time_min = seven_days_ago
    if time_max is None:
        time_max = datetime.datetime.now(datetime.timezone.utc)
    if isinstance(time_min, str):
        try:
            time_min = _datetime_from_string_or_magic_words(time_min)
        except:
            time_min = datetime.datetime.now(datetime.timezone.utc)
    if isinstance(time_max, str):
        try:
            time_max = _datetime_from_string_or_magic_words(time_max)
        except:
            time_max = None

    if time_min >= time_max:
        time_max = None
    return time_min, time_max
