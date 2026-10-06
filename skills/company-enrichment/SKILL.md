---
name: company-enrichment
description: >-
  Enrich Notion CRM Companies with French open company data (SIREN, NAF→sector,
  size, revenue), or build a dated, source-backed lead brief on a French company
  (situation as of a date, BODACC/BOAMP events, press, lead qualification). Use
  when filling firmographics, qualifying a lead, or preparing outreach ("brief on",
  "avant de contacter", "situation au"). Prefer lookup_siren / local MCP; follow
  crm-ops write discipline (preview + go). Never invent SIREN or LinkedIn.
---

# company-enrichment

Generic successor of Artelys-only open-data enrichment. **No Infisical, no Prosper requirement** for the customer path.

Two modes:

- **Fill firmographics** — write SIREN, sector, size and revenue on a Company.
- **Lead brief** — build a dated, source-backed brief and qualify the lead.

## Prerequisites

1. Follow **`crm-ops`** write discipline (preview table, explicit go).
2. Prefer local MCP `lookup_siren` / `upsert_companies` dry-run when available.
3. Without the local MCP, use Notion hosted MCP, and query `recherche-entreprises.api.gouv.fr` directly (see `references/sources.md`).

## Fill firmographics

**In scope:** SIREN, sector (from NAF), size, country, website, LinkedIn when evidenced. Revenue with its fiscal year, headcount band with its year. Property names: `references/brief.md`, section "Notion write".

**Out of scope:** schema changes without explicit validation, inventing URLs/financials. Person create/enrich → `person-enrichment`. Prosper / OpenRouter (Louis-only `--with-external` path — not this skill).

**Confidence:** only write SIREN on high confidence (user-supplied 9 digits, or registry name match ≥ 85 with corroboration). Otherwise `needs_review` and leave empty.

## Lead brief

Sources: `references/sources.md`. Output: `references/brief.md`.

1. Get the as-of date. If the user gives none, use today. Reject a future date.
2. Confirm the identity. Use the SIREN first: from the user, the Notion page, `lookup_siren`, or recherche-entreprises. If a name matches more than one company, apply the stop rule in `references/brief.md`.
3. Check that the company existed on the as-of date. If it did not, say so and stop. If it was closed on that date, query recherche-entreprises and BODACC only. Give the closure evidence and the verdict "Do not pursue". Log the other sources "not applicable: company closed".
4. Get the ICP. Look in this order: the user message, then the ICP that the workspace overlay skill points to (a page or a database). If you find none, use the default criteria in `references/brief.md` and say so.
5. If the brief is for a Notion Company (or the user names a CRM company), query the **`crm`** source in `references/sources.md` **before** you mark any buying need, compute need, or outreach signal as Unknown. Read linked Leads, Activities and Meetings.
6. Query each other source in `references/sources.md`. Apply its as-of filter. Log every attempt in the retrieval log.
7. Record each material claim with its label (Fact, Interpretation, Unknown), source, event date, retrieval date and reference link.
8. List conflicts, stale data and failed retrievals. Then qualify the lead with explicit evidence. CRM claims override an open-data "Unknown" on the same topic.
9. Write the brief in the user's language, with the template in `references/brief.md`. Offer the Notion write.

## Rules

- Write no Fact without a reference link.
- Never present data published after the as-of date as known on that date.
- Never turn an Interpretation into a Fact. A name match stays an Interpretation.
- Never say a source was queried if you did not query it. If you have no tool for a source, log it "not available".
- Give revenue with its fiscal year and headcount with its year.
- Copy manager names and roles only. Never copy a birth date.
