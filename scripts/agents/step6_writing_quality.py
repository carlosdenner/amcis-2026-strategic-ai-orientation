"""
Step 6 Agent -- Writing Quality & Readability Audit

Performs an automated quality review of paper.md:
1. Readability metrics (Flesch-Kincaid, Gunning Fog, sentence stats)
2. Passive voice detection & percentage
3. Academic tone and clarity assessment (LLM-powered)
4. Section-by-section feedback with concrete edits
5. Overall publishability assessment

Outputs: data/processed/enriched/step6_writing_quality.json
"""

import json, os, re, math
from collections import Counter
from . import config
from .llm import chat_json

# ── Paths ────────────────────────────────────────────────────────────────────
PAPER_PATH = os.path.join(config.BASE_DIR, "paper", "paper.md")
OUTPUT_PATH = os.path.join(config.ENRICHED_DIR, "step6_writing_quality.json")

# ── Readability helpers ──────────────────────────────────────────────────────

def _strip_markdown(text: str) -> str:
    """Remove YAML front-matter, markdown formatting, tables, and code fences."""
    # Remove YAML front matter
    text = re.sub(r"^---[\s\S]*?---", "", text)
    # Remove code fences
    text = re.sub(r"```[\s\S]*?```", "", text)
    # Remove tables (lines starting with |)
    text = re.sub(r"^\|.*$", "", text, flags=re.MULTILINE)
    # Remove image references
    text = re.sub(r"!\[.*?\]\(.*?\)(\{.*?\})?", "", text)
    # Remove citation keys
    text = re.sub(r"\[@[\w;, ]+\]", "", text)
    # Remove markdown headers but keep text
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Remove bold/italic markers
    text = re.sub(r"[*_]{1,3}", "", text)
    # Remove HTML comments
    text = re.sub(r"<!--[\s\S]*?-->", "", text)
    # Remove reference divs
    text = re.sub(r":::\s*\{#refs\}[\s\S]*?:::", "", text)
    # Collapse whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _sentences(text: str) -> list[str]:
    """Split text into sentences (simple heuristic)."""
    # Split on period/question/exclamation followed by space or end
    sents = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sents if len(s.strip()) > 10]


def _words(text: str) -> list[str]:
    """Extract words."""
    return re.findall(r"[a-zA-Z']+", text)


def _syllable_count(word: str) -> int:
    """Estimate syllable count for a word."""
    word = word.lower().strip()
    if len(word) <= 3:
        return 1
    # Remove trailing e
    if word.endswith("e"):
        word = word[:-1]
    # Count vowel groups
    count = len(re.findall(r"[aeiouy]+", word))
    return max(1, count)


def _compute_readability(text: str) -> dict:
    """Compute readability metrics from plain text."""
    sents = _sentences(text)
    words = _words(text)
    if not sents or not words:
        return {"error": "Insufficient text for analysis"}

    n_sentences = len(sents)
    n_words = len(words)
    n_syllables = sum(_syllable_count(w) for w in words)
    n_complex = sum(1 for w in words if _syllable_count(w) >= 3)

    # Average sentence length
    avg_sent_len = n_words / n_sentences
    avg_syll_per_word = n_syllables / n_words

    # Flesch Reading Ease (higher = easier)
    flesch_re = 206.835 - 1.015 * avg_sent_len - 84.6 * avg_syll_per_word

    # Flesch-Kincaid Grade Level
    fk_grade = 0.39 * avg_sent_len + 11.8 * avg_syll_per_word - 15.59

    # Gunning Fog Index
    fog = 0.4 * (avg_sent_len + 100 * (n_complex / n_words))

    # Sentence length distribution
    sent_lengths = [len(_words(s)) for s in sents]
    long_sents = [s for s in sents if len(_words(s)) > 40]

    return {
        "total_words": n_words,
        "total_sentences": n_sentences,
        "avg_sentence_length": round(avg_sent_len, 1),
        "median_sentence_length": sorted(sent_lengths)[len(sent_lengths) // 2],
        "max_sentence_length": max(sent_lengths),
        "sentences_over_40_words": len(long_sents),
        "flesch_reading_ease": round(flesch_re, 1),
        "flesch_kincaid_grade": round(fk_grade, 1),
        "gunning_fog_index": round(fog, 1),
        "complex_word_pct": round(100 * n_complex / n_words, 1),
        "interpretation": _interpret_readability(flesch_re, fk_grade, fog),
    }


def _interpret_readability(fre: float, fk: float, fog: float) -> str:
    """Interpret readability scores for academic context."""
    notes = []
    # Academic papers typically score 20-40 Flesch RE
    if fre < 10:
        notes.append("Very difficult to read — even for academic standards. Consider simplifying some sentences.")
    elif fre < 30:
        notes.append("Difficult — typical for academic papers. Acceptable for AMCIS.")
    elif fre < 50:
        notes.append("Moderately difficult — slightly more accessible than typical IS papers.")
    else:
        notes.append("Fairly easy — may lack academic sophistication.")

    if fk > 18:
        notes.append(f"FK grade {fk} is very high; consider breaking long sentences.")
    elif fk > 14:
        notes.append(f"FK grade {fk} is typical for academic IS writing.")

    if fog > 20:
        notes.append(f"Fog index {fog} is very high — reduce jargon density in key passages.")
    return " ".join(notes)


def _detect_passive_voice(text: str) -> dict:
    """Detect passive voice constructions."""
    # Pattern: be-verb + past participle (simplified)
    be_verbs = r"(?:is|are|was|were|be|been|being|gets|got|gotten)"
    passive_pattern = rf"\b{be_verbs}\s+(?:\w+ly\s+)?(\w+(?:ed|en|ized|ised|ated|ted|sed))\b"
    sents = _sentences(text)
    passive_sents = []
    for s in sents:
        if re.search(passive_pattern, s, re.IGNORECASE):
            passive_sents.append(s)

    return {
        "total_sentences": len(sents),
        "passive_sentences": len(passive_sents),
        "passive_pct": round(100 * len(passive_sents) / max(len(sents), 1), 1),
        "target_range": "15-25% for academic IS papers",
        "examples": passive_sents[:5],  # Show first 5
    }


def _extract_sections(raw_text: str) -> dict[str, str]:
    """Split paper.md into named sections."""
    sections = {}
    current = "Front Matter"
    buf = []
    for line in raw_text.split("\n"):
        m = re.match(r"^(#{1,3})\s+(.+)", line)
        if m:
            if buf:
                sections[current] = "\n".join(buf)
            current = m.group(2).strip()
            buf = []
        else:
            buf.append(line)
    if buf:
        sections[current] = "\n".join(buf)
    return sections


# ── LLM prompts ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """\
You are an expert academic writing reviewer for top-tier Information Systems
conferences (AMCIS, ICIS, ECIS). You have deep expertise in IS research methodology
and academic English. Your job is to provide specific, actionable feedback that
will improve the paper's clarity, precision, and persuasiveness.
"""

REVIEW_PROMPT = """\
Review the following academic paper section for writing quality. Focus on:

1. CLARITY: Are arguments easy to follow? Any ambiguous sentences?
2. PRECISION: Are claims appropriately hedged? Any overclaiming?
3. FLOW: Does the argument build logically? Any abrupt transitions?
4. CONCISENESS: Any redundant phrases, wordy constructions, or filler?
5. ACADEMIC TONE: Is the register appropriate for AMCIS?
6. SPECIFIC EDITS: Provide 3-5 concrete sentence-level improvements.

SECTION: "{section_name}"

TEXT:
{section_text}

READABILITY STATS FOR THIS SECTION:
{readability_stats}

Return JSON:
{{
  "section": "{section_name}",
  "overall_grade": "A|B|C|D|F",
  "clarity_score": 1-10,
  "precision_score": 1-10,
  "flow_score": 1-10,
  "conciseness_score": 1-10,
  "tone_score": 1-10,
  "strengths": ["list of 2-3 specific strengths"],
  "issues": [
    {{
      "type": "clarity|precision|flow|conciseness|tone",
      "severity": "critical|major|minor",
      "location": "Quote the problematic phrase or sentence",
      "suggestion": "Concrete rewrite or fix"
    }}
  ],
  "rewrite_suggestions": [
    {{
      "original": "exact sentence from the text",
      "improved": "your improved version",
      "rationale": "Why this is better"
    }}
  ]
}}
"""

OVERALL_PROMPT = """\
You have reviewed all sections of an AMCIS 2026 paper individually. Now provide
an overall assessment.

SECTION GRADES:
{section_grades}

READABILITY METRICS:
{readability_summary}

PASSIVE VOICE ANALYSIS:
{passive_summary}

Return JSON:
{{
  "overall_grade": "A|B|C|D|F",
  "publishability": "ready|minor_revisions|major_revisions|not_ready",
  "top_3_strengths": ["list"],
  "top_3_weaknesses": ["list"],
  "priority_fixes": [
    {{
      "priority": 1,
      "description": "What to fix",
      "section": "Which section",
      "impact": "Why this matters for acceptance"
    }}
  ],
  "amcis_fit_assessment": "How well does the writing match AMCIS expectations?"
}}
"""


def run(paper_path: str = None):
    """Execute Step 6: Writing quality audit of paper.md."""
    print("=" * 70)
    print("STEP 6 AGENT — Writing Quality & Readability Audit")
    print("=" * 70)

    paper_path = paper_path or PAPER_PATH
    if not os.path.exists(paper_path):
        print(f"  ERROR: Paper not found at {paper_path}")
        return None

    # ── Load and parse paper ─────────────────────────────────────────────────
    with open(paper_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    print(f"  Loaded paper: {len(raw_text):,} chars")

    plain_text = _strip_markdown(raw_text)
    sections = _extract_sections(raw_text)
    print(f"  Found {len(sections)} sections")

    # ── Phase 1: Readability metrics ─────────────────────────────────────────
    print("\n  Phase 1: Computing readability metrics...")
    readability = _compute_readability(plain_text)
    print(f"    Flesch Reading Ease: {readability.get('flesch_reading_ease', 'N/A')}")
    print(f"    Flesch-Kincaid Grade: {readability.get('flesch_kincaid_grade', 'N/A')}")
    print(f"    Gunning Fog: {readability.get('gunning_fog_index', 'N/A')}")
    print(f"    Total words: {readability.get('total_words', 'N/A')}")

    # ── Phase 2: Passive voice detection ─────────────────────────────────────
    print("\n  Phase 2: Passive voice analysis...")
    passive = _detect_passive_voice(plain_text)
    print(f"    Passive voice: {passive['passive_pct']}% ({passive['passive_sentences']}/{passive['total_sentences']} sentences)")

    # ── Phase 3: Section-by-section LLM review ──────────────────────────────
    print("\n  Phase 3: Section-by-section LLM review...")
    # Review major sections (skip short/front-matter)
    review_sections = {k: v for k, v in sections.items()
                       if len(v) > 200 and k not in ("Front Matter", "References")}

    section_reviews = []
    for name, text in review_sections.items():
        if name.startswith(":::"):
            continue
        print(f"    Reviewing: {name}...")
        # Compute per-section readability
        sec_plain = _strip_markdown(text)
        sec_read = _compute_readability(sec_plain)

        # Truncate very long sections for the prompt
        prompt_text = text[:12_000] if len(text) > 12_000 else text

        review = chat_json(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": REVIEW_PROMPT.format(
                    section_name=name,
                    section_text=prompt_text,
                    readability_stats=json.dumps(sec_read, indent=2),
                )},
            ],
            model=config.SYNTHESIS_MODEL,
            max_tokens=config.MAX_OUTPUT_TOKENS,
        )
        section_reviews.append(review)

    # ── Phase 4: Overall assessment ──────────────────────────────────────────
    print("\n  Phase 4: Overall assessment...")
    section_grades = "\n".join(
        f"  {r.get('section', '?')}: {r.get('overall_grade', '?')} "
        f"(clarity={r.get('clarity_score', '?')}, precision={r.get('precision_score', '?')}, "
        f"flow={r.get('flow_score', '?')}, conciseness={r.get('conciseness_score', '?')}, "
        f"tone={r.get('tone_score', '?')})"
        for r in section_reviews
    )

    overall = chat_json(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": OVERALL_PROMPT.format(
                section_grades=section_grades,
                readability_summary=json.dumps(readability, indent=2),
                passive_summary=json.dumps(passive, indent=2),
            )},
        ],
        model=config.SYNTHESIS_MODEL,
        max_tokens=config.MAX_OUTPUT_TOKENS,
    )

    # ── Assemble output ──────────────────────────────────────────────────────
    result = {
        "paper_file": paper_path,
        "readability": readability,
        "passive_voice": passive,
        "section_reviews": section_reviews,
        "overall_assessment": overall,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n  Output saved: {OUTPUT_PATH}")
    print(f"  Overall grade: {overall.get('overall_grade', '?')}")
    print(f"  Publishability: {overall.get('publishability', '?')}")

    return result
