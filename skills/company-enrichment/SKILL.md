---
name: company-enrichment
description: >-
  Enrich Notion CRM Companies with French open company data (SIREN, NAF→sector,
  size). Use when filling firmographics. Prefer lookup_siren / local MCP; follow
  crm-ops write discipline (preview + go). Never invent SIREN or LinkedIn.
---

# company-enrichment

Generic successor of Artelys-only open-data enrichment. **No Infisical, no Prosper requirement** for the customer path.

## Prerequisites

1. Follow **`crm-ops`** write discipline (preview table, explicit go).
2. Prefer local MCP `lookup_siren` / `upsert_companies` dry-run when available.
3. Else Notion hosted MCP + public `recherche-entreprises.api.gouv.fr` via documented steps (or `lookup_siren` when local MCP is up).

## In scope

- SIREN, sector (from NAF), size, country, website, LinkedIn when evidenced.
- BODACC/RNE as **documented open-data steps** when the user asks (no Prosper required).

## Out of scope

- Schema migrations, person enrichment, inventing URLs/financials.
- Prosper / OpenRouter (Louis-only `--with-external` path — not this skill).

## Confidence

Only write SIREN on high confidence (user-supplied 9 digits, or registry name match ≥ 85 with corroboration). Otherwise `needs_review` and leave empty.
