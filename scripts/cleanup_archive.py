#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from social_scheduler.archive_ops import cleanup_archive


def main() -> int:
    parser = argparse.ArgumentParser(description="Cleanup archived folders older than N days.")
    parser.add_argument("--older-than-days", type=int, default=20)
    args = parser.parse_args()

    removed = cleanup_archive(older_than_days=args.older_than_days)
    print(f"Removed {len(removed)} archived week folder(s).")
    for item in removed:
        print(f" - {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
