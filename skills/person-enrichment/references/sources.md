# Sources — person enrichment

Public data only. No source needs an API key or a login.

Each source has the same fields. To add a source, add one `## \`<id>\`` section with these five fields:

- **What it gives** — the data you can read.
- **Query** — the exact request. Replace `<name>`, `<company>`, `<email>`, `<domain>`.
- **As-of filter** — how to treat stale or current-only data.
- **Reference link** — the link to put in the claims table.
- **Caveats** — known limits. Read them before you write a claim.

Log every source in the retrieval log, also when you did not query it.

## `crm`

**What it gives:** existing People (email, LinkedIn, Position, Company), linked Leads and Activities that name the person.

**Query:** Notion MCP search / query People by email, then LinkedIn URL, then name + company. Local MCP: `search_people`. Also read Company → related People.

**As-of filter:** CRM is current state. Label `Fact (CRM)`.

**Reference link:** the Notion page URL.

**Caveats:** Upsert skip on exact match does not fill empty LinkedIn/position — patch missing fields after match. Never create a second Person for the same email.

## `company-site`

**What it gives:** name, role/title, team, sometimes email or LinkedIn, on the employer's public pages (`/equipe`, `/team`, `/about`, `/contact`).

**Query:** find the official site (from Company page, email domain, or web search). Open team and contact pages. Match `<name>` or email local-part.

**As-of filter:** current state unless the page shows a date.

**Reference link:** deep link to the team or bio page.

**Caveats:** Label titles here **Fact (company claim)**. A missing person on the team page is not proof they left. Do not invent a page URL.

## `linkedin-public`

**What it gives:** public headline, current role, company, profile URL — only what is visible without login.

**Query:** web search `site:linkedin.com/in "<full name>" "<company>"` or the URL the user gave. Open only public results.

**As-of filter:** current state. Prefer a profile that lists the same employer as the clue.

**Reference link:** the `linkedin.com/in/...` URL you opened.

**Caveats:** Never invent a slug from the name. If search returns several profiles, list them and ask. Login wall or empty public view → log `not available`, leave LinkedIn empty. Do not use Sales Navigator or scraped dumps.

## `recherche-entreprises`

**What it gives:** `dirigeants` (legal managers) for a SIREN — name and role only.

**Query:** `https://recherche-entreprises.api.gouv.fr/search?q=<SIREN>&per_page=5` (or `lookup_siren`). Match `<name>` against `dirigeants`.

**As-of filter:** current RNE state. Label "current state".

**Reference link:** `https://annuaire-entreprises.data.gouv.fr/entreprise/<SIREN>`

**Caveats:** Managers only — most employees are absent. Never copy birth date or nationality if present in the payload. Name match without company corroboration stays Interpretation.

## `web-search`

**What it gives:** conference bios, press quotes, GitHub/org pages, speaker lists that state role and employer.

**Query:** `"<full name>" "<company>"` and `"<email>"` when known. Prefer primary sources over aggregators.

**As-of filter:** drop items clearly about a different employer or dated after a known departure (if evidenced).

**Reference link:** the article or bio URL.

**Caveats:** Press is Interpretation unless it quotes the company site. Skip data-broker and people-search sites (ZoomInfo, Pappers people paywall dumps used as profile stores, etc.). Prefer official domain and LinkedIn public hits.
