"""Write-safety guards (D18/D24)."""

from unittest.mock import AsyncMock

import pytest
from notion_pilot_powers.config import CRMSettings as Settings
from notion_pilot_powers.mcp.models import ActivityInput, DealInput, PersonRecord
from notion_pilot_powers.mcp.session import SyncerSession
from notion_pilot_powers.mcp.tools import enrich_people, log_activity, upsert_deal, upsert_people
from pydantic import SecretStr


def _settings() -> Settings:
    return Settings(
        notion_token=SecretStr("t"),
        notion_people_data_source_id="p",
        notion_companies_data_source_id="c",
        notion_deals_database_id="d",
        notion_activities_database_id="a",
    )


async def _session() -> SyncerSession:
    s = SyncerSession(_settings())
    s.company_syncer.load_notion_snapshot = AsyncMock()
    s.people_syncer.load_notion_snapshot = AsyncMock()
    s.deals_syncer.load_notion_snapshot = AsyncMock()
    await s.ensure_loaded()
    return s


async def test_batch_cap_rejects_26():
    session = await _session()
    with pytest.raises(ValueError, match="batch cap is 25"):
        await upsert_people(
            session, [PersonRecord(name=f"N{i}", company="C") for i in range(26)], confirm=False
        )


async def test_enrich_requires_page_ids():
    session = await _session()
    with pytest.raises(ValueError, match="page_ids"):
        await enrich_people(session, _settings(), page_ids=None, confirm=False)


async def test_upsert_deal_update_omits_stage_when_not_passed():
    session = await _session()
    session.deals_syncer._snapshot = {"Existing": "deal-1"}
    session.deals_syncer.update_merge = AsyncMock(return_value="deal-1")
    result = await upsert_deal(
        session, _settings(), DealInput(name="Existing", confirm=True)
    )
    record = session.deals_syncer.update_merge.call_args[0][1]
    assert record.stage == ""
    assert result["status"] == "updated"


async def test_log_activity_skips_duplicate():
    session = await _session()
    session.activities.list_recent = AsyncMock(
        return_value=[
            {
                "page_id": "a1",
                "title": "Call",
                "type": "📞 Call",
                "date": "2026-09-14",
                "deal_id": "",
                "person_id": "",
                "company_id": "",
            }
        ]
    )
    session.activities.create = AsyncMock()
    result = await log_activity(
        session,
        _settings(),
        ActivityInput(type="📞 Call", title="Call", date="2026-09-14", confirm=True),
    )
    assert result["status"] == "duplicate_skipped"
    session.activities.create.assert_not_called()
