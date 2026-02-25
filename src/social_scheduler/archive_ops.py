from __future__ import annotations

import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

from social_scheduler.paths import ARCHIVE_DIR, CONTENT_WEEKLY_DIR
from social_scheduler.weeks import validate_week_id, week_end_date


def archive_week(week_id: str, weekly_dir: Path = CONTENT_WEEKLY_DIR, archive_dir: Path = ARCHIVE_DIR) -> Path:
    validate_week_id(week_id)
    source = weekly_dir / week_id
    destination = archive_dir / week_id

    if not source.exists() or not source.is_dir():
        raise FileNotFoundError(f"week folder not found: {source}")
    if destination.exists():
        raise FileExistsError(f"archive folder already exists: {destination}")

    archive_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))
    return destination


def _older_than_cutoff_by_week_id(week_id: str, cutoff_date: datetime) -> bool:
    try:
        return week_end_date(week_id) < cutoff_date.date()
    except ValueError:
        return False


def cleanup_archive(older_than_days: int = 20, archive_dir: Path = ARCHIVE_DIR) -> list[Path]:
    if older_than_days < 0:
        raise ValueError("older_than_days must be >= 0")

    if not archive_dir.exists():
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=older_than_days)
    removed: list[Path] = []

    for item in sorted(archive_dir.iterdir()):
        if not item.is_dir():
            continue

        remove_dir = _older_than_cutoff_by_week_id(item.name, cutoff)
        if not remove_dir:
            last_modified = datetime.fromtimestamp(item.stat().st_mtime, tz=timezone.utc)
            remove_dir = last_modified < cutoff

        if remove_dir:
            shutil.rmtree(item)
            removed.append(item)

    return removed
