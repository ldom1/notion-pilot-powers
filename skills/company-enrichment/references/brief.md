# Brief template — lead brief

Write the brief in the user's language. Keep the section order. Translate the table column names when the user does not write in English.

Header line: `<legal name> — SIREN <SIREN> — as of <AS_OF> — brief of <today> — identity: confirmed | unconfirmed`

## Identity

- Legal name, brand name if any, SIREN, head office, NAF code and label, legal form, category.
- State on the as-of date: active, closed (date), or not yet created.
- **Stop rule:** if the identity is unconfirmed, write only the Identity section and the retrieval log.
  - In Identity, show up to 5 candidates (name, SIREN, city, NAF, state). Ask the user to choose.
  - If the registry gives more than 5 matches, also ask for a city, an activity or a website.
  - In the retrieval log, log the other sources "not applicable: identity unconfirmed".
- Identity is confirmed only when the registry returns the SIREN. The SIREN can come from the user, the Notion page, or a single name match that agrees on city or activity.
- If the registry does not return a given SIREN, write "SIREN not found" and stop.

## Timeline

Events on or before the as-of date, newest first.

| Date | Event | Source | Reference |
|---|---|---|---|

## Claims

One row per material claim. A material claim is a fact that changes the qualification or the outreach.

| Claim | Label | Source | Event date | Retrieved | Reference |
|---|---|---|---|---|---|

- **Fact** — read from an official record, with a reference link.
- **Interpretation** — inferred from facts, or read from press, web or a name match.
- **Unknown** — searched but not found, or the source failed.

Rules:

- Give the headcount band with its year: "10-19 (2023)". Give revenue with its fiscal year: "CA 4.2 M€ (2022)".
- A "current state" value is a Fact about today. Write "Fact (current state)" when you use it for a past date.
- Managers: name and role only. Never copy a birth date or a nationality.
- Never write a Fact without a reference link.

## Retrieval log

One row per source in `sources.md`.

| Source | Status | Detail |
|---|---|---|

Status values:

- `queried` — the source returned data.
- `empty` — the source answered with no result.
- `failed` — error or timeout. Give the error.
- `not applicable` — the source cannot cover the as-of date. Give the reason.
- `not available` — no tool to reach the source.

## Conflicts and stale data

- Conflicts: field, value per source, which value is newer.
- Stale data: values older than 2 years on the as-of date, and "current state" values used for a past date.

## Lead qualification

- **Verdict:** Pursue, Pursue after checks, Hold, or Do not pursue.
- **Criteria:** the ICP used, and where it comes from (user, workspace overlay, Notion "ICP" page, or default criteria).
- **Default criteria:** company active; sector fit; size fit; no open collective procedure; recent growth, hiring or contract signals.
- Mark a criterion "not assessed" when no ICP or no data allows it. With a "not assessed" criterion, the best verdict is "Pursue after checks".
- **Evidence:** for each criterion, the matching claims and their labels.
- **What could make this wrong:** the weakest evidence, and the data you could not get.
- **Verify before outreach:** the checks the user must do first. If the NAF is 70.10Z (head office or holding), say that the buyer can be a subsidiary.
- **Closed company:** if a BODACC "Ventes et cessions" notice names a buyer or an absorbing company (`acte.descriptif`), give it as the possible successor. Label it Fact, with the notice link.

A closed company, or one in liquidation on the as-of date, gets "Do not pursue". A company in sauvegarde or redressement gets "Hold" unless the ICP says otherwise.

## Notion write

Follow `crm-ops` write discipline.

1. Read the current property values of the page. Show a preview of the brief and of the new property values.
2. Wait for an explicit go.
3. Append the brief to the Company page body, under the heading `Brief — as of <AS_OF>`.
4. Fill only these properties, and only from a Fact: `SIREN`, `Sector`, `Size`, `Année effectif`, `CA`, `Résultat net`, `Marge nette %`, `Année financière`.
5. `Année financière` is the fiscal year of `CA`, `Résultat net` and `Marge nette %`. `Année effectif` is the year of `Size`.
6. Properties hold the latest known value. Skip a property when the page already has an equal or newer year. A brief for a past date goes to the page body only.
7. If a property does not exist in the database, propose its name and type. Create it only after explicit validation. Types: `Année effectif` and `Année financière` are numbers; `CA` and `Résultat net` are euro numbers; `Marge nette %` is a percent number.
