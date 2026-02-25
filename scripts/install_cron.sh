#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CRON_FILE="$ROOT_DIR/config/cron/crontab.example"

crontab "$CRON_FILE"
echo "Installed cron template from $CRON_FILE"
