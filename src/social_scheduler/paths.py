from __future__ import annotations

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
CONTENT_WEEKLY_DIR = ROOT_DIR / "content" / "weekly"
ARCHIVE_DIR = ROOT_DIR / "archive"
PROJECTS_DIR = ROOT_DIR / "config" / "projects"
STATE_DIR = ROOT_DIR / "state"
DB_PATH = STATE_DIR / "scheduler.db"
