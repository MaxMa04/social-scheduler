#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def main() -> int:
    try:
        from social_scheduler.project_config import load_project_configs
    except ModuleNotFoundError as exc:
        print(f"Missing dependency: {exc.name}. Run `bash scripts/setup_local.sh`.")
        return 1

    try:
        results = load_project_configs()
    except RuntimeError as exc:
        print(str(exc))
        return 1

    if not results:
        print("No project configs found.")
        return 0

    invalid = 0
    for result in results:
        if result.valid and result.project:
            print(f"[VALID] {result.path} ({result.project.project_name})")
        else:
            invalid += 1
            print(f"[INVALID] {result.path}: {result.error}")

    print(f"Summary: {len(results) - invalid} valid, {invalid} invalid")
    return 1 if invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())
