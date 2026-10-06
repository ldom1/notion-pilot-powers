---
name: person-enrichment
description: >-
  Create or enrich a Notion CRM Person from a public clue (name, email, phone,
  company, LinkedIn URL). Fill Name, email, LinkedIn, Position, Seniority and
  Role Type from public sources only. Rank best prospecting contact when several
  people are given. Use when adding contacts, enriching People, or choosing whom
  to call. Follow crm-ops write discipline (preview + go). Never invent LinkedIn,
  email, phone or title. Never copy private or non-public profile data.
---

# person-enrichment

Generic counterpart of `company-enrichment` for humans. **Public data only.** No Infisical, no paid people DB, no scraping behind login.

Two modes:

- **Fill / create Person** — resolve identity, write strongly expected fields on People.
- **Contact pick** — given 2+ people at one company, recommend the best outreach contact for a stated goal (default: prospective exchange).

## Prerequisites

1. Follow **`crm-ops`** write discipline (preview table, explicit go). Property shapes: `crm-ops/references/people.md`.
2. Prefer local MCP `search_people` / `upsert_people` dry-run when available.
3. Without the local MCP, use Notion hosted MCP. Dedup by email, then LinkedIn, then name + company.
4. Resolve or create the **Company** first (`company-enrichment` / `crm-ops`) when the user names an employer.

## Fill / create Person

**Input:** any one or more of: full name, first/last name, email, phone, company name, LinkedIn URL, title.

**In scope:** `Name`, `Company`, `Email - pro`, `Linkedin`, `Position`, `Seniority`, `Role Type`, `Phone` when evidenced from public sources in `references/sources.md`.

**Out of scope:** birth date, home address, private emails, photos, paid data brokers, inventing URLs or titles, schema changes without validation.

**Steps:**

1. Parse the clue. Normalize email domain → company candidate.
2. Dedup in CRM (`crm` source). On exact email or LinkedIn match: UPDATE missing fields only. Do not create a duplicate.
3. Query each source in `references/sources.md`. Log every attempt.
4. Confirm identity: name + company (or email domain) must agree across at least one public source, or the user must confirm. Ambiguous → list candidates, stop.
5. Map title → `Seniority` and `Role Type` with the tables in `references/person.md`. If unsure → propose + `needs_review`.
6. Show the preview table (current vs proposed). Write only after explicit go.
7. Optionally append a short enrichment note on the Person page body (template in `references/person.md`).

**Confidence:** write LinkedIn / email / phone only with a reference link. Never invent a LinkedIn URL from a name guess.

## Contact pick

1. Enrich each person (or use fields already in CRM).
2. Score with the rubric in `references/person.md` against the user's goal (default: prospective technical/commercial exchange).
3. Rank with evidence. Name one **primary** and optional **CC**. State what could make the pick wrong.
4. If a better public contact exists at the company (team page) but is not in the list, name them as Interpretation — do not create them without go.

## Rules

- Public sources only. If a profile is login-walled and you cannot read it, log `not available` — do not invent.
- Never present a paid or private directory hit as Fact.
- Never copy birth date, nationality, or personal phone labelled private.
- Label every material claim (Fact / Fact (company claim) / Fact (CRM) / Interpretation / Unknown).
- Write no LinkedIn without a URL you actually opened or that the user supplied.
- Prefer company team page and user-supplied email over a weak name match.
