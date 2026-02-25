from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from social_scheduler.paths import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS scheduling_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_id TEXT NOT NULL,
    weekday TEXT NOT NULL,
    project_name TEXT NOT NULL,
    platform_name TEXT NOT NULL,
    account_handle TEXT NOT NULL,
    content_path TEXT NOT NULL,
    state TEXT NOT NULL,
    scheduled_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (week_id, weekday, project_name, platform_name, account_handle, content_path)
);
"""


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn


def upsert_schedule_record(
    conn: sqlite3.Connection,
    *,
    week_id: str,
    weekday: str,
    project_name: str,
    platform_name: str,
    account_handle: str,
    content_path: str,
    state: str,
) -> None:
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """
        INSERT INTO scheduling_records (
            week_id, weekday, project_name, platform_name, account_handle,
            content_path, state, scheduled_at, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(week_id, weekday, project_name, platform_name, account_handle, content_path)
        DO UPDATE SET
            state=excluded.state,
            scheduled_at=excluded.scheduled_at,
            updated_at=excluded.updated_at
        """,
        (
            week_id,
            weekday,
            project_name,
            platform_name,
            account_handle,
            content_path,
            state,
            now,
            now,
            now,
        ),
    )
