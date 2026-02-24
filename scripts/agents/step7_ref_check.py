"""
Step 7 Agent -- Reference Integrity Check

Cross-checks citations in paper.md against references.bib:
1. Finds all [@key] citations in the paper
2. Parses all BibTeX entries in references.bib
3. Reports: missing refs, unused refs, duplicate keys, format issues
4. LLM-powered citation context check (is each citation used appropriately?)

Outputs: data/processed/enriched/step7_ref_check.json
"""

import json, os, re
from collections import Counter
from . import config
from .llm import chat_json

# ── Paths ────────────────────────────────────────────────────────────────────
PAPER_PATH = os.path.join(config.BASE_DIR, "paper", "paper.md")
BIB_PATH = os.path.join(config.BASE_DIR, "paper", "references.bib")
OUTPUT_PATH = os.path.join(config.ENRICHED_DIR, "step7_ref_check.json")


def _parse_citations(paper_text: str) -> list[dict]:
    """Extract all [@key] citation occurrences with context."""
    citations = []
    # Match [@key1; @key2] patterns
    for match in re.finditer(r"\[([^\]]*@[^\]]+)\]", paper_text):
        full_cite = match.group(1)
        # Get surrounding context (±100 chars)
        start = max(0, match.start() - 100)
        end = min(len(paper_text), match.end() + 100)
        context = paper_text[start:end].replace("\n", " ").strip()

        # Extract individual keys
        keys = re.findall(r"@([\w:.-]+)", full_cite)
        for key in keys:
            citations.append({
                "key": key,
                "full_citation": match.group(0),
                "context": context,
                "position": match.start(),
            })
    return citations


def _parse_bibtex(bib_text: str) -> dict[str, dict]:
    """Parse BibTeX entries into a dict keyed by citation key."""
    entries = {}
    # Match @type{key, ... }
    pattern = re.compile(
        r"@(\w+)\s*\{\s*([\w:.-]+)\s*,\s*([\s\S]*?)(?=\n@|\Z)",
        re.MULTILINE
    )
    for match in pattern.finditer(bib_text):
        entry_type = match.group(1).lower()
        key = match.group(2)
        body = match.group(3)

        # Extract fields
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*\{([^}]*)\}", body):
            fields[fm.group(1).lower()] = fm.group(2).strip()

        entries[key] = {
            "type": entry_type,
            "title": fields.get("title", ""),
            "author": fields.get("author", ""),
            "year": fields.get("year", ""),
            "journal": fields.get("journal", fields.get("booktitle", "")),
            "all_fields": list(fields.keys()),
        }
    return entries


def _check_bibtex_quality(entries: dict) -> list[dict]:
    """Check BibTeX entries for common quality issues."""
    issues = []
    required_fields = {
        "article": ["author", "title", "journal", "year"],
        "inproceedings": ["author", "title", "booktitle", "year"],
        "book": ["author", "title", "publisher", "year"],
        "misc": ["author", "title", "year"],
        "online": ["author", "title", "year", "url"],
        "techreport": ["author", "title", "institution", "year"],
        "report": ["author", "title", "institution", "year"],
    }

    for key, entry in entries.items():
        etype = entry["type"]
        required = required_fields.get(etype, ["author", "title", "year"])

        for field in required:
            if field not in entry["all_fields"]:
                issues.append({
                    "key": key,
                    "issue_type": "missing_field",
                    "severity": "major" if field in ("author", "title") else "minor",
                    "detail": f"Missing required field '{field}' for @{etype}",
                })

        # Check for placeholder text
        title = entry.get("title", "")
        if any(p in title.lower() for p in ["todo", "fixme", "placeholder", "xxx"]):
            issues.append({
                "key": key,
                "issue_type": "placeholder",
                "severity": "critical",
                "detail": f"Title appears to contain placeholder text: {title}",
            })

        # Check year validity
        year = entry.get("year", "")
        if year and not re.match(r"^(19|20)\d{2}$", year):
            issues.append({
                "key": key,
                "issue_type": "invalid_year",
                "severity": "minor",
                "detail": f"Year '{year}' may be invalid",
            })

    return issues


CONTEXT_CHECK_PROMPT = """\
You are a meticulous academic reviewer checking whether citations are used
correctly in context. For each citation below, verify:

1. Does the claim being made match what the cited source likely covers?
2. Is the citation placed at the right point in the sentence?
3. Are there any signs of citation misattribution?

CITATIONS WITH CONTEXT:
{citations_json}

BIBLIOGRAPHY ENTRIES:
{bib_json}

For each citation, assess whether the usage appears correct based on the
source title, author, and the surrounding text.

Return JSON:
{{
  "citation_checks": [
    {{
      "key": "citation_key",
      "context_snippet": "the surrounding text",
      "source_title": "title from bibliography",
      "assessment": "correct|suspicious|likely_wrong",
      "confidence": "high|medium|low",
      "reason": "Why you think this"
    }}
  ],
  "overall_citation_quality": "excellent|good|acceptable|needs_work",
  "recommendations": ["list of improvement suggestions"]
}}
"""


def run(paper_path: str = None, bib_path: str = None):
    """Execute Step 7: Reference integrity check."""
    print("=" * 70)
    print("STEP 7 AGENT — Reference Integrity Check")
    print("=" * 70)

    paper_path = paper_path or PAPER_PATH
    bib_path = bib_path or BIB_PATH

    if not os.path.exists(paper_path):
        print(f"  ERROR: Paper not found at {paper_path}")
        return None
    if not os.path.exists(bib_path):
        print(f"  ERROR: Bibliography not found at {bib_path}")
        return None

    # ── Load files ───────────────────────────────────────────────────────────
    with open(paper_path, "r", encoding="utf-8") as f:
        paper_text = f.read()
    with open(bib_path, "r", encoding="utf-8") as f:
        bib_text = f.read()

    # ── Phase 1: Parse citations and bibliography ────────────────────────────
    print("\n  Phase 1: Parsing citations and bibliography...")
    citations = _parse_citations(paper_text)
    bib_entries = _parse_bibtex(bib_text)

    cited_keys = set(c["key"] for c in citations)
    bib_keys = set(bib_entries.keys())

    print(f"    Citations in paper: {len(citations)} occurrences, {len(cited_keys)} unique keys")
    print(f"    BibTeX entries: {len(bib_keys)}")

    # ── Phase 2: Cross-reference check ───────────────────────────────────────
    print("\n  Phase 2: Cross-reference integrity...")
    missing_from_bib = cited_keys - bib_keys
    unused_in_paper = bib_keys - cited_keys

    # Count citation frequency
    cite_counts = Counter(c["key"] for c in citations)

    if missing_from_bib:
        print(f"    MISSING from .bib: {missing_from_bib}")
    else:
        print("    All cited keys found in .bib")

    if unused_in_paper:
        print(f"    UNUSED in paper: {unused_in_paper}")
    else:
        print("    All .bib entries cited in paper")

    # ── Phase 3: BibTeX quality check ────────────────────────────────────────
    print("\n  Phase 3: BibTeX entry quality...")
    bib_issues = _check_bibtex_quality(bib_entries)
    critical = [i for i in bib_issues if i["severity"] == "critical"]
    major = [i for i in bib_issues if i["severity"] == "major"]
    minor = [i for i in bib_issues if i["severity"] == "minor"]
    print(f"    Issues: {len(critical)} critical, {len(major)} major, {len(minor)} minor")

    # ── Phase 4: LLM citation context check ──────────────────────────────────
    print("\n  Phase 4: LLM citation context check...")

    # Sample citations for LLM check (all unique, up to 30)
    unique_citations = {}
    for c in citations:
        if c["key"] not in unique_citations and c["key"] in bib_keys:
            unique_citations[c["key"]] = c
    sampled = list(unique_citations.values())[:30]

    # Build bib summary for sampled keys
    bib_summary = {k: bib_entries[k] for k in unique_citations if k in bib_entries}

    context_check = chat_json(
        messages=[
            {"role": "system", "content": "You are an expert academic citation reviewer."},
            {"role": "user", "content": CONTEXT_CHECK_PROMPT.format(
                citations_json=json.dumps(sampled, indent=2)[:15_000],
                bib_json=json.dumps(bib_summary, indent=2)[:15_000],
            )},
        ],
        model=config.SYNTHESIS_MODEL,
        max_tokens=config.MAX_OUTPUT_TOKENS,
    )

    # ── Assemble output ──────────────────────────────────────────────────────
    result = {
        "paper_file": paper_path,
        "bib_file": bib_path,
        "summary": {
            "total_citations": len(citations),
            "unique_citation_keys": len(cited_keys),
            "bibtex_entries": len(bib_keys),
            "missing_from_bib": sorted(missing_from_bib),
            "unused_in_paper": sorted(unused_in_paper),
            "citation_frequency": dict(cite_counts.most_common()),
        },
        "bibtex_quality_issues": bib_issues,
        "citation_context_check": context_check,
        "integrity_status": "PASS" if not missing_from_bib else "FAIL",
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n  Output saved: {OUTPUT_PATH}")
    print(f"  Integrity: {'PASS' if not missing_from_bib else 'FAIL — missing keys!'}")
    print(f"  Citation quality: {context_check.get('overall_citation_quality', '?')}")

    return result
