#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from social_scheduler.weeks import create_week_scaffold


def main() -> int:
    parser = argparse.ArgumentParser(description="Create weekly scaffold with German weekdays.")
    parser.add_argument("--week", help="ISO week id, e.g. 2026-W09")
    args = parser.parse_args()

    try:
        week_path = create_week_scaffold(week_id=args.week)
    except ValueError as exc:
        print(str(exc))
        return 1

    print(f"Created/ensured week scaffold: {week_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
