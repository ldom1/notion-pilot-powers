# Changelog

## [Unreleased]

## [0.8.0] - 2026-10-21

### Added
- `company-enrichment` ranks lead signals with `references/signals.md`:
  - Each signal type has a strength (0–5) and a hook window. A signal outside its window is context only.
  - A priority score (strength × freshness × confidence × specificity) picks the one signal that carries the hook. The skill skips a hook type that a CRM Activity used in the last 90 days.
  - One event seen in several sources (for example a BOAMP award and its DECP record, or press funding and the BODACC capital change) is one row with all links.
  - New composite signals from the same open sources: contract renewal due (DECP end date = notification + duration), confirmed funding, full takeover, first public contract, contract machine, contract lost, exit from crisis, external vs internal merger, silent pre-distress, and a "replacement vs departure" check.
- The Signals table of the brief has a `Strength` column.
- `person-enrichment` ranks a person appointed to a buying role less than 100 days ago first in a contact pick.

### Fixed
- BODACC corrections and annulments are applied: an annulled notice is no longer reported as a Fact.
- Collective procedures map to states from the judgment nature. A positive exit (« extinction du passif », end of the procedure) no longer blocks the verdict; a running plan still gives Hold.
- BOAMP wins are also searched by the winner's name: the SIRET in an award notice is usually the buyer's.

## [0.7.0] - 2026-10-21

### Added
- Each GitHub Release has one zip per skill (`crm-ops.zip`, `company-enrichment.zip`, `person-enrichment.zip`) for **Customize → Skills → Upload skill** in the Claude app.
- `crm-ops` works as a standalone skill (for skill marketplaces such as Agensi): it sends the user to the notion-pilot.com wizard when no CRM exists, skips enrichment when the enrichment skills are absent, and lists its tested agents and network calls.
- `crm-ops` links `company-enrichment` and `person-enrichment` and says which fields each one fills.
- `company-enrichment` and `person-enrichment` work without `crm-ops` and without a CRM: they keep the preview-then-go rule, and give the result in the chat when no database exists. Each lists its tested agents and public sources.

### Changed
- Plugin `homepage` is now https://notion-pilot.com (was the GitHub repo).

### Fixed
- `crm-ops` companies reference points to `notion_pilot_powers/core/siren_lookup.py` (the old path did not exist).

## [0.6.1] - 2026-10-13

### Fixed
- Skill descriptions and evals no longer name one workspace's company, products or secret manager. The Claude app shows `SKILL.md` to every user who installs it.

## [0.6.0] - 2026-10-13

### Added
- `crm-ops` asks for the reason before it writes `Closed Lost`, and writes it to the Leads `Lost Reason` property (Notion Pilot ≥ 1.3.0; else `Notes`).
- `crm-ops` logs a to-do as an Activity with Type `✅ Task`, a due date in `Next Step Date` and a `Done` checkbox, and checks `Done` when the task is finished.
- `get_open_leads` returns `next_step_date`.

### Changed
- `crm-ops` leads reference: no product names from one workspace; `Product` uses the live options.

## [0.5.1] - 2026-10-13

### Fixed
- Marketplace plugin `source` is now `./`. claude.ai documents relative plugin paths only in this form; `.` gave "Marketplace sync failed" in the Claude app. Claude Code accepts both.
- `company-enrichment` in the Claude app: when the code sandbox has no network, it uses web search or web fetch on annuaire-entreprises and logs the blocked sources.
- Lead brief chat output is Markdown only: no raw `<details>` tags in the Claude app.

## [0.5.0] - 2026-10-13

### Added
- `company-enrichment` finds the ICP in a database titled « ICP profiles » when the user message and the overlay give none. The Notion Pilot wizard deploys it. The brief uses the `Active` profile whose Product and Sectors fit, and asks when more than one fits.

### Changed
- Lead brief: the verdict comes first, before the hook, in the Notion body and in the chat preview.

### Fixed
- `crm-ops` writes nothing while a question in the preview is open. A go sent before the answer does not cover that question.
- `crm-ops` asks one decision per question, and never bundles go with another choice.
- `crm-ops` prints one status line per queried source, without raw JSON or scripts in the chat.
- `crm-ops` no longer points to a missing `references/` folder: it reads the live database schema before a write and uses existing select options only.
- `crm-ops` uses the local MCP Notion tools only when `notion_token` is set. Without it, it uses Notion's hosted connector; `lookup_siren` still works. A local server that fails to start (no `uv`) is ignored.
- `plugin.json`, `pyproject.toml` and `__version__` match the released tag (0.4.0).

## [0.4.0] - 2026-10-07

### Changed
- Lead brief is short and sales-first: Notion body = hook, interest signals, ICP score table (✅/🟡/❌/❔), max 5 checks; at most 25 blocks; a new brief replaces the old one (no addendum). Timeline, claims, retrieval log and conflicts stay in the chat preview.
- Identity goes to Company properties: `NAF`, `Forme juridique`, `Siège`, `Date de création`, `Dirigeant`, `Fiche registre`, `Verdict ICP`, `Dernier brief`.
- Signals record an event date and a public date; only signals public on the as-of date count.

### Added
- Lead brief sources: `decp` (public contracts awarded), `ted` (EU tenders), `cordis` (EU R&D projects), `ademe` (ADEME aid), `ratios-inpi` (filed accounts). All work without authentication.

## [0.3.0] - 2026-10-06

### Added
- `person-enrichment` skill: create/enrich a CRM Person from a public clue (name, email, phone, company, LinkedIn); contact-pick rubric for outreach. Sources in `references/sources.md`, template in `references/person.md`. Public data only — never invent LinkedIn.
- `person-enrichment` data protection rules: professional data only, published work phone only, no personal email unless user-supplied, never an email built from a naming pattern, stop on objection or deletion request. A SAS « Président » maps to `c_suite`, not `founder`.

## [0.2.2] - 2026-10-06

### Fixed
- Lead brief: query Notion CRM (`crm` source — Leads, Activities, Meetings) before marking a buying or compute need Unknown; BOAMP empty does not mean no private RFP.

## [0.2.1] - 2026-10-06

### Fixed
- Lead brief Notion write: read the live select options before proposing `Sector` or `Size`; never write an option the database lacks.
- A current property value with no year (for example `Size` without `Année effectif`) is shown next to the new value and never overwritten by default.
- Size fit also assesses the group when the company is part of one; a readable malformed RSS feed is not `failed`.
- The ICP comes from the user or from where the workspace overlay points (page or database), no longer from a page titled "ICP".

## [0.2.0] - 2026-10-06

### Added
- `company-enrichment` lead brief mode: dated, source-backed brief of a French company (recherche-entreprises, BODACC, BOAMP, RSS, web search) with lead qualification. Source registry in `references/sources.md`, template in `references/brief.md`.
- `Année effectif` property (year of `Size`) documented in the Companies property list (Notion-MCP write from `company-enrichment`). Headcount-to-`Size` and NAF-to-`Sector` tables in `sources.md`.
- Skill structure tests (`tests/unit/skills`) and `company-enrichment` evals.
- Lead brief: "Fact (company claim)" label for a company's own statements; web search finds the official site first; group-level `categorie_entreprise` explained; RSS with no mention logged `empty`.

## [0.1.0]

### Added
- Plugin marketplace + router skill + generic `crm-ops` / `company-enrichment` (P2).
- Declared `.mcp.json` (SHA-pinned, no `--with-external`) and Security & data README (P0 fork A).
- Initial extract of CRM core + stdio MCP from `notion-pilot@5a5e1fbc` (P1).
- `CRMSettings` (env only, no `.env` / Infisical).
- `--with-external` gate for Prosper/OpenRouter tools (D23).
- `lookup_siren` tool; write-safety guards (batch cap 25, deal update merge, enrich requires `page_ids`, activity duplicate skip).
