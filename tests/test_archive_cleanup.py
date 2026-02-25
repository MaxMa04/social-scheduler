from __future__ import annotations

import os
import unittest
from datetime import datetime, timedelta
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from social_scheduler.archive_ops import archive_week, cleanup_archive
from social_scheduler.constants import GERMAN_WEEKDAYS


def _make_week(base: Path, week_id: str) -> Path:
    week = base / week_id
    week.mkdir(parents=True)
    for day in GERMAN_WEEKDAYS:
        (week / day).mkdir()
    (week / "Montag" / "video.mp4").write_text("x", encoding="utf-8")
    return week


class ArchiveCleanupTests(unittest.TestCase):
    def test_archive_week_moves_folder(self) -> None:
        with self.subTest("move folder"):
            from tempfile import TemporaryDirectory

            with TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                weekly = tmp_path / "content" / "weekly"
                archive = tmp_path / "archive"
                week_id = "2026-W09"

                source_week = _make_week(weekly, week_id)
                destination = archive_week(week_id=week_id, weekly_dir=weekly, archive_dir=archive)

                self.assertFalse(source_week.exists())
                self.assertTrue(destination.exists())
                self.assertTrue((destination / "Montag" / "video.mp4").exists())

    def test_cleanup_archive_removes_only_old_directories(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive = tmp_path / "archive"
            old_week = _make_week(archive, "2026-W01")
            new_week = _make_week(archive, "2026-W02")

            old_ts = (datetime.now() - timedelta(days=25)).timestamp()
            new_ts = (datetime.now() - timedelta(days=5)).timestamp()

            os.utime(old_week, (old_ts, old_ts))
            os.utime(new_week, (new_ts, new_ts))

            removed = cleanup_archive(older_than_days=20, archive_dir=archive)

            self.assertIn(old_week, removed)
            self.assertFalse(old_week.exists())
            self.assertTrue(new_week.exists())


if __name__ == "__main__":
    unittest.main()
