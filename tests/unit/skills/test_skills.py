"""Structure checks for the skill files. Skills are instructions, not code: these
tests catch broken links, missing frontmatter and malformed source entries."""

import json
import re
from pathlib import Path

import pytest
from notion_pilot_powers.core.siren_lookup import naf_section_to_sector, tranche_to_size

ROOT = Path(__file__).resolve().parents[3]
SKILL_FILES = [ROOT / "SKILL.md", *sorted((ROOT / "skills").glob("*/SKILL.md"))]
ENRICH = ROOT / "skills" / "company-enrichment"
SOURCES = ENRICH / "references" / "sources.md"
SOURCE_FIELDS = ("What it gives", "Query", "As-of filter", "Reference link", "Caveats")


def _frontmatter(path: Path) -> dict[str, str]:
    m = re.match(r"---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.DOTALL)
    assert m, f"{path} has no frontmatter"
    return dict(re.findall(r"^(\w[\w-]*):\s*(.*)$", m.group(1), re.MULTILINE))


def _sections(path: Path) -> dict[str, str]:
    parts = re.split(r"^## ", path.read_text(encoding="utf-8"), flags=re.MULTILINE)[1:]
    return {p.split("\n", 1)[0].strip(): p for p in parts}


@pytest.mark.parametrize("path", SKILL_FILES, ids=lambda p: p.parent.name)
def test_skill_has_name_and_description(path: Path) -> None:
    fm = _frontmatter(path)
    assert fm.get("name") == ("notion-pilot-powers" if path.parent == ROOT else path.parent.name)
    description = path.read_text(encoding="utf-8").split("description:", 1)[1].split("\n---", 1)[0]
    assert len(description.replace(">-", "").strip()) > 40


@pytest.mark.parametrize("path", SKILL_FILES, ids=lambda p: p.parent.name)
def test_skill_references_exist(path: Path) -> None:
    for ref in re.findall(r"`((?:references|evals)/[\w./-]+)`", path.read_text(encoding="utf-8")):
        assert (path.parent / ref).is_file(), f"{path} links missing {ref}"


def test_every_source_has_required_fields() -> None:
    sources = {k: v for k, v in _sections(SOURCES).items() if k.startswith("`")}
    expected = {"`recherche-entreprises`", "`bodacc`", "`boamp`", "`rss`", "`web-search`"}
    assert expected <= set(sources)
    for name, body in sources.items():
        for field in SOURCE_FIELDS:
            assert f"**{field}:**" in body, f"{name} lacks {field}"


def test_dated_queries_filter_on_as_of() -> None:
    sources = _sections(SOURCES)
    for name in ("`bodacc`", "`boamp`"):
        assert "dateparution <= date'<AS_OF>'" in sources[name] and "<SIREN>" in sources[name]


def test_headcount_table_matches_lookup_siren() -> None:
    rows = re.findall(
        r"^\| `(\w\w)` \| [^|]+ \| ([^|]*) \|$", SOURCES.read_text(encoding="utf-8"), re.MULTILINE
    )
    assert len(rows) == 16
    for code, size in rows:
        assert size.strip() == tranche_to_size(code), code


def test_sector_table_matches_lookup_siren() -> None:
    rows = re.findall(
        r"^\| `([A-U])` \| ([^|]+) \|$", SOURCES.read_text(encoding="utf-8"), re.MULTILINE
    )
    assert len(rows) == 19
    for section, sector in rows:
        assert sector.strip() == naf_section_to_sector(section), section


def test_brief_properties_are_documented_in_crm_ops() -> None:
    brief = (ENRICH / "references" / "brief.md").read_text(encoding="utf-8")
    line = next(ln for ln in brief.splitlines() if ln.startswith("4. Fill only these properties"))
    companies = (ROOT / "skills" / "crm-ops" / "references" / "companies.md").read_text(
        encoding="utf-8"
    )
    for prop in re.findall(r"`([^`]+)`", line):
        assert f"`{prop}`" in companies, prop


def test_rss_feeds_are_unique_https() -> None:
    rows = re.findall(
        r"^\| `([a-z][\w-]*)` \| [^|]+ \| (\S+) \|$",
        SOURCES.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    keys = [k for k, _ in rows]
    assert rows and len(keys) == len(set(keys))
    assert all(url.startswith("https://") for _, url in rows)


def test_brief_template_has_evidence_sections() -> None:
    text = (ENRICH / "references" / "brief.md").read_text(encoding="utf-8")
    for heading in (
        "Identity",
        "Timeline",
        "Claims",
        "Retrieval log",
        "Conflicts and stale data",
        "Lead qualification",
        "Notion write",
    ):
        assert f"## {heading}" in text
    assert "| Claim | Label | Source | Event date | Retrieved | Reference |" in text
    assert "birth date" in text
    for label in (
        "Fact",
        "Fact (company claim)",
        "Fact (current state)",
        "Interpretation",
        "Unknown",
    ):
        assert f"**{label}**" in text or f'"{label}"' in text, label


def test_evals_are_well_formed() -> None:
    data = json.loads((ENRICH / "evals" / "evals.json").read_text(encoding="utf-8"))
    assert data["skill_name"] == "company-enrichment"
    assert len(data["evals"]) >= 5
    for case in data["evals"]:
        assert case["prompt"] and case["expectations"]
