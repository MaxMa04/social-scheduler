from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

try:
    import yaml
except ImportError:  # pragma: no cover - dependency check
    yaml = None
from pydantic import ValidationError

from social_scheduler.models import ProjectConfig
from social_scheduler.paths import PROJECTS_DIR


@dataclass
class ConfigValidationResult:
    path: Path
    valid: bool
    project: ProjectConfig | None = None
    error: str | None = None


def load_project_configs(projects_dir: Path = PROJECTS_DIR) -> List[ConfigValidationResult]:
    if yaml is None:
        raise RuntimeError(
            "PyYAML is required. Install dependencies with `bash scripts/setup_local.sh`."
        )

    results: List[ConfigValidationResult] = []
    if not projects_dir.exists():
        return results

    for path in sorted(projects_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("YAML root must be a mapping/object")
            project = ProjectConfig.model_validate(data)
            results.append(ConfigValidationResult(path=path, valid=True, project=project))
        except (yaml.YAMLError, ValidationError, ValueError) as exc:
            results.append(ConfigValidationResult(path=path, valid=False, error=str(exc)))

    return results
