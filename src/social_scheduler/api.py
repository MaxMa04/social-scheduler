from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI

from social_scheduler.paths import ARCHIVE_DIR
from social_scheduler.project_config import load_project_configs
from social_scheduler.weeks import list_weeks

app = FastAPI(title="Local Social Scheduler MVP", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/projects")
def projects() -> dict[str, list[dict[str, object]]]:
    try:
        results = load_project_configs()
    except RuntimeError as exc:
        return {"projects": [{"valid": False, "error": str(exc)}]}

    items = []
    for result in results:
        if result.valid and result.project:
            items.append(
                {
                    "path": str(result.path),
                    "valid": True,
                    "project": result.project.model_dump(),
                }
            )
        else:
            items.append(
                {
                    "path": str(result.path),
                    "valid": False,
                    "error": result.error,
                }
            )
    return {"projects": items}


@app.get("/weeks")
def weeks() -> dict[str, list[dict[str, object]]]:
    return {
        "weeks": [
            {
                "week_id": week.week_id,
                "path": str(week.path),
                "weekdays": week.weekdays,
            }
            for week in list_weeks()
        ]
    }


@app.get("/archive")
def archive() -> dict[str, list[dict[str, object]]]:
    archived = []
    if ARCHIVE_DIR.exists():
        for path in sorted(ARCHIVE_DIR.iterdir()):
            if path.is_dir():
                archived.append(
                    {
                        "week_id": path.name,
                        "path": str(path),
                        "last_modified": datetime.fromtimestamp(
                            path.stat().st_mtime, tz=timezone.utc
                        ).isoformat(),
                    }
                )
    return {"archive": archived}
