# Signals — scoring, dedup and composites

How to turn the records from `sources.md` into a short, ranked list of signals, and pick the main signal and its supporting signals. Apply it in this order:

1. Drop or fix records with "Corrections and annulments".
2. Merge records of the same event with "Cross-source dedup".
3. Set the procedure state with "Collective procedure states".
4. Compute the "Composite signals".
5. Give each signal its strength and window ("Strength and hook window").
6. Rank with "Priority".

## Dates

Each event has two dates:

- **Event date** — the fact itself: judgment date, deed date, meeting date, contract notification.
- **Public on** — the first publication, filing or release date.

Use the event date to merge records and to compute composites. Use max(event date, public on) to compute freshness. A fact found late stays usable for a short time ("we have just learned…").

## Corrections and annulments

BODACC publishes corrections ("Avis rectificatif") and annulments ("Avis d'annulation"). Read `typeavis_lib` and `parutionavisprecedent` on every notice.

- **Annulment** — find the original notice (`parutionavisprecedent`). Remove it and every signal or composite built on it. Never report it as a Fact.
- **Correction** — replace the original notice with the corrected one. Use the corrected values.
- **Several corrections** of the same notice: the latest one published on or before the as-of date wins.
- A correction or annulment published **after** the as-of date was not known on that date. Keep the original notice, and say so in "Conflicts and stale data".
- A correction does not reset the dates: the event date stays the judgment or deed date, and "public on" stays the first publication.
- If you cannot find the original notice, keep the correction and say so in "Conflicts and stale data".

## Cross-source dedup

One event gets one row in the Signals table, with every reference link. The source of truth gives the values; the other sources give freshness and links.

| Event type | Sources (usual order) | Source of truth | Same event when | Window |
|---|---|---|---|---|
| Creation | registry → BODACC creation → press | registry (date), BODACC (deed) | same SIREN | 45 days |
| Sale or transfer of a business | BODACC sale (provisional, then regular) → press | BODACC (price, parties) | same seller SIREN, or same buyer SIREN + same business address | 45 days |
| Manager change | BODACC change → press | BODACC | same SIREN + same person + same role + same direction (in or out) | 60 days |
| Capital increase | press → BODACC change | BODACC (new capital) | same SIREN + same new capital amount | 60 days |
| Head office move | BODACC change → registry | BODACC (event date) | same SIREN + same destination city | 45 days |
| Contract won | BOAMP or TED award → DECP | DECP (SIRET, amount, duration) | same SIREN + same buyer + similar subject. BOAMP and TED notices with the same buyer and subject are one award | 90 days |
| Collective procedure | BODACC → press | BODACC | same SIREN + same procedure state | 30 days |
| Merger | press (plan) → BODACC plan → BODACC completion | BODACC | same absorbing + absorbed SIREN. Plan and completion are two stages of one event | 120 days |
| Accounts filed | BODACC deposit, `ratios-inpi` | `ratios-inpi` | same SIREN + same fiscal year | none |
| Name or legal form change | BODACC change → registry | registry | same SIREN + same new value | 60 days |

Rules:

- Press "raised X M€" is the amount raised, not the share capital. It never merges with a capital increase by this table. It joins only through the composite "Confirmed funding".
- Two manager moves at the same meeting are two events: keep the person in the key. A person out and a person in, same role, same date, is one "replacement".
- **Same-date umbrella:** two or more changes with the same event date (manager, name, legal form, head office, capital) are one signal "articles overhaul". Its strength is the highest of its parts. A composite that uses these changes absorbs the umbrella.
- A BOAMP award without SIRET is an Interpretation. The DECP record with the SIRET makes it a Fact.
- Radiation (end of registration) and closure (end of activity) are two events, sometimes months apart. Never merge them.

## Collective procedure states

Map each BODACC "Procédures collectives" notice to one state. Read `jugement.nature` and `jugement.complementJugement`. One signal per change of state, never one per judgment. The event date is the judgment date (`jugement.date`), not `dateparution`.

If `nature` and `complementJugement` disagree (for example nature « plan de redressement », text « arrêtant le plan de sauvegarde »), use the text of the latest correction. If they still disagree, show both in "Conflicts and stale data" and use the state with the stricter verdict.

| State | Natures (verbatim fragments of `jugement.nature`) | Verdict effect |
|---|---|---|
| Conciliation | « homologation de l'accord », « résolution de l'accord homologué » | Hold |
| Sauvegarde | « ouverture d'une procédure de sauvegarde » and its follow-ups | Hold |
| Sauvegarde plan | « arrêtant le plan de sauvegarde », « modifiant le plan de sauvegarde » | Hold |
| Redressement | « ouverture d'une procédure de redressement judiciaire » and its follow-ups | Hold |
| Continuation plan | « plan de redressement », « modifiant le plan de redressement / de continuation », « plan de traitement de sortie de crise », « résolution du plan … » | Hold |
| Sale plan | « arrêtant un plan de cession », « modifiant le plan de cession » | Do not pursue the seller. The notice names the buyer: a new lead |
| Liquidation | « liquidation judiciaire » (opening, conversion, extension) | Do not pursue |
| Positive exit | « mettant fin à la procédure de sauvegarde / de redressement judiciaire », « clôture de la procédure de sauvegarde », « clôture pour extinction du passif » | Pursue: the company is saved |
| Negative closure | « clôture pour insuffisance d'actif », « reprise des poursuites individuelles », « clôture de la procédure de rétablissement professionnel » | Do not pursue: the company is dead |
| Retraction | « rétractation … sur tierce opposition », « arrêt de la cour d'appel infirmant » | Remove the state of the decision it names |
| Sanction of a manager | « interdiction de gérer », « faillite personnelle » | No change for the company. Never use it in a hook |
| Technical | appointments and replacements of court officers, extensions of the observation period | No change of state |

- While a difficulty state is active (conciliation to continuation plan), give no positive hook. The only exception is the composite "Exit from crisis".
- Use the latest state on the as-of date. An older difficulty followed by a positive exit is not a difficulty.
- If a nature fits no row (for example « autre jugement »), read the notice text. If it is still unclear, show it verbatim, treat it as a difficulty, and ask.

## Strength and hook window

Strength is the value of the signal to decide whom to call and what to say: 5 = trigger, 4 = strong, 3 = useful combined, 2 = weak alone, 1 = context, 0 = hygiene. The window is how long the signal can carry the hook, counted from max(event date, public on). After the window, the signal is context only.

Two windows are anchored on another date: "Contract renewal due" runs from 90 days before the contract end to the end; "Head office move" runs from 60 days before to 60 days after the move. Freshness is 1.0 at the start of the window.

| Signal | Source | Strength | Hook window |
|---|---|---|---|
| Contract renewal due (composite) | `decp` | 5 | 90 days before the end |
| Contract won | `decp`, `boamp`, `ted` | 5 | 30 days (15 days if found late) |
| Business bought (company is the buyer) | `bodacc` | 5 | 120 days |
| Business sold (company is the seller) | `bodacc` | 3 | 120 days |
| Business bought, seen at the buyer's registration (`origineFonds` "achat") | `bodacc` | 4 | 120 days |
| Collective procedure: change of state | `bodacc` | 4 | 120 days after the change |
| Capital increase | `bodacc` | 4 | 90 days |
| Manager change (legal representative: président, directeur général, gérant) | `bodacc` | 4 | 100 days |
| Board member change (administrateur, membre du conseil) | `bodacc` | 2 | — (context) |
| Statutory auditor appointed (growth past legal thresholds) | `bodacc` `listepersonnes.administration` | 4 | 90 days |
| Merger completed (external) | `bodacc` | 4 | 90 days |
| First public contract | `decp` | 4 | 45 days |
| Contract holder changed, or subcontracting declared | `decp` | 4 | 60 days |
| Revenue or result change between two fiscal years | `ratios-inpi` | 4 | 60 days after filing |
| Contract won (private), new site, funding, acquisition, public aid — press | `rss`, `web-search` | 4 | 90 days |
| EU R&D project started | `cordis` | 3 | 90 days |
| Public aid granted | `ademe` | 3 | 90 days |
| Lease-management started or ended | `bodacc` | 3 | 90–120 days |
| Head office move | `bodacc` | 3 | 60 days before to 60 days after |
| Name change | `bodacc` | 3 | 60 days |
| Capital reduction | `bodacc` | 3 | — (vigilance; read the reason: losses or share buyback) |
| Contract amended: more money or time | `decp` | 3 | 60 days |
| Press: certification, product launch, international expansion | `rss`, `web-search` | 3 | 60–90 days |
| Accounts filed | `bodacc`, `ratios-inpi` | 2 | 30 days |
| Open tender from the company as buyer | `boamp` | 2 | until the deadline |
| Continuation despite losses (L.225-248 / L.223-42) | `bodacc` | 2 | never alone: composite only |
| Radiation or closure | `bodacc`, registry | 1 | — (state: dead) |
| Press: anniversary, award, partnership | `rss`, `web-search` | 1 | 30–60 days |
| Routine change with no sales meaning | `bodacc` | 0 | — (drop) |

## Composite signals

A composite is two or more events that, together, mean more than each one. Its strength is never lower than the strongest of its parts, except where the composite exists to remove noise ("Internal merger", "Departure without replacement"). Compute only the composites whose inputs you have. A composite absorbs its parts: show it as one row and list the parts' links.

| Composite | Rule (condition window) | Why it is stronger | Strength | Hook window |
|---|---|---|---|---|
| Contract renewal due | DECP contract: `datenotification` + `dureemois` (use `dureemoismodification` when set) ends after the as-of date and within 120 days of it | Known date of a buying or rebidding decision. Not pre-computed anywhere: compute it | 5 | 90 days before the end |
| Confirmed funding | press "lève X" + BODACC capital increase within ±90 days | Press gives the amount and investors; BODACC proves it and kills name homonyms | 5 | 60 days after the BODACC notice |
| Full takeover | BODACC sale of the business + manager change (in) within 60 days | Business, control and the new decision-maker are all known | 5 | 120 days |
| First public contract | first DECP award ever seen for the SIREN + company younger than 5 years | New needs at once: advance payment, guarantee, compliance, staffing | 4 | 45 days |
| Contract machine | ≥ 3 awards (DECP, BOAMP or TED, after dedup) from ≥ 2 buyers within 180 days | A recurring public revenue engine and a visible order book | 4 | 180 days rolling |
| Contract ending, no follow-up | contract renewal due + no new award or tender from the same buyer with a similar subject (formal procedures only) | A predictable revenue gap at a known date | 3 | 90 days before the end |
| Contract lost | after the end, the same buyer awards a contract with a similar CPV code (`codecpv`) to another holder | Dated churn for the old holder; dated win for the new one | 4 | 60 days |
| Exit from crisis | procedure state "Sauvegarde plan", "Continuation plan" or "Positive exit" + (capital increase or new contract won) dated after that judgment and within 120 days of it | Blacklisted elsewhere; the new investment proves the rebound | 4 | 120 days |
| External growth | merger completed where the absorbed and the absorbing companies share no manager | Separates a real acquisition from a group clean-up | 4 | 90 days |
| Internal merger | merger completed where they share a manager | Group clean-up: no sales meaning | 1 | — |
| Replacement | manager out + manager in, same role, same date | A new decision-maker, and the old one is gone | 4 | 100 days |
| Departure without replacement | manager out, no manager in for 45 days | Never write "congratulations to the new manager" | 1 | — (vigilance) |
| Silent pre-distress | ≥ 2 within 12 months: continuation despite losses / capital reduction for losses / accounts not filed 7 months after the fiscal year end | Each marker is ambiguous alone; together they precede a procedure by 6–18 months | 3 | while true — verdict Hold |

Rules:

- **Similar subject:** same buyer and the same first 5 digits of `codecpv`, or the same key words in `objet`. Say which one you used.
- **Accounts not filed:** the fiscal year closed more than 7 months before the as-of date, and no BODACC "Dépôts des comptes" notice and no `ratios-inpi` row exists for it. Confidential filings still publish a BODACC deposit notice: a confidential filing is not a missing one.
- A press item is an Interpretation. Alone, it can never carry the hook at strength 5: only "Confirmed funding" can.
- Never infer age, health or a planned sale from a person's data. Never verbalise an inference about a person in the hook.

## Priority

Rank the signals that are inside their hook window:

`score = strength × freshness × confidence × specificity`

- **freshness** — 1.0 on the first day of the window, down to 0.3 on the last day, linear.
- **confidence** — Fact 1.0, Fact (company claim) 0.8, Interpretation 0.6.
- **specificity** — composite 1.3, single event 1.0, attribute (size, sector, revenue level) 0.7.

Then:

1. **Veto first,** before you rank. A company closed, in liquidation, or in an active difficulty state gets no positive hook (see "Collective procedure states"). Write the hook line as "No hook: <state> since <date>" and give the next date to check.
2. **One main signal:** the highest score. It is the reason to contact the company now, and the hook is built on it.
3. **Two or three supporting signals:** the next highest scores inside their window. Prefer signals of another type than the main signal: they add a second reason, not a repeat (two contracts won are one reason). If fewer than two qualify, show what exists; never fill the list with signals outside their window.
4. **Tie-break:** the newer signal, then the rarer one (a contract renewal beats a press award), then a composite over a single event.
5. **Cooldown:** if a CRM Activity of the last 90 days already used the same signal type as its hook, take the next signal. Say so in the preview.
6. Signals outside their window stay in the Signals table as context. Never use them as the main or a supporting signal.
