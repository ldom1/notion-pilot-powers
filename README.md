# notion-pilot-powers

CRM skills + optional local MCP for [Notion Pilot](https://github.com/ldom1/notion-pilot).

## Install (Claude Code)

```
/plugin marketplace add ldom1/notion-pilot-powers
/plugin install notion-pilot-powers@notion-pilot-powers
```

1. Deploy the CRM structure at [notion-pilot.com](https://notion-pilot.com).
2. Connect **Notion's hosted MCP** (default path — no token required in the plugin).
3. Optional: create an internal integration (Read / Update / Insert content, **No user information**), share **only the CRM parent page**, and fill plugin settings (token + 4 IDs) for the local MCP.

```bash
uvx --from git+https://github.com/ldom1/notion-pilot-powers@<release-sha> notion-pilot-powers
```

## Security & data

**The write safety boundary is your assistant's tool-approval prompt**, not the server's `confirm` flag. Do not add write tools to `permissions.allow`, and do not run write sessions with `--dangerously-skip-permissions` or auto mode.

| # | Connection | Auth | Standing access? |
|---|---|---|---|
| T1 | notion-pilot.com wizard | OAuth as you; token only in session cookie | No token kept server-side |
| T2 | Notion hosted MCP (default) | OAuth as you, full user permissions | Until disconnected |
| T3 | Local notion-pilot-powers MCP | Internal integration token | Until integration removed |
| T4 | Assistant provider | Your assistant account | Per provider terms |
| T5 | `lookup_siren` → gov API | None | Name queries only |

- **Token storage:** macOS Keychain (fallback `~/.claude/.credentials.json`). **Linux/Windows:** plaintext `~/.claude/.credentials.json` (file permissions only).
- Token reaches the server as an **environment variable**, never a CLI argument.
- External Prosper/OpenRouter tools need `--with-external` **and** their env vars (not shipped in the plugin `.mcp.json`).

### Where your data goes

> **Where your data goes.** Your CRM records are stored in your Notion workspace. On the **Notion Enterprise plan**, Notion can host that workspace in the EU (Frankfurt); on other plans, Notion stores it in its default region (US). Region and terms are set by your agreement with Notion ([details](https://www.notion.com/help/data-residency)). EU hosting covers CRM data stored in Notion, not AI processing. When your assistant reads CRM records, that content is processed by your assistant's provider (e.g. Anthropic for Claude), under the provider's data processing terms; Notion's residency does not cover it. Notion states that some of its own AI processing can also happen outside the residency region. notion-pilot.com deploys the CRM structure and keeps no CRM records and no Notion access token.

## Developers

Self-host capture channels (Telegram, email, Discord) live in the [notion-pilot wiki](https://github.com/ldom1/notion-pilot/wiki/Self-host).
