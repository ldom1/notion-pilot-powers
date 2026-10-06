# Person template — enrichment & contact pick

Write in the user's language. Keep section order.

Header: `<Full name> — <Company> — enriched <today> — identity: confirmed | unconfirmed`

## Identity

- Full name, email, phone (if public), employer, LinkedIn URL.
- How identity was confirmed (user email + domain, company site, LinkedIn, registry manager).
- **Stop rule:** if unconfirmed, list up to 5 candidates (name, employer, source link). Ask the user to choose. Do not write Notion properties.

## Claims

| Claim | Label | Source | Retrieved | Reference |
|---|---|---|---|---|

- **Fact** — official registry or a URL you opened that states the claim.
- **Fact (company claim)** — employer site or employer press.
- **Fact (CRM)** — already on a CRM Person / Lead / Activity, with Notion link.
- **Interpretation** — inferred (seniority from title, best-contact score).
- **Unknown** — searched, not found.

Never write a Fact without a reference link. Never invent LinkedIn.

## Retrieval log

| Source | Status | Detail |
|---|---|---|

Status: `queried` | `empty` | `failed` | `not applicable` | `not available`.

## Title → CRM enums

Property shapes: `crm-ops/references/people.md`.

**Seniority** (pick one):

| Title signals | Seniority |
|---|---|
| Fondateur, Co-founder, Président (founder) | `founder` |
| CEO, CTO, COO, DG, Gérant (exec) | `c_suite` |
| VP, SVP | `vp` |
| Directeur, Director, Head of | `director` |
| Manager, Responsible, Lead (people mgr) | `manager` |
| Senior / Principal (IC) | `senior` |
| Mid-level IC | `mid` |
| Junior, Intern | `junior` |

If unsure → propose and mark `needs_review`. Do not invent a title to force a bucket.

**Role Type** (multi_select; pick all that fit):

Read the live People select options before write. Map title meaning to the closest existing tags (examples of meaning, not fixed labels): purchase → buyer/procurement; modeling/HPC/IT → technical/engineering; sales → commercial; C-level without function → executive; finance/HR/legal → operations or other as available.

Never create an option without validation.

## Contact pick rubric

Goal default: **prospective exchange** (discover need, not close a PO).

Score each person 0–2 per row. Highest total = primary. Tie-break: technical over pure admin for a technical product; then seniority that can sponsor a next meeting.

| Criterion | 2 | 1 | 0 |
|---|---|---|---|
| Domain fit | Owns the problem (compute, product, architecture) | Adjacent | Unrelated (pure admin/finance) |
| Reach | Public email or known channel | LinkedIn only | No channel |
| Authority | Can sponsor a pilot or intro | Influences | No leverage |
| Warmth | Prior CRM Activity / warm intro | Cold but public bio | Unknown |

Output:

- **Primary** — name, why (cite claims).
- **CC / secondary** — optional.
- **What could make this wrong** — weakest evidence.
- Better public contact not in the list → name as Interpretation only.

## Notion write

1. Show a preview table: property, current, proposed, source link. Wait for go.
2. Create or update the Person. Required: `Name`, `Company`. Strongly expected: `Email - pro`, `Linkedin`, `Position`, `Seniority`, `Role Type`, `Phone`.
3. Do not overwrite a filled field with a weaker source without asking.
4. Optional: append under a dated heading on the Person body: Identity summary, Claims table, Retrieval log, Contact-pick note if any.
5. If the user names a Lead, offer to add the Person to Lead `Contacts` after go.
