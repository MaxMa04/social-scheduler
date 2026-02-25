# Local-First Social Scheduler (MVP)

Production-ready MVP for local scheduling workflows on a ThinkPad.

## Features
- Weekly folders with German weekdays: `Montag`..`Sonntag`
- YAML project configs with platform/account metadata (no secrets)
- SQLite-backed local scheduling state
- FastAPI endpoints for health, projects, weeks, archive
- Sunday archive job and daily cleanup job
- Cron template + setup helper

## Project Layout
- `src/` app + domain code
- `scripts/` operational scripts
- `config/projects/*.yaml` project configurations
- `${SOCIAL_SCHEDULER_STORAGE_ROOT}/content/weekly/<YYYY-Www>/{Montag..Sonntag}` weekly working folders
- `${SOCIAL_SCHEDULER_STORAGE_ROOT}/archive/<YYYY-Www>` archived weekly content
- `${SOCIAL_SCHEDULER_STORAGE_ROOT}/state/scheduler.db` local SQLite DB
- `config/cron/crontab.example` cron template

Runtime storage root is controlled by `SOCIAL_SCHEDULER_STORAGE_ROOT` and defaults to `/home/max/social-scheduler-data`.

## Quickstart
```bash
make setup
cp .env.example .env
make create-week
make validate-projects
make schedule
make run-api
```

API runs at `http://127.0.0.1:8000`.

## Script Usage
Create current ISO week scaffold:
```bash
python scripts/create_week.py
```

Create a specific ISO week scaffold:
```bash
python scripts/create_week.py --week 2026-W09
```

Validate project YAML configs:
```bash
python scripts/validate_projects.py
```

Generate scheduling records:
```bash
python scripts/run_scheduler.py
```

Archive a week (default: current week):
```bash
python scripts/archive_week.py --week 2026-W09
```

Cleanup archived folders older than 20 days:
```bash
python scripts/cleanup_archive.py --older-than-days 20
```

## Scheduling State
Scheduler stores records in SQLite table `scheduling_records` with states:
- `queued`: default for discovered media files
- `published`: auto-set when filename contains `[published]`

## Cron Setup
See `config/cron/crontab.example` and adjust `PROJECT_ROOT`, `STORAGE_ROOT`, and `PYTHON` for your machine.

Install the cron template:
```bash
make install-cron
```

## Example Project Config
See `config/projects/example.yaml`.

## Testing
```bash
make test
```
