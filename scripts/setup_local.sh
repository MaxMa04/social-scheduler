#!/usr/bin/env bash
set -euo pipefail

STORAGE_ROOT="${SOCIAL_SCHEDULER_STORAGE_ROOT:-/home/max/social-scheduler-data}"

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]

mkdir -p "$STORAGE_ROOT/content/weekly" "$STORAGE_ROOT/archive" "$STORAGE_ROOT/state"

echo "Setup complete. Activate with: source .venv/bin/activate"
