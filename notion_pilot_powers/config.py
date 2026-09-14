"""CRM settings — environment variables only (no .env file, no Infisical)."""

from __future__ import annotations

from typing import Any

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _blank_to_none(v: Any) -> Any:
    if isinstance(v, str) and not v.strip():
        return None
    return v


class CRMSettings(BaseSettings):
    """Fields the local MCP needs. Never reads a project `.env` (D17)."""

    model_config = SettingsConfigDict(
        env_file=None,
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    notion_token: SecretStr | None = None
    notion_people_data_source_id: str | None = None
    notion_companies_data_source_id: str | None = None
    notion_deals_database_id: str | None = None
    notion_activities_database_id: str | None = None
    prosper_mcp_url: str | None = Field(
        default=None,
        description="Prosper SSE URL. None unless set — no localhost default.",
    )
    openrouter_api_key: SecretStr | None = None
    openrouter_model: str = "google/gemini-2.5-flash-lite"
    openrouter_url: str = "https://openrouter.ai/api/v1"
    openrouter_http_referer: str = ""
    openrouter_app_title: str = "notion-pilot-powers"

    @field_validator(
        "notion_token",
        "notion_people_data_source_id",
        "notion_companies_data_source_id",
        "notion_deals_database_id",
        "notion_activities_database_id",
        "prosper_mcp_url",
        "openrouter_api_key",
        mode="before",
    )
    @classmethod
    def _optional_blank(cls, v: Any) -> Any:
        return _blank_to_none(v)


def load_settings() -> CRMSettings:
    return CRMSettings()
