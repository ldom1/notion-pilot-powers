# Sources — lead brief

Open data only. Every automated source works without authentication: no account, no API key. Sources that need an account (INPI RNE, INPI patents and trademarks, France Travail) are out of scope.

Each source has the same fields. To add a source, add one `## \`<id>\`` section with these five fields:

- **What it gives** — the data you can read.
- **Query** — the exact request. Replace `<SIREN>`, `<name>` and `<AS_OF>` (YYYY-MM-DD). URL-encode the `where` value, for example with `curl -G --data-urlencode`.
- **As-of filter** — how to drop data that was not known on the as-of date.
- **Reference link** — the link to put in the signals table.
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
- **BOAMP empty ≠ no tender.** Also check `decp` and `ted`. Private RFPs, partner-led bids and co-selling deals do not appear here. Check `crm` before you say there is no procurement activity.

## `decp`

**What it gives:** public contracts awarded, from the buyers' own data (DECP): subject, buyer, amount, procedure, notification date. It also covers contracts below the BOAMP threshold.

**Query:** `https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/decp-v3-marches-valides/records?where=((titulaire_id_1>=<SIREN>00000 and titulaire_id_1<<SIREN+1>00000) or startswith(titulaire_id_2,"<SIREN>") or (titulaire_id_3>=<SIREN>00000 and titulaire_id_3<<SIREN+1>00000)) and datenotification <= date'<AS_OF>'&order_by=datenotification desc&limit=20&select=id,datenotification,objet,montant,acheteur_id,acheteur_nom,nature,procedure`

`<SIREN+1>` is the SIREN plus one, as a number. `titulaire_id_1` and `titulaire_id_3` are numbers, `titulaire_id_2` is text: keep the query as written. For contracts the company buys, run `where=startswith(acheteur_id,"<SIREN>") and datenotification <= date'<AS_OF>'`.

**As-of filter:** `datenotification <= date'<AS_OF>'` in the query.

**Reference link:** `https://data.economie.gouv.fr/explore/dataset/decp-v3-marches-valides/table/?q=<id>`

**Caveats:**
- `acheteur_nom` is often null. Give `acheteur_id` (SIRET) and resolve the name with `recherche-entreprises` when it matters.
- Buyers publish late or not at all. Empty does not mean no public contract.
- When the company is the buyer, report its purchases as a separate signal. Never call them contracts won.

## `ted`

**What it gives:** EU public procurement notices above the EU thresholds, from all member states: contract awards, winners, buyers.

**Query:** `POST https://api.ted.europa.eu/v3/notices/search` with the JSON body `{"query": "winner-name = \"<name>\" AND publication-date <= <AS_OF as YYYYMMDD> SORT BY publication-date DESC", "fields": ["publication-number", "publication-date", "notice-type", "notice-title", "buyer-name", "winner-name"], "limit": 20}`. For notices where the company buys, use `buyer-name = "<name>"`.

**As-of filter:** `publication-date <= <AS_OF>` in the query.

**Reference link:** `https://ted.europa.eu/fr/notice/-/detail/<publication-number>`

**Caveats:**
- The search is by name: a match is an Interpretation until the notice gives the SIREN or the address.
- Use `=` (exact phrase), never `~`: `~` stems the name and returns unrelated notices.
- Try the legal name and the brand name. Notices write names with different case and suffixes ("SAS").

## `cordis`

**What it gives:** EU-funded R&D projects (Horizon 2020, Horizon Europe) in which the company is a participant or coordinator: acronym, title, start and end dates.

**Query:** SPARQL `GET https://cordis.europa.eu/datalab/sparql?query=<query>` with `Accept: application/sparql-results+json`:

```sparql
PREFIX eurio:<http://data.europa.eu/s66#>
SELECT ?id ?acr ?title ?start ?end WHERE {
  ?org eurio:vatNumber ?vat . FILTER(STRENDS(?vat, "<SIREN>"))
  ?role eurio:isRoleOf ?org . ?p eurio:hasInvolvedParty ?role ;
     eurio:identifier ?id ; eurio:startDate ?start .
  OPTIONAL { ?p eurio:hasAcronym/eurio:shortForm ?acr }
  OPTIONAL { ?p eurio:title ?title } OPTIONAL { ?p eurio:endDate ?end }
  FILTER(?start <= "<AS_OF>"^^xsd:date)
} ORDER BY DESC(?start) LIMIT 20
```

**As-of filter:** `?start <= <AS_OF>` in the query.

**Reference link:** `https://cordis.europa.eu/project/id/<id>`

**Caveats:**
- The French VAT number ends with the SIREN. Some organisations have no VAT number in CORDIS: then log `empty` and say so.
- A project gives R&D themes and partners. It is a Fact about the participation, an Interpretation about a buying need.

## `ratios-inpi`

**What it gives:** filed annual accounts by fiscal year: revenue (`chiffre_d_affaires`), net result (`resultat_net`). Often more years than `recherche-entreprises` `finances`.

**Query:** `https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/ratios_inpi_bce/records?where=siren="<SIREN>" and date_cloture_exercice < date'<AS_OF>'&order_by=date_cloture_exercice desc&limit=5`

**As-of filter:** `date_cloture_exercice < date'<AS_OF>'` in the query. Accounts are filed months after the closing date: apply the BODACC "Dépôts des comptes" check of `recherche-entreprises`.

**Reference link:** `https://annuaire-entreprises.data.gouv.fr/donnees-financieres/<SIREN>`

**Caveats:**
- Companies can file confidential accounts. Then the dataset is empty: log `empty`, not "no revenue".
- `marge_nette` is often null. Compute `Marge nette %` from `resultat_net / chiffre_d_affaires` when both exist.
- Growth over 2 years or more is a signal (type accounts).

## `ademe`

**What it gives:** ADEME financial aid granted to the company (energy, climate, industry, mobility, buildings, circular economy): project subject, amount, aid scheme, agreement date.

**Query:** `https://data.ademe.fr/data-fair/api/v1/datasets/les-aides-financieres-de-l'ademe/lines?qs=idBeneficiaire:<SIREN>* AND dateConvention:<=<AS_OF>&sort=-dateConvention&size=20&select=dateConvention,objet,montant,dispositifAide,referenceDecision,nomBeneficiaire`

**As-of filter:** `dateConvention:<=<AS_OF>` in the query.

**Reference link:** `https://data.ademe.fr/datasets/les-aides-financieres-de-l'ademe` and the `referenceDecision`.

**Caveats:**
- The dataset covers about the last three years of agreements.
- An aid is a Fact about a funded project. It is not proof of revenue or of a buying need, and the project can be finished on the as-of date.

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
