# Sources — lead brief

Open data only. No source needs an API key.

Each source has the same fields. To add a source, add one `## \`<id>\`` section with these five fields:

- **What it gives** — the data you can read.
- **Query** — the exact request. Replace `<SIREN>`, `<name>` and `<AS_OF>` (YYYY-MM-DD). URL-encode the `where` value, for example with `curl -G --data-urlencode`.
- **As-of filter** — how to drop data that was not known on the as-of date.
- **Reference link** — the link to put in the claims table.
- **Caveats** — known limits. Read them before you write a claim.

Log every source in the retrieval log, also when you did not query it. Read every returned record, not only the first ones.

## `recherche-entreprises`

**What it gives:**
- Identity: legal name, SIREN, head office, NAF code, legal form, `categorie_entreprise`.
- State: `etat_administratif` (A = active, C = closed), `date_creation`, `date_fermeture`.
- Size and money: `tranche_effectif_salarie` with `annee_tranche_effectif_salarie`, `finances` by fiscal year (`ca`, `resultat_net`).
- People: `dirigeants`, `date_mise_a_jour_rne`. Manager data comes from the RNE through this API.

**Query:** `https://recherche-entreprises.api.gouv.fr/search?q=<SIREN>&per_page=5`. For a name: `q=<name>`. The local MCP tool `lookup_siren` runs the name search.

**As-of filter:** the API gives the current state only.
- Use the company `date_creation`, not the date of an establishment. If it is after the as-of date, the company did not exist. Stop.
- If `date_fermeture` is on or before the as-of date, the company was closed.
- Use `finances` years before the as-of year only. Always give the fiscal year with the value.
- Always give the headcount band with `annee_tranche_effectif_salarie`. If the year is missing, say so.
- If that year is on or after the as-of year, label the band "current state, after the as-of date". Do not use it to qualify the lead.
- Label managers, address and NAF "current state" when the as-of date is before today.
- `categorie_entreprise` (PME, ETI, GE) is computed at group level. A small headcount with ETI or GE means the company belongs to a larger group. Say so in "Conflicts and stale data"; do not call it a conflict about size.

**Headcount codes** (`tranche_effectif_salarie`). Write the INSEE band in the brief. Use the `Size` option for Notion. The option is approximate: it matches `lookup_siren`. Leave `Size` empty for `NN`.

| code | INSEE band | Size option |
|---|---|---|
| `NN` | unknown |  |
| `00` | 0 | 1-10 |
| `01` | 1-2 | 1-10 |
| `02` | 3-5 | 1-10 |
| `03` | 6-9 | 1-10 |
| `11` | 10-19 | 11-50 |
| `12` | 20-49 | 11-50 |
| `21` | 50-99 | 51-200 |
| `22` | 100-199 | 51-200 |
| `31` | 200-249 | 201-500 |
| `32` | 250-499 | 201-500 |
| `41` | 500-999 | 501-2000 |
| `42` | 1000-1999 | 501-2000 |
| `51` | 2000-4999 | 2001-10000 |
| `52` | 5000-9999 | 2001-10000 |
| `53` | 10000+ | 10000+ |

**Sector** (from the NAF section letter, as `lookup_siren` does). These are the options the Notion Pilot wizard creates. A live database can use other options: see "Notion write" in `brief.md`. J: `Telecom` if the NAF code starts with 61, else `Software`. M: `Research` if it starts with 72, else `Consulting`.

| NAF section | Sector option |
|---|---|
| `A` | Industry |
| `B` | Industry |
| `C` | Industry |
| `D` | Energy |
| `E` | Energy |
| `F` | Industry |
| `G` | Other |
| `H` | Industry |
| `I` | Other |
| `K` | Finance |
| `L` | Other |
| `N` | Consulting |
| `O` | Public Sector |
| `P` | Public Sector |
| `Q` | Public Sector |
| `R` | Other |
| `S` | Other |
| `T` | Other |
| `U` | Other |

**Reference link:** `https://annuaire-entreprises.data.gouv.fr/entreprise/<SIREN>`

**Caveats:**
- Copy the manager name and role only. Never copy a birth date or a nationality.
- `finances` gives the fiscal year, not the filing date. Check the BODACC "Dépôts des comptes" notices. If the deposit of that year is after the as-of date, label the value "probably not public on the as-of date".
- The INPI RNE API needs an account. It is out of scope.

## `bodacc`

**What it gives:** official legal notices: creations, changes, sales and transfers, collective procedures, conciliation, deregistrations, accounts filings.

**Query:** `https://bodacc-datadila.opendatasoft.com/api/explore/v2.1/catalog/datasets/annonces-commerciales/records?where=registre like "<SIREN>" and dateparution <= date'<AS_OF>'&order_by=dateparution desc&limit=20&select=id,dateparution,familleavis_lib,typeavis_lib,tribunal,jugement,acte,url_complete`

**As-of filter:** `dateparution <= date'<AS_OF>'` in the query. The event date is `dateparution` (publication date).

**Second query:** to check procedures beyond the 20 newest notices, run the same query with `and (familleavis_lib in ("Procédures collectives","Procédures de conciliation","Ventes et cessions","Radiations") or familleavis_lib is null)`.

**Reference link:** `url_complete` of each notice.

**Caveats:**
- The judgment date inside `jugement` can be earlier than `dateparution`. Give both when they differ.
- `familleavis_lib` values: Créations, Immatriculations, Modifications diverses, Ventes et cessions, Procédures collectives, Procédures de conciliation, Procédures de rétablissement professionnel, Radiations, Dépôts des comptes, Annonces diverses.
- For "Ventes et cessions", read `acte.descriptif`. It names the other party: buyer, or absorbing company in a merger.
- A "Procédures collectives" notice is a Fact about the procedure. Read `jugement` for its type (sauvegarde, redressement, liquidation, plan, clôture).
- `total_count` above 20 means older notices exist. Say so.
- BODACC covers companies in the trade register. Public bodies and most associations are not in it. For them, log BODACC "not applicable", not "empty".

## `boamp`

**What it gives:** public procurement notices: buyer, subject, winners (`titulaire`), publication date.

**Query:** `https://boamp-datadila.opendatasoft.com/api/explore/v2.1/catalog/datasets/boamp/records?where=search(donnees,"<SIREN>") and dateparution <= date'<AS_OF>'&order_by=dateparution desc&limit=20&select=idweb,dateparution,nature_libelle,objet,nomacheteur,titulaire,url_avis`

**As-of filter:** `dateparution <= date'<AS_OF>'` in the query.

**Reference link:** `url_avis` of each notice.

**Caveats:**
- The search is full text. The SIREN can be the buyer, a winner, or an unrelated number.
- Compare `nomacheteur` and `titulaire` with the legal name. Label the role: buyer, winner, or unclear.
- Count a notice as a won contract only when the company is in `titulaire` and `nature_libelle` is a result ("Résultat de marché").
- When the company is the buyer, report its purchases as a separate signal: it buys these services. Never call them contracts won.
- A gap in dates can come from the dataset, not from the company. Say so. Do not conclude "no activity".
- A search by name (`search(titulaire,"<name>")`) is an Interpretation, never a Fact.
- **BOAMP empty ≠ no tender.** Private RFPs, partner-led bids and co-selling deals do not appear here. Check `crm` before you say there is no procurement activity.

## `crm`

**What it gives:** prior CRM knowledge for this company — Leads (stage, product, next step, notes), Activities (meetings, outcomes), Meetings, and related People. Often the only evidence of compute needs, private RFPs, or partners (for example a cloud partner).

**Query:** when a Notion Company page (or company name in the CRM) is in scope:
1. Search the workspace for the company name and SIREN.
2. Open every Lead whose Client/Company relation is this company.
3. Open linked Activities and Meetings (and any Meeting pages that mention the company).
4. Read Stage, Product, Next Step, Notes, and activity Notes/Outcome.

**As-of filter:** keep events dated on or before the as-of date. Undated CRM notes are "date unknown"; still use them for qualification, labelled accordingly.

**Reference link:** the Notion URL of the Lead, Activity or Meeting.

**Caveats:**
- Label CRM rows **Fact (CRM)** when the claim is written in the CRM record. User statements in the current chat that are not in the CRM are Interpretation (or Fact if the user asks you to treat them as given).
- Never mark a buying need, compute/HPC need, RFP or partner relationship **Unknown** until you have queried `crm` (or logged it `not available` / `not applicable`).
- An empty BOAMP or RSS result does not cancel a CRM Lead or Activity on the same topic.

## `rss`

**What it gives:** recent French business press items.

**Query:** fetch each feed in the table. Keep items whose title or description contains the legal name, the brand name or the SIREN.

| key | name | url |
|---|---|---|
| `jde_france` | JDE — France | https://www.lejournaldesentreprises.com/rss-france |
| `jde_ara` | JDE — Auvergne-Rhône-Alpes | https://www.lejournaldesentreprises.com/rss-auvergne-rhone-alpes |
| `jde_pdl` | JDE — Pays de la Loire | https://www.lejournaldesentreprises.com/rss-pays-de-la-loire |
| `latribune_eco` | La Tribune — Économie | https://www.latribune.fr/rss/rubriques/economie-2 |
| `fusacq_buzz` | Fusacq Buzz | https://flux.fusacq.com/rss-fusacq-buzz.xml |
| `agefi_restructurations` | AGEFI — Restructurations | https://www.agefi.fr/theme/restructurations.rss |
| `maddyness` | Maddyness | https://www.maddyness.com/feed/ |
| `actufr_eco` | actu.fr — Économie | https://actu.fr/economie/rss.xml |

To add a feed, add one row.

**As-of filter:** keep items with `pubDate` on or before the as-of date. If the as-of date is more than 3 months before today, do not fetch the feeds: log "not applicable".

**Reference link:** the item `link`.

**Caveats:**
- Feeds hold recent items only: from a few days to a few months.
- If the oldest item of a feed is after the as-of date, log the feed "not applicable". Do not write "no news".
- A name match is an Interpretation. Homonyms are frequent.

## `web-search`

**What it gives:** press, company pages, announcements not in the official sources.

**Query:** first find the official website: `"<name>" <NAF activity label>`, for example `"Calogena" ingénierie énergie`. Then `"<name>" <SIREN>` and `"<name>" <head office city>`. A name alone often returns homonyms.

**As-of filter:** keep results with a visible publication date on or before the as-of date. Drop results without a date, or log them as "date unknown".

**Reference link:** the page URL.

**Caveats:**
- A result is an Interpretation unless it is an official source. A statement on the company's own page is a "Fact (company claim)".
- Search tools often show no date. Open the page to find its date. No dated page, no claim.
- Ignore the search tool's summary text. It can contain events after the as-of date.
- Check that the page names the same company (SIREN, city or activity).
