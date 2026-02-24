"""
Step 8 Agent -- Peer Review Simulator

Simulates structured reviews from 3 reviewer personas:
  - Reviewer 1: Methodologist (statistical rigor, research design, validity)
  - Reviewer 2: Domain Expert (IS theory, governance, AI management)
  - Reviewer 3: Skeptic (logical gaps, alternative explanations, overclaims)

Each reviewer produces an independent review, then a meta-review synthesizes.

Outputs: data/processed/enriched/step8_peer_review.json
"""

import json, os
from . import config
from .llm import chat_json

# ── Paths ────────────────────────────────────────────────────────────────────
PAPER_PATH = os.path.join(config.BASE_DIR, "paper", "paper.md")
OUTPUT_PATH = os.path.join(config.ENRICHED_DIR, "step8_peer_review.json")


# ── Reviewer personas ───────────────────────────────────────────────────────

REVIEWER_1_SYSTEM = """\
You are REVIEWER 1: a senior IS researcher specializing in QUANTITATIVE METHODS.
You have published extensively in MISQ, ISR, and JMIS. You sit on the AMCIS
program committee. You are rigorous but fair.

Your review priorities:
1. Research design validity (internal, external, construct, statistical conclusion)
2. Statistical methodology (appropriate tests, effect sizes, confidence intervals)
3. Data quality and representativeness
4. Replicability and transparency
5. Appropriate use of secondary data
6. Threats to validity and how they are addressed

You are NOT impressed by novel theory if the empirics are weak. You look for
whether the data actually supports the claims being made.
"""

REVIEWER_2_SYSTEM = """\
You are REVIEWER 2: a senior IS researcher specializing in AI GOVERNANCE,
DIGITAL TRANSFORMATION, and INSTITUTIONAL THEORY. You have published in
JAIS, EJIS, and Information & Management. You review for AMCIS and ICIS.

Your review priorities:
1. Theoretical contribution — does this advance IS theory meaningfully?
2. Construct definitions — are they clear, well-bounded, and operationalizable?
3. Literature positioning — is prior work fairly represented?
4. Theoretical mechanisms — are the causal arguments plausible?
5. Novelty — what is genuinely new here vs. what is already known?
6. Practical relevance — does this inform IS practice?

You value theoretical depth and conceptual precision. You push authors to
clarify exactly what their contribution is relative to existing knowledge.
"""

REVIEWER_3_SYSTEM = """\
You are REVIEWER 3: the SKEPTIC. You are a mid-career researcher known for
tough but constructive reviews. You look for what can go wrong.

Your review priorities:
1. Alternative explanations for every finding
2. Logical leaps and inferential gaps
3. Overclaiming relative to evidence strength
4. Survivorship bias, selection effects, confounding
5. Whether the "so what" is compelling
6. Whether limitations are genuinely addressed or just listed

You play devil's advocate. For every claim, you ask: "Could this be explained
by something simpler?" and "What evidence would change your mind?"
You are constructive — you want the paper to improve, not just to criticize.
"""

REVIEW_PROMPT = """\
Review the following paper submitted to AMCIS 2026. Provide a structured
review following the AMCIS review form format.

PAPER TEXT:
{paper_text}

Provide your review as JSON:
{{
  "overall_recommendation": "strong_accept|accept|minor_revision|major_revision|reject",
  "confidence": "high|medium|low",
  "overall_assessment": "3-5 sentence summary of the paper's contribution and quality",
  "strengths": [
    {{
      "point": "Specific strength",
      "elaboration": "Why this matters"
    }}
  ],
  "weaknesses": [
    {{
      "point": "Specific weakness",
      "severity": "critical|major|minor",
      "elaboration": "Why this is a problem",
      "suggestion": "How to address it"
    }}
  ],
  "questions_for_authors": [
    "Specific question that needs answering"
  ],
  "detailed_comments": [
    {{
      "section": "Which section",
      "comment": "Specific comment",
      "type": "substantive|editorial|clarification"
    }}
  ],
  "missing_references": [
    "Author (Year) — Why this should be cited"
  ],
  "score_breakdown": {{
    "novelty": 1-10,
    "rigor": 1-10,
    "significance": 1-10,
    "presentation": 1-10,
    "overall": 1-10
  }}
}}
"""

META_REVIEW_PROMPT = """\
You are the ASSOCIATE EDITOR for this AMCIS 2026 submission. You have received
three independent reviews. Synthesize them into a meta-review.

REVIEWER 1 (Methodologist):
Recommendation: {r1_rec}
Overall: {r1_overall}
Strengths: {r1_strengths}
Weaknesses: {r1_weaknesses}

REVIEWER 2 (Domain Expert):
Recommendation: {r2_rec}
Overall: {r2_overall}
Strengths: {r2_strengths}
Weaknesses: {r2_weaknesses}

REVIEWER 3 (Skeptic):
Recommendation: {r3_rec}
Overall: {r3_overall}
Strengths: {r3_strengths}
Weaknesses: {r3_weaknesses}

Provide your meta-review as JSON:
{{
  "editorial_recommendation": "accept|minor_revision|major_revision|reject",
  "consensus_strengths": ["Points all/most reviewers agree are strong"],
  "consensus_weaknesses": ["Points all/most reviewers flag as problematic"],
  "disagreements": ["Where reviewers disagree and your assessment"],
  "required_revisions": [
    {{
      "priority": 1,
      "requirement": "What must change",
      "rationale": "Why, referencing reviewer comments",
      "difficulty": "easy|moderate|hard"
    }}
  ],
  "optional_improvements": ["Nice-to-have changes"],
  "risks_if_not_addressed": "What happens if the required revisions are not made",
  "editorial_summary": "2-3 paragraph summary for the authors"
}}
"""


def run(paper_path: str = None):
    """Execute Step 8: Simulated peer review."""
    print("=" * 70)
    print("STEP 8 AGENT — Peer Review Simulator")
    print("=" * 70)

    paper_path = paper_path or PAPER_PATH
    if not os.path.exists(paper_path):
        print(f"  ERROR: Paper not found at {paper_path}")
        return None

    with open(paper_path, "r", encoding="utf-8") as f:
        paper_text = f.read()

    print(f"  Loaded paper: {len(paper_text):,} chars")

    # Trim if needed for context window (keep under ~80k chars ≈ 20k tokens)
    if len(paper_text) > 80_000:
        paper_text = paper_text[:80_000] + "\n\n[... truncated for review ...]"

    reviewers = [
        ("Reviewer 1 — Methodologist", REVIEWER_1_SYSTEM),
        ("Reviewer 2 — Domain Expert", REVIEWER_2_SYSTEM),
        ("Reviewer 3 — Skeptic", REVIEWER_3_SYSTEM),
    ]

    reviews = []
    for name, system_prompt in reviewers:
        print(f"\n  {name} is reviewing...")
        review = chat_json(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": REVIEW_PROMPT.format(paper_text=paper_text)},
            ],
            model=config.SYNTHESIS_MODEL,
            max_tokens=config.MAX_OUTPUT_TOKENS,
        )
        review["reviewer"] = name
        reviews.append(review)
        rec = review.get("overall_recommendation", "?")
        scores = review.get("score_breakdown", {})
        print(f"    Recommendation: {rec}")
        print(f"    Scores: novelty={scores.get('novelty','?')}, rigor={scores.get('rigor','?')}, "
              f"significance={scores.get('significance','?')}, presentation={scores.get('presentation','?')}")

    # ── Meta-review ──────────────────────────────────────────────────────────
    print(f"\n  Associate Editor synthesizing meta-review...")

    def _summarize_list(items, key="point"):
        if isinstance(items, list):
            return "; ".join(
                i.get(key, str(i)) if isinstance(i, dict) else str(i)
                for i in items[:5]
            )
        return str(items)

    meta_review = chat_json(
        messages=[
            {"role": "system", "content":
             "You are an experienced AMCIS Associate Editor. Be fair, constructive, and decisive."},
            {"role": "user", "content": META_REVIEW_PROMPT.format(
                r1_rec=reviews[0].get("overall_recommendation", "?"),
                r1_overall=reviews[0].get("overall_assessment", "?"),
                r1_strengths=_summarize_list(reviews[0].get("strengths", [])),
                r1_weaknesses=_summarize_list(reviews[0].get("weaknesses", [])),
                r2_rec=reviews[1].get("overall_recommendation", "?"),
                r2_overall=reviews[1].get("overall_assessment", "?"),
                r2_strengths=_summarize_list(reviews[1].get("strengths", [])),
                r2_weaknesses=_summarize_list(reviews[1].get("weaknesses", [])),
                r3_rec=reviews[2].get("overall_recommendation", "?"),
                r3_overall=reviews[2].get("overall_assessment", "?"),
                r3_strengths=_summarize_list(reviews[2].get("strengths", [])),
                r3_weaknesses=_summarize_list(reviews[2].get("weaknesses", [])),
            )},
        ],
        model=config.SYNTHESIS_MODEL,
        max_tokens=config.MAX_OUTPUT_TOKENS,
    )

    # ── Assemble output ──────────────────────────────────────────────────────
    result = {
        "paper_file": paper_path,
        "reviews": reviews,
        "meta_review": meta_review,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n  Output saved: {OUTPUT_PATH}")
    print(f"\n  ── SUMMARY ──")
    for r in reviews:
        print(f"    {r.get('reviewer', '?')}: {r.get('overall_recommendation', '?')}")
    print(f"    Meta-review: {meta_review.get('editorial_recommendation', '?')}")

    return result
