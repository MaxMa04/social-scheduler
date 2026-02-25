from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import List

from social_scheduler.constants import GERMAN_WEEKDAYS
from social_scheduler.paths import CONTENT_WEEKLY_DIR


@dataclass
class WeekInfo:
    week_id: str
    path: Path
    weekdays: List[str]


def current_week_id(reference_date: date | None = None) -> str:
    ref = reference_date or date.today()
    iso = ref.isocalendar()
    return f"{iso.year}-W{iso.week:02d}"


def create_week_scaffold(week_id: str | None = None, base_dir: Path = CONTENT_WEEKLY_DIR) -> Path:
    week = week_id or current_week_id()
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
