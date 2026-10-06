# Changelog

## [Unreleased]

### Added
- `person-enrichment` skill: create/enrich a CRM Person from a public clue (name, email, phone, company, LinkedIn); contact-pick rubric for outreach. Sources in `references/sources.md`, template in `references/person.md`. Public data only — never invent LinkedIn.

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
