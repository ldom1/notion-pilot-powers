# Changelog

## Unreleased

### Added
- `company-enrichment` lead brief mode: dated, source-backed brief of a French company (recherche-entreprises, BODACC, BOAMP, RSS, web search) with lead qualification. Source registry in `references/sources.md`, template in `references/brief.md`.
- `Année effectif` property (year of `Size`) documented in the Companies property list (Notion-MCP write from `company-enrichment`). Headcount-to-`Size` and NAF-to-`Sector` tables in `sources.md`.
- Skill structure tests (`tests/unit/skills`) and `company-enrichment` evals.
- Lead brief: "Fact (company claim)" label for a company's own statements; web search finds the official site first; group-level `categorie_entreprise` explained; RSS with no mention logged `empty`.
- Plugin marketplace + router skill + generic `crm-ops` / `company-enrichment` (P2).
- Declared `.mcp.json` (SHA-pinned, no `--with-external`) and Security & data README (P0 fork A).
- Initial extract of CRM core + stdio MCP from `notion-pilot@5a5e1fbc` (P1).
- `CRMSettings` (env only, no `.env` / Infisical).
- `--with-external` gate for Prosper/OpenRouter tools (D23).
- `lookup_siren` tool; write-safety guards (batch cap 25, deal update merge, enrich requires `page_ids`, activity duplicate skip).
