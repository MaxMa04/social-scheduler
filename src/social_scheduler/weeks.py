from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import List

from social_scheduler.constants import GERMAN_WEEKDAYS
from social_scheduler.paths import CONTENT_WEEKLY_DIR


@dataclass
class WeekInfo:
    week_id: str
    path: Path
    weekdays: List[str]


WEEK_ID_PATTERN = re.compile(r"^(\d{4})-W(\d{2})$")


def current_week_id(reference_date: date | None = None) -> str:
    ref = reference_date or date.today()
    iso = ref.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def parse_week_id(week_id: str) -> tuple[int, int]:
    match = WEEK_ID_PATTERN.fullmatch(week_id)
    if not match:
        raise ValueError("week must match ISO format YYYY-Www (e.g. 2026-W09)")

    year = int(match.group(1))
    week = int(match.group(2))
    try:
        date.fromisocalendar(year, week, 1)
    except ValueError as exc:
        raise ValueError(f"invalid ISO week: {week_id}") from exc

    return year, week


def validate_week_id(week_id: str) -> str:
    parse_week_id(week_id)
    return week_id


def week_start_date(week_id: str) -> date:
    year, week = parse_week_id(week_id)
    return date.fromisocalendar(year, week, 1)


def week_end_date(week_id: str) -> date:
    return week_start_date(week_id) + timedelta(days=6)


def create_week_scaffold(week_id: str | None = None, base_dir: Path = CONTENT_WEEKLY_DIR) -> Path:
    week = validate_week_id(week_id) if week_id else current_week_id()
    week_path = base_dir / week
    week_path.mkdir(parents=True, exist_ok=True)
    for day in GERMAN_WEEKDAYS:
        (week_path / day).mkdir(exist_ok=True)
    return week_path


def list_weeks(base_dir: Path = CONTENT_WEEKLY_DIR) -> List[WeekInfo]:
    if not base_dir.exists():
        return []

    items: List[WeekInfo] = []
    for week_path in sorted([p for p in base_dir.iterdir() if p.is_dir()]):
        weekdays = [day for day in GERMAN_WEEKDAYS if (week_path / day).is_dir()]
        items.append(WeekInfo(week_id=week_path.name, path=week_path, weekdays=weekdays))
    return items
