---
name: notion-pilot-powers
description: >-
  Entry point for Notion Pilot CRM skills. Routes to crm-ops (leads, activities,
  people, companies), company-enrichment (SIREN / open data), or person-enrichment (public contact data). Use when the user
  works a Notion CRM from Claude Code, pastes sales email, or asks to log a deal
  or activity. Trigger: /notion-pilot-powers
---

# notion-pilot-powers

One plugin, three skills. **Notion hosted MCP is required** for the default path. The local `notion-pilot-powers` MCP is optional (dedup, SIREN, dry-run).

## Route

| Skill | When |
|---|---|
| `crm-ops` | Create/update leads, log activities, upsert people/companies, search CRM |
| `company-enrichment` | Fill SIREN / sector / size / open-data fields on a company, or build a dated lead brief |
| `person-enrichment` | Create/enrich a Person from a public clue (name, email, phone, LinkedIn); pick best outreach contact |

## Prerequisites

1. Notion hosted MCP connected (`mcp.notion.com`) — default path (D3).
2. Optional: fill plugin `userConfig` (token + 4 IDs) for the local MCP.

Do not invent CRM IDs. Do not enable Prosper/OpenRouter tools in the customer plugin.
