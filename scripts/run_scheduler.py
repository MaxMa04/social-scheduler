#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def main() -> int:
    try:
        from social_scheduler.scheduler import run_scheduler
    except ModuleNotFoundError as exc:
        print(f"Missing dependency: {exc.name}. Run `bash scripts/setup_local.sh`.")
        return 1

    try:
        result = run_scheduler()
    except RuntimeError as exc:
        print(str(exc))
        return 1

    print(
        f"Scheduler completed: records_written={result.records_written}, "
        f"skipped_invalid_configs={result.skipped_invalid_configs}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
