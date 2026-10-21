---
name: company-enrichment
description: >-
  Enrich Notion CRM Companies with French open company data (SIREN, NAF→sector,
  size, revenue), or build a dated, source-backed lead brief on a French company
  (interest signals from BODACC, BOAMP, DECP, TED, CORDIS, ADEME and press; ICP
  qualification; a hook for outreach). Use
  when filling firmographics, qualifying a lead, or preparing outreach ("brief on",
  "avant de contacter", "situation au"). Short output: hook, signals,
  ICP score; identity goes to properties. Prefer lookup_siren / local MCP; follow
  crm-ops write discipline (preview + go). Never invent SIREN or LinkedIn.
---

# company-enrichment

French open-data enrichment for any Notion Pilot CRM. Public sources only; no paid data provider.

Two modes:

- **Fill firmographics** — write SIREN, sector, size and revenue on a Company.
- **Lead brief** — find the interest signals, qualify the lead against the ICP, and write a hook for outreach.

## Prerequisites

1. A CRM deployed in the user's Notion by the free wizard at https://notion-pilot.com, for writes only. Without a Companies database, give the lead brief or the firmographics in the chat, and tell the user the wizard can create the CRM.
2. Follow **`crm-ops`** write discipline (preview table, explicit go). If [`crm-ops`](https://github.com/ldom1/notion-pilot-powers/tree/main/skills/crm-ops) is not installed, the rule still applies: show a preview table and write only after an explicit go.
3. Prefer local MCP `lookup_siren` / `upsert_companies` dry-run when available.
4. Without the local MCP, use Notion hosted MCP, and query `recherche-entreprises.api.gouv.fr` directly (see `references/sources.md`).
5. If the code sandbox has no network (Claude app), use web search or web fetch on `annuaire-entreprises.data.gouv.fr/entreprise/<SIREN>`. Log the blocked sources as "not available" in the retrieval log.

Tested agents: Claude Code, Claude app.

## Network and data

- Public sources only, no account and no token: French company register (`recherche-entreprises.api.gouv.fr`, `annuaire-entreprises.data.gouv.fr`), BODACC and BOAMP (`*-datadila.opendatasoft.com`), DECP (`data.economie.gouv.fr`), TED and CORDIS (`europa.eu`), ADEME (`data.ademe.fr`), and press found by web search. Full list: `references/sources.md`.
- Queries carry a company name or SIREN only. No CRM record leaves the user's Notion except through the user's assistant.

## Fill firmographics

**In scope:** SIREN, sector (from NAF), size, country, website, LinkedIn when evidenced. Revenue with its fiscal year, headcount band with its year. Property names: `references/brief.md`, section "Notion write".

**Out of scope:** schema changes without explicit validation, inventing URLs/financials. Person create/enrich → `person-enrichment`.

**Confidence:** only write SIREN on high confidence (user-supplied 9 digits, or registry name match ≥ 85 with corroboration). Otherwise `needs_review` and leave empty.

## Lead brief

Sources: `references/sources.md`. Scoring, dedup and composites: `references/signals.md`. Output: `references/brief.md`.

1. Get the as-of date. If the user gives none, use today. Reject a future date.
2. Confirm the identity. Use the SIREN first: from the user, the Notion page, `lookup_siren`, or recherche-entreprises. If a name matches more than one company, apply the stop rule in `references/brief.md`.
3. Check that the company existed on the as-of date. If it did not, say so and stop. If it was closed on that date, query recherche-entreprises and BODACC only. Give the closure evidence and the verdict "Do not pursue". Log the other sources "not applicable: company closed".
4. Get the ICP. Look in this order: the user message, then the ICP that the workspace overlay skill points to (a page or a database), then a database titled « ICP profiles » (the wizard deploys it in the ICP page of the CRM). In that database, use the profile with Status `Active` whose Product and Sectors fit the prospect. If more than one fits, or none, ask the user. If you find no ICP, use the default criteria in `references/brief.md` and say so.
5. If the brief is for a Notion Company (or the user names a CRM company), query the **`crm`** source in `references/sources.md` **before** you mark any buying need, compute need, or outreach signal as Unknown. Read linked Leads, Activities and Meetings.
6. Query each other source in `references/sources.md`. Apply its as-of filter. Log every attempt in the retrieval log.
7. Record each interest signal with its label (Fact, Interpretation, Unknown), event date, public date and reference link.
8. Apply `references/signals.md` in its order: drop annulled notices and apply corrections, merge the same event across sources, set the procedure state, compute the composite signals, give each signal its strength and hook window, then rank by priority score.
9. List conflicts, stale data and failed retrievals. Then score each ICP criterion with evidence. CRM claims override an open-data "Unknown" on the same topic.
10. Write the hook from the top-ranked signal and the ICP pain.
11. Write the brief in the user's language, with the template in `references/brief.md`. Offer the Notion write.

## Rules

- **Be brief.** The reader is a sales rep. Put the verdict, the hook and the signals first. Identity goes to properties, evidence stays in the chat. Follow "Concision" in `references/brief.md`.

- Write no Fact without a reference link.
- Never present data published after the as-of date as known on that date.
- Never turn an Interpretation into a Fact. A name match stays an Interpretation.
- Never say a source was queried if you did not query it. If you have no tool for a source, log it "not available".
- Give revenue with its fiscal year and headcount with its year.
- Copy manager names and roles only. Never copy a birth date.
