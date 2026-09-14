---
name: crm-ops
description: >-
  Operate a Notion CRM (Leads, Activities, People, Companies) deployed by
  Notion Pilot. Use for sales emails, create/update deals, log activities, or
  upsert people/companies. Prefer local notion-pilot-powers MCP when loaded;
  otherwise Notion hosted MCP. Always preview table then wait for explicit go.
---

# crm-ops

Generic CRM operations for a Notion Pilot-deployed workspace. **No workspace names or hard-coded IDs** — resolve DBs via Notion MCP search (titles: Leads / 💶 Leads, Activities / ⚡ Activities, People, Companies, Meetings) or via local MCP `userConfig`.

## Prerequisites

1. **Notion hosted MCP** authenticated (default path). If missing → stop and ask the user to connect it.
2. Optional **local `notion-pilot-powers` MCP** for dry-run upserts, dedup, `lookup_siren`.

Read entity references under `references/` for the entities you touch.

## Hard rules

- **Always preview** — validation table before any create/update. Write only after explicit go (`ok`, `go`, …).
- **Never invent** LinkedIn, SIREN, email, titles, or financials.
- **Language:** follow the user; default EN.
- Prefer one multi-entity plan when the user pastes a thread.

## Tooling preference

| Prefer | Fallback |
|--------|----------|
| Local MCP tools (`upsert_*` dry-run → confirm, `search_*`, `log_activity`, …) | Notion hosted MCP search/fetch/create/update |
| If local MCP failed to start | Hosted MCP only (skills still load — P0 fork A) |

Never call the Notion API directly from this skill.

## Workflow

1. Parse intent → which entities.
2. Resolve existing rows (search).
3. Fill gaps; tag `source=…`.
4. Preview table → ask only for blockers.
5. On go: Company → People → Lead → Activities (link relations).
6. Short summary of what was written / `needs_review`.
