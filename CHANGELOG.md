# Changelog

## Unreleased

### Added
- Plugin marketplace + router skill + generic `crm-ops` / `company-enrichment` (P2).
- Declared `.mcp.json` (SHA-pinned, no `--with-external`) and Security & data README (P0 fork A).
- Initial extract of CRM core + stdio MCP from `notion-pilot@5a5e1fbc` (P1).
- `CRMSettings` (env only, no `.env` / Infisical).
- `--with-external` gate for Prosper/OpenRouter tools (D23).
- `lookup_siren` tool; write-safety guards (batch cap 25, deal update merge, enrich requires `page_ids`, activity duplicate skip).
