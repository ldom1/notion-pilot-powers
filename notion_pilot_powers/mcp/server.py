"""stdio MCP server for notion-pilot-powers (no HTTP transport)."""

from __future__ import annotations

import argparse
import sys

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from notion_pilot_powers import __version__
from notion_pilot_powers.config import CRMSettings, load_settings
from notion_pilot_powers.mcp import tools as t
from notion_pilot_powers.mcp.models import (
    ActivityInput,
    BatchResult,
    CompanyRecord,
    DealInput,
    PersonRecord,
)
from notion_pilot_powers.mcp.session import SyncerSession

_RO = ToolAnnotations(readOnlyHint=True)
_RO_OPEN = ToolAnnotations(readOnlyHint=True, openWorldHint=True)
_WRITE = ToolAnnotations(destructiveHint=True, idempotentHint=True)
_APPEND = ToolAnnotations(destructiveHint=False, idempotentHint=True)
_OPEN = ToolAnnotations(openWorldHint=True)

mcp = FastMCP("notion-pilot-powers")

_settings: CRMSettings | None = None
_session: SyncerSession | None = None


def _get_settings() -> CRMSettings:
    global _settings
    if _settings is None:
        _settings = load_settings()
    return _settings


def _get_session() -> SyncerSession:
    global _session
    if _session is None:
        _session = SyncerSession(_get_settings())
        _session.start_prewarm()
    return _session


def _register_core() -> None:
    @mcp.tool(annotations=_WRITE)
    async def upsert_people(records: list[PersonRecord], confirm: bool = False) -> BatchResult:
        """Upsert people (dedup-checked). Dry-run unless confirm=True."""
        return await t.upsert_people(_get_session(), records, confirm)

    @mcp.tool(annotations=ToolAnnotations(destructiveHint=True, idempotentHint=True, openWorldHint=True))
    async def upsert_companies(records: list[CompanyRecord], confirm: bool = False) -> BatchResult:
        """Upsert companies (dedup + optional SIREN). Dry-run unless confirm=True."""
        return await t.upsert_companies(_get_session(), _get_settings(), records, confirm)

    @mcp.tool(annotations=_RO)
    async def find_duplicates(
        target: str = "both", threshold: float = 85.0
    ) -> list[dict[str, float | str]]:
        """Find likely-duplicate People/Companies pairs."""
        return await t.find_duplicates(_get_session(), target, threshold)

    @mcp.tool(annotations=_RO)
    async def search_people(query: str, limit: int = 10) -> list[dict[str, object]]:
        """Fuzzy-search People — read-only."""
        return await t.search_people(_get_session(), query, limit)

    @mcp.tool(annotations=_RO)
    async def search_companies(query: str, limit: int = 10) -> list[dict[str, object]]:
        """Fuzzy-search Companies — read-only."""
        return await t.search_companies(_get_session(), query, limit)

    @mcp.tool(name="get_recent_people", annotations=_RO)
    async def get_recent_people_endpoint() -> list[dict[str, object]]:
        """People added in the last 7 days."""
        return await t.get_recent_people_tool(_get_settings())

    @mcp.tool(name="get_open_leads", annotations=_RO)
    async def get_open_leads_endpoint() -> list[dict[str, object]]:
        """Open (non-closed) deals."""
        return await t.get_open_leads_tool(_get_settings())

    @mcp.tool(annotations=_WRITE)
    async def upsert_deal(deal: DealInput) -> dict[str, object]:
        """Upsert a deal by exact title. Dry-run unless confirm=True."""
        return await t.upsert_deal(_get_session(), _get_settings(), deal)

    @mcp.tool(annotations=_APPEND)
    async def log_activity(activity: ActivityInput) -> dict[str, object]:
        """Append an activity. Dry-run unless confirm=True. Exact duplicates skipped."""
        return await t.log_activity(_get_session(), _get_settings(), activity)

    @mcp.tool(name="get_activities", annotations=_RO)
    async def get_activities_endpoint(
        deal_page_id: str | None = None, limit: int = 20
    ) -> list[dict[str, object]]:
        """Recent activities, newest first."""
        return await t.get_activities_tool(_get_session(), _get_settings(), deal_page_id, limit)

    @mcp.tool(annotations=_RO)
    async def refresh_notion_snapshot() -> dict[str, int]:
        """Reload the in-memory People/Companies cache from Notion (other clients may have written)."""
        return await t.refresh_notion_snapshot(_get_session())

    @mcp.tool(annotations=_RO_OPEN)
    async def lookup_siren(name: str) -> list[dict[str, object]]:
        """Look up French company SIREN candidates (gov API). Read-only."""
        return await t.lookup_siren_tool(name)


def _register_external() -> None:
    settings = _get_settings()
    if settings.prosper_mcp_url:

        @mcp.tool(annotations=_OPEN)
        async def enrich_people(page_ids: list[str], confirm: bool = False) -> BatchResult:
            """Enrich People via Prosper (empty fields only). page_ids required (1–25)."""
            return await t.enrich_people(_get_session(), settings, page_ids, confirm=confirm)

        @mcp.tool(annotations=_OPEN)
        async def enrich_companies(page_ids: list[str], confirm: bool = False) -> BatchResult:
            """Enrich Companies via Prosper (empty fields only). page_ids required (1–25)."""
            return await t.enrich_companies(_get_session(), settings, page_ids, confirm=confirm)

    if settings.openrouter_api_key:

        @mcp.tool(annotations=_RO_OPEN)
        async def rank_contacts_for_pitch(
            pitch: str,
            top_k: int = 10,
            company: str | None = None,
            seniority: str | None = None,
            role_type: str | None = None,
        ) -> list[dict[str, object]]:
            """Rank CRM contacts for a pitch (OpenRouter)."""
            return await t.rank_contacts_for_pitch(
                _get_session(), settings, pitch, top_k, company, seniority, role_type
            )


_register_core()


def enable_external_tools() -> None:
    """Register Prosper/OpenRouter tools when env is set (D23). Idempotent enough for one process."""
    _register_external()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="notion-pilot-powers")
    parser.add_argument(
        "--with-external",
        action="store_true",
        help="Register Prosper/OpenRouter tools when their env vars are set (D23).",
    )
    args = parser.parse_args(argv)
    print(
        f"notion-pilot-powers v{__version__} (stdio"
        f"{', external' if args.with_external else ''})",
        file=sys.stderr,
    )
    if args.with_external:
        enable_external_tools()
    mcp.run()


if __name__ == "__main__":
    main()
