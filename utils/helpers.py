"""
Helper utility functions for ExamOpt
"""
import re
from datetime import datetime
from typing import Optional


def validate_time_format(time_str: str) -> bool:
    """Validates HH:MM in 24-hour format."""
    if not isinstance(time_str, str):
        return False
    match = re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", time_str.strip())
    return bool(match)


def validate_date_format(date_str: str) -> bool:
    """Validates YYYY-MM-DD format."""
    if not isinstance(date_str, str):
        return False
    try:
        datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return True
    except ValueError:
        return False


def format_time(time_str: str) -> str:
    """Formats HH:MM string to readable 12-hour AM/PM string."""
    try:
        dt = datetime.strptime(time_str.strip(), "%H:%M")
        return dt.strftime("%I:%M %p")
    except Exception:
        return time_str
