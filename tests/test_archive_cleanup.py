from __future__ import annotations

import os
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from social_scheduler.archive_ops import archive_week, cleanup_archive
from social_scheduler.constants import GERMAN_WEEKDAYS
from social_scheduler.weeks import validate_week_id, week_end_date


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
            old_week = _make_week(archive, "old-folder")
            new_week = _make_week(archive, "new-folder")

            old_ts = (datetime.now() - timedelta(days=25)).timestamp()
            new_ts = (datetime.now() - timedelta(days=5)).timestamp()

            os.utime(old_week, (old_ts, old_ts))
            os.utime(new_week, (new_ts, new_ts))

            removed = cleanup_archive(older_than_days=20, archive_dir=archive)

            self.assertIn(old_week, removed)
            self.assertFalse(old_week.exists())
            self.assertTrue(new_week.exists())

    def test_cleanup_archive_prefers_week_age_over_mtime(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive = tmp_path / "archive"

            old_iso_week = date.today() - timedelta(days=35)
            old_week_id = f"{old_iso_week.isocalendar().year}-W{old_iso_week.isocalendar().week:02d}"
            old_week_dir = _make_week(archive, old_week_id)

            # Simulate a recently touched old folder: mtime would normally protect it.
            recent_ts = (datetime.now() - timedelta(days=1)).timestamp()
            os.utime(old_week_dir, (recent_ts, recent_ts))

            removed = cleanup_archive(older_than_days=20, archive_dir=archive)

            self.assertIn(old_week_dir, removed)
            self.assertFalse(old_week_dir.exists())


class WeekValidationTests(unittest.TestCase):
    def test_validate_week_id_accepts_valid_iso_week(self) -> None:
        self.assertEqual(validate_week_id("2026-W09"), "2026-W09")

    def test_validate_week_id_rejects_invalid_format(self) -> None:
        with self.assertRaises(ValueError):
            validate_week_id("2026-09")

    def test_validate_week_id_rejects_invalid_week_number(self) -> None:
        with self.assertRaises(ValueError):
            validate_week_id("2026-W54")

    def test_week_end_date_returns_sunday(self) -> None:
        self.assertEqual(week_end_date("2026-W09"), date(2026, 3, 1))


if __name__ == "__main__":
    unittest.main()
