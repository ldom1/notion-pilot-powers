# Brief template — lead brief

Write the brief in the user's language. Keep the section order. Translate headings and table column names when the user does not write in English.

The brief has two outputs:

- **Working notes** (chat only): Identity, Signals, Retrieval log, Conflicts and stale data. They hold the evidence. Show them in the preview. Never write them to Notion.
- **Notion page**: identity in properties, and a short body for the sales rep. See "Notion page" and "Notion write".

## Concision

The reader is a sales rep who prepares a call or an email. Every line must help that.

- Lead with the hook and the interest signals. They are the reason to call now.
- One line per bullet. One fact per line. No process notes, no "lessons", no restated rules.
- Never repeat in the body a value that is in a property (SIREN, NAF, head office, manager, size, revenue).
- Notion body: at most 25 top-level blocks. Working notes: tables, no prose paragraphs.
- Drop routine notices that carry no sales meaning (for example BODACC "Modifications diverses" with no change of capital, manager, head office or activity).
- A new brief replaces the previous one. Never append an addendum.

## Identity

Header line: `<legal name> — SIREN <SIREN> — as of <AS_OF> — identity: confirmed | unconfirmed`

- Legal name, brand name if any, SIREN, head office, NAF code and label, legal form, creation date, manager.
- State on the as-of date: active, closed (date), or not yet created.
- **Stop rule:** if the identity is unconfirmed, write only the Identity section and the retrieval log.
  - In Identity, show up to 5 candidates (name, SIREN, city, NAF, state). Ask the user to choose.
  - If the registry gives more than 5 matches, also ask for a city, an activity or a website.
  - In the retrieval log, log the other sources "not applicable: identity unconfirmed".
- Identity is confirmed only when the registry returns the SIREN. The SIREN can come from the user, the Notion page, or a single name match that agrees on city or activity.
- If the registry does not return a given SIREN, write "SIREN not found" and stop.

## Signals

An interest signal is a dated event that gives a reason to contact the company now, or that changes its needs or its budget. Events on or before the as-of date, newest first.

| Event date | Public on | Type | Signal | Label | Reference |
|---|---|---|---|---|---|

- **Event date** is the date of the event or the fiscal year. **Public on** is the publication, filing or release date. Keep a signal only when **Public on** is on or before the as-of date.

Types: press, funding, partnership, public contract (`boamp`, `decp`, `ted`), EU project (`cordis`), public aid (`ademe`), manager change, capital or transfer (`bodacc`), hiring, procedure, accounts (`ratios-inpi`), CRM.

Labels:

- **Fact** — read from an official record, with a reference link.
- **Fact (company claim)** — stated by the company on its own site or in its own press release. It is a fact that the company says it, not that it is verified. This matters most for clients, references, technologies and commercial figures. Give the deep link when one exists.
- **Fact (CRM)** — written on a Lead, Activity or Meeting in the CRM, with a Notion link.
- **Fact (current state)** — a current value (registry, address, manager) used for a past as-of date.
- **Interpretation** — inferred from facts, or read from press, web or a name match.
- **Unknown** — searched but not found, or the source failed. For buying needs, compute needs, RFPs or partners: only after `crm` was queried (or logged not available).

Rules:

- Never write a Fact without a reference link.
- Give the headcount band with its year: "10-19 (2023)". Give revenue with its fiscal year: "CA 4.2 M€ (2022)".
- Managers: name and role only. Never copy a birth date or a nationality.

## Retrieval log

One row per source in `sources.md`.

| Source | Status | Detail |
|---|---|---|

Status values:

- `queried` — the source returned data.
- `empty` — the source answered, but no record matches the company. Use it also when you read the RSS feeds and none mentions the company.
- `failed` — error or timeout, or a response you cannot read. Give the error. A malformed feed that you can still read is `empty` or `queried`, with a note.
- `not applicable` — the source cannot cover the as-of date. Give the reason.
- `not available` — no tool to reach the source.

## Conflicts and stale data

- Conflicts: field, value per source, which value is newer.
- Stale data: values older than 2 years on the as-of date, and "current state" values used for a past date.
- A conflict that matters for the outreach (for example the size) becomes one "Check before contact" item on the Notion page.

## Lead qualification

- **Verdict:** Pursue, Pursue after checks, Hold, or Do not pursue.
- **Criteria:** the ICP used, and where it comes from (user, workspace overlay, or default criteria). Link the ICP page when there is one.
- **Default criteria:** company active; sector fit; size fit; no open collective procedure; recent growth, hiring or contract signals.
- **Score** each criterion: ✅ fit, 🟡 partial, ❌ no fit, ❔ unknown. The comment gives the evidence in one line.
- Size fit: assess the legal entity. If it belongs to a group (`categorie_entreprise` ETI or GE with a small headcount), also assess the group, as an Interpretation.
- Score a criterion ❔ when no ICP or no data allows it. With a ❔ criterion, the best verdict is "Pursue after checks".
- Do not score compute / buying pain ❔ if a CRM Lead or Activity already states it. Prefer **Fact (CRM)** over open-data silence.
- **Check before contact:** at most 5 checks the user must do first. Put the weakest evidence here. If the NAF is 70.10Z (head office or holding), say that the buyer can be a subsidiary.
- **Closed company:** if a BODACC "Ventes et cessions" notice names a buyer or an absorbing company (`acte.descriptif`), give it as the possible successor. Label it Fact, with the notice link.

A closed company, or one in liquidation on the as-of date, gets "Do not pursue". A company in sauvegarde or redressement gets "Hold" unless the ICP says otherwise.

## Hook

One to three sentences, ready to paste in an email. Write it after the qualification.

- Name the 2 or 3 strongest recent signals in concrete words (a project, a partner, a funding round).
- Connect them to the ICP pain that the product solves.
- If the CRM has a past exchange, refer to it (date, topic, contact).
- Use only signals from the Signals table. No new claim.

## Notion page

The body, in the user's language. Example headings in English:

```
## Brief — <AS_OF>
> 💡 Hook: <hook>                                   (callout)
### Interest signals
- <YYYY-MM-DD> · <type> · <signal, max 15 words> — [source](<link>)   (max 8, newest first)
### Qualification — ICP <link to the ICP page>      (page mention when the ICP is a Notion page)
**Verdict:** <verdict>
| ICP criterion | Score | Comment |
### Check before contact
1. <check>                                          (max 5)
```

- Signals: keep the ones that matter for the outreach. Fact and Fact (CRM) first; mark an Interpretation with "(interp.)".
- No Identity, Timeline, Claims, Retrieval log or Conflicts section in the body.

## Notion write

Follow `crm-ops` write discipline.

1. Read the current property values and body of the page. Show a preview of the body and of the new property values.
2. Wait for an explicit go.
3. Delete the previous `Brief — ` section of the body, if any. Then append the new body.
4. Fill only these properties: `SIREN`, `Sector`, `Size`, `Année effectif`, `CA`, `Résultat net`, `Marge nette %`, `Année financière`, `NAF`, `Forme juridique`, `Siège`, `Date de création`, `Dirigeant`, `Fiche registre`, `Verdict ICP`, `Dernier brief`.
5. Registry properties come only from a Fact. `NAF` is "<code> — <label>". `Siège` is "<postcode> <city>". `Dirigeant` is "<name> — <role>" of the first manager. `Fiche registre` is the annuaire-entreprises link. `Verdict ICP` is the verdict. `Dernier brief` is the as-of date.
6. `Année financière` is the fiscal year of `CA`, `Résultat net` and `Marge nette %`. `Année effectif` is the year of `Size`.
7. Properties hold the latest known value. Skip a property when the page already has an equal or newer year. A brief for a past date goes to the page body only.
8. A current value with no year (for example `Size` without `Année effectif`) may be human-entered. Show both values in the preview. Do not overwrite it unless the user chooses the new value.
9. For a select property (`Sector`, `Size`, `Verdict ICP`), read the live select options of the database first. If the mapped option does not exist, show the mapped value and the closest live options. Write only the option the user chooses.
10. If a property does not exist in the database, propose its name and type. Create it only after explicit validation. Types: `Année effectif` and `Année financière` are numbers; `CA` and `Résultat net` are euro numbers; `Marge nette %` is a percent number; `NAF`, `Forme juridique`, `Siège` and `Dirigeant` are text; `Date de création` and `Dernier brief` are dates; `Fiche registre` is a URL; `Verdict ICP` is a select (Pursue, Pursue after checks, Hold, Do not pursue).
