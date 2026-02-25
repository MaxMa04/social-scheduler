#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from social_scheduler.archive_ops import archive_week
from social_scheduler.weeks import current_week_id


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive weekly content folder.")
    parser.add_argument("--week", help="ISO week id to archive (default: current week)")
    args = parser.parse_args()

    week_id = args.week or current_week_id()
    destination = archive_week(week_id=week_id)
    print(f"Archived {week_id} to {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
