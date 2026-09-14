# notion-pilot-powers

CRM core + optional local MCP for [Notion Pilot](https://github.com/ldom1/notion-pilot).

Customer path: skills + Notion hosted MCP. Optional local MCP adds dedup, SIREN, and dry-run writes.

```bash
uvx --from git+https://github.com/ldom1/notion-pilot-powers notion-pilot-powers
```

See the design spec in Local Brain: `2026-09-14-skills-mcp-split-design`. Plugin marketplace + generic skills land in a follow-up PR (P2).

## Security & data

- Token via env (`NOTION_TOKEN`), never CLI args.
- External Prosper/OpenRouter tools only with `--with-external` **and** their env vars.
- Write tools default to dry-run (`confirm=false`). Host tool-approval is the real safety boundary.
