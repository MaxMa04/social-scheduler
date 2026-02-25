from __future__ import annotations

from typing import List
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, Field, field_validator, model_validator

from social_scheduler.constants import DEFAULT_FILE_EXTENSIONS, GERMAN_WEEKDAYS, VALID_STATES


class AccountConfig(BaseModel):
    handle: str = Field(min_length=1)
    channel: str = Field(min_length=1)
    enabled: bool = True


class PlatformConfig(BaseModel):
    name: str = Field(min_length=1)
    accounts: List[AccountConfig] = Field(default_factory=list)

    @field_validator("accounts")
    @classmethod
    def require_accounts(cls, value: List[AccountConfig]) -> List[AccountConfig]:
        if not value:
            raise ValueError("platform must contain at least one account")
        return value


class RulesConfig(BaseModel):
    include_days: List[str] = Field(default_factory=lambda: list(GERMAN_WEEKDAYS))
    file_extensions: List[str] = Field(default_factory=lambda: list(DEFAULT_FILE_EXTENSIONS))
    default_state: str = "queued"

    @field_validator("include_days")
    @classmethod
    def validate_days(cls, value: List[str]) -> List[str]:
        invalid = sorted(set(value) - set(GERMAN_WEEKDAYS))
        if invalid:
            raise ValueError(f"invalid weekdays: {', '.join(invalid)}")
        return value

    @field_validator("file_extensions")
    @classmethod
    def normalize_extensions(cls, value: List[str]) -> List[str]:
        normalized = []
        for extension in value:
            ext = extension.lower().strip()
            if not ext:
                continue
            if not ext.startswith("."):
                ext = f".{ext}"
            normalized.append(ext)
        return normalized or list(DEFAULT_FILE_EXTENSIONS)

    @field_validator("default_state")
    @classmethod
    def validate_state(cls, value: str) -> str:
        if value not in VALID_STATES:
            raise ValueError(f"default_state must be one of {sorted(VALID_STATES)}")
        return value


class ProjectConfig(BaseModel):
    project_name: str = Field(min_length=1)
    timezone: str
    platforms: List[PlatformConfig]
    rules: RulesConfig = Field(default_factory=RulesConfig)

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as exc:
            raise ValueError(f"unknown timezone: {value}") from exc
        return value

    @model_validator(mode="after")
    def ensure_platforms(self) -> "ProjectConfig":
        if not self.platforms:
            raise ValueError("project must contain at least one platform")
        return self
