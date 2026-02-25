from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from social_scheduler.db import get_connection, upsert_schedule_record
from social_scheduler.project_config import load_project_configs
from social_scheduler.weeks import list_weeks


@dataclass
class ScheduleRunResult:
    records_written: int
    skipped_invalid_configs: int


def _is_media_file(path: Path, extensions: list[str]) -> bool:
    return path.is_file() and path.suffix.lower() in set(extensions)


def _detect_state(filename: str, default_state: str) -> str:
    return "published" if "[published]" in filename.lower() else default_state


def run_scheduler() -> ScheduleRunResult:
    config_results = load_project_configs()
    valid_projects = [item.project for item in config_results if item.valid and item.project]
    skipped_invalid = sum(1 for item in config_results if not item.valid)

    records_written = 0
    with get_connection() as conn:
        for week in list_weeks():
            for project in valid_projects:
                assert project is not None
                include_days = set(project.rules.include_days)
                extensions = project.rules.file_extensions

                for weekday in include_days:
                    day_path = week.path / weekday
                    if not day_path.is_dir():
                        continue

                    for media in sorted(day_path.iterdir()):
                        if not _is_media_file(media, extensions):
                            continue

                        state = _detect_state(media.name, project.rules.default_state)

                        for platform in project.platforms:
                            for account in platform.accounts:
                                if not account.enabled:
                                    continue
                                upsert_schedule_record(
                                    conn,
                                    week_id=week.week_id,
                                    weekday=weekday,
                                    project_name=project.project_name,
                                    platform_name=platform.name,
                                    account_handle=account.handle,
                                    content_path=str(media.resolve()),
                                    state=state,
                                )
                                records_written += 1

        conn.commit()

    return ScheduleRunResult(
        records_written=records_written,
        skipped_invalid_configs=skipped_invalid,
    )
