---
name: crm-ops
description: >-
  Operate a Notion CRM (Leads, Activities, People, Companies) deployed by
  Notion Pilot. Use for sales emails, create/update deals, log activities, or
  upsert people/companies. Prefer local notion-pilot-powers MCP when loaded;
  otherwise Notion hosted MCP. Always preview table then wait for explicit go.
---

# crm-ops

Generic CRM operations for a Notion Pilot-deployed workspace. **No workspace names or hard-coded IDs** — resolve DBs via Notion MCP search (titles: Leads / 💶 Leads, Activities / ⚡ Activities, People, Companies, Meetings, ICP profiles) or via local MCP `userConfig`.

## Prerequisites

1. **CRM deployed** in the user's Notion by the free wizard at https://notion-pilot.com. If no Leads / People / Companies databases exist → stop and send the user there.
2. **Notion hosted MCP** authenticated (default path). If missing → stop and ask the user to connect it.
3. Optional **local `notion-pilot-powers` MCP** for dry-run upserts, dedup, `lookup_siren`. Install: https://github.com/ldom1/notion-pilot-powers.
4. Optional skills for enrichment. If they are not installed, do not enrich: leave the fields empty, list them under `needs_review`, and tell the user which skill fills them.
   - [`company-enrichment`](https://github.com/ldom1/notion-pilot-powers/tree/main/skills/company-enrichment): SIREN, sector, size, revenue and a lead brief for French companies.
   - [`person-enrichment`](https://github.com/ldom1/notion-pilot-powers/tree/main/skills/person-enrichment): role, seniority and work contact for a person, from public sources.

Tested agents: Claude Code, Claude app.

Before a write, read the live schema of each database you touch (property names, types, select options). Write only existing select options; if a value has no option, show it and ask.

## Network and data

- This skill calls only the MCP servers above. It never calls an API directly.
- CRM records stay in the user's Notion. notion-pilot.com keeps no CRM records and no Notion token.
- The local MCP `lookup_siren` tool queries the French government company register (`recherche-entreprises.api.gouv.fr`) with company names only. No token is sent.

## Hard rules

- **Always preview** — validation table before any create/update. Write only after explicit go (`ok`, `go`, …).
- **An open question blocks the write.** If the preview asks a question, write nothing until the user answers it. A go sent while a question is open does not cover it: ask the question again, then show the updated preview.
- **One decision per question.** Never bundle go with another choice (a stage, a sector, an ICP). When several choices are open, number them so each gets its own answer.
- **No tool noise in the chat.** While you query sources, print one status line per source (`BODACC — 3 notices`, `TED — empty`, `DECP — failed: 403`). Never paste raw JSON, scripts or API responses.
- **Never invent** LinkedIn, SIREN, email, titles, or financials.
- **Language:** follow the user; default EN.
- Prefer one multi-entity plan when the user pastes a thread.

## Tooling preference

| Prefer | Fallback |
|--------|----------|
| Local MCP tools (`upsert_*` dry-run → confirm, `search_*`, `log_activity`, …) **only when the plugin's `notion_token` is set** | Notion hosted MCP search/fetch/create/update |
| No `notion_token`, or a local tool returns a `NOTION_TOKEN` error | Hosted MCP only. `lookup_siren` still works: it needs no token |
| Local MCP failed to start (for example `uv` not installed) | Hosted MCP only. Skills still load |

Never call the Notion API directly from this skill.

## Workflow

1. Parse intent → which entities.
2. Resolve existing rows (search).
3. Fill gaps; tag `source=…`.
4. Preview table → ask only for blockers.
5. On go: Company → People → Lead → Activities (link relations).
6. Short summary of what was written / `needs_review`.
