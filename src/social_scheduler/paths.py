from __future__ import annotations

import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_STORAGE_ROOT = Path("/home/max/social-scheduler-data")
STORAGE_ROOT = Path(
    os.getenv("SOCIAL_SCHEDULER_STORAGE_ROOT", str(DEFAULT_STORAGE_ROOT))
).expanduser()

CONTENT_WEEKLY_DIR = STORAGE_ROOT / "content" / "weekly"
ARCHIVE_DIR = STORAGE_ROOT / "archive"
PROJECTS_DIR = ROOT_DIR / "config" / "projects"
STATE_DIR = STORAGE_ROOT / "state"
DB_PATH = STATE_DIR / "scheduler.db"
