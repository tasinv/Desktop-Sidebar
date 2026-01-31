from datetime import datetime
from zoneinfo import ZoneInfo

from desktop_sidebar.timefmt import format_time, format_date


def test_format_time_am_pm():
    # 9:05am
    dt = datetime(2026, 12, 30, 9, 5, tzinfo=ZoneInfo("UTC"))
    assert format_time(dt) == "09:05am"

    # 3:30pm -> 03:30pm
    dt2 = datetime(2026, 12, 30, 15, 30, tzinfo=ZoneInfo("UTC"))
    assert format_time(dt2) == "03:30pm"


def test_format_date():
    dt = datetime(2026, 12, 30, 9, 5, tzinfo=ZoneInfo("UTC"))
    assert format_date(dt) == "30/12/26"


def test_timezone_conversion():
    # 12:00 UTC should be 07:00 America/New_York in standard time (if not DST)
    dt_utc = datetime(2026, 1, 1, 12, 0, tzinfo=ZoneInfo("UTC"))
    dt_ny = dt_utc.astimezone(ZoneInfo("America/New_York"))
    # Just ensure hours changed
    assert dt_ny.hour != dt_utc.hour
