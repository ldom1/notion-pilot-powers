"""Smoke test for mcp/server.py — verifies core tools are registered, no network."""

import pytest

pytest.importorskip("mcp")


async def test_core_tools_registered_without_external(monkeypatch):
    monkeypatch.setenv("NOTION_TOKEN", "fake-token")
    monkeypatch.setenv("NOTION_PEOPLE_DATA_SOURCE_ID", "fake-people-ds")
    monkeypatch.setenv("NOTION_COMPANIES_DATA_SOURCE_ID", "fake-companies-ds")
    # Clear optional external so they wouldn't register even with flag
    monkeypatch.delenv("PROSPER_MCP_URL", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    from notion_pilot_powers.mcp.server import mcp

    tools = await mcp.list_tools()
    tool_names = {t.name for t in tools}
    assert tool_names == {
        "upsert_people",
        "upsert_companies",
        "find_duplicates",
        "search_people",
        "search_companies",
        "get_recent_people",
        "get_open_leads",
        "refresh_notion_snapshot",
        "upsert_deal",
        "log_activity",
        "get_activities",
        "lookup_siren",
    }
    assert "enrich_people" not in tool_names
    assert "rank_contacts_for_pitch" not in tool_names


async def test_external_tools_need_flag_and_env(monkeypatch):
    monkeypatch.setenv("NOTION_TOKEN", "fake-token")
    monkeypatch.setenv("PROSPER_MCP_URL", "http://example.test/sse")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")
    monkeypatch.setenv("NOTION_PEOPLE_DATA_SOURCE_ID", "p")
    monkeypatch.setenv("NOTION_COMPANIES_DATA_SOURCE_ID", "c")

    # Re-import path: call enable_external_tools on fresh settings
    import notion_pilot_powers.mcp.server as srv

    srv._settings = None
    srv.enable_external_tools()
    tools = await srv.mcp.list_tools()
    names = {t.name for t in tools}
    assert "enrich_people" in names
    assert "enrich_companies" in names
    assert "rank_contacts_for_pitch" in names
