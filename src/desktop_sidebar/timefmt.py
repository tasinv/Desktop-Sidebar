from datetime import datetime


def format_time(dt: datetime) -> str:
    """Return 12-hour time with leading zero and lowercase am/pm (e.g. 09:55am)."""
    return dt.strftime("%I:%M%p").lower()


def format_date(dt: datetime) -> str:
    """Return date as DD/MM/YY (e.g. 30/12/26)."""
    return dt.strftime("%d/%m/%y")
