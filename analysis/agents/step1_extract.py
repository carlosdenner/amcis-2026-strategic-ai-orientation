"""
Step 1 Agent — Evidence Extraction & Construct Definition Enrichment

Reads each relevant literature source and extracts passages that ground
the three core constructs (AI Orientation, Trust Readiness, Integration Readiness).
Produces enriched construct definitions with page/section-level citations.
"""

import csv, json, os
from . import config
from .literature_loader import load_sources, prepare_source_context
from .llm import chat_json, chat

SYSTEM_PROMPT = """\
You are a rigorous IS (Information Systems) research assistant helping build \
construct definitions for an AMCIS 2026 paper titled "Strategic AI Orientation \
Enabled by Trust & Integration Readiness."

THEORETICAL SPINE (apply consistently across all constructs):
- Dynamic Managerial Capabilities (DMC): CIO competencies are micro-foundations \
  enabling organisational AI capabilities.
- Role Theory: The CIO role is expanding and becoming multi-dimensional in \
  digital/AI transformation contexts.
- Governance-as-Capability: Responsible AI governance is a structured set of \
  practices (structural, relational, procedural) with antecedents and effects.
Use this tri-theory frame when evaluating evidence and defining sub-dimensions.

MCKINSEY SCALING CONSTRAINTS (anchor for practical relevance):
These are the top barriers to scaling agentic AI (McKinsey 2026, Exhibit 5):
  1. Talent/capability gaps (31%)
  2. Integration complexity with existing systems/tools (29%)
  3. Security/reliability/hallucinations (26%)
  4. Regulatory/privacy/compliance (24%)
  5. Lack of modern data foundations (21%)
  6. Lack of clear business use cases (18%)
  7. Difficulty measuring ROI/value (17%)
  8. Internal resistance/change management (16%)
For each sub-dimension you define, note which constraint(s) it addresses.

ROLE: You are a critical evidence analyst, NOT a cheerful summariser. Your job \
is to find, weigh, and sometimes REJECT evidence. A passage that merely mentions \
a keyword is NOT evidence for a construct.

RULES:
1. Only cite passages that ACTUALLY APPEAR in the provided sources.
2. Do NOT fabricate, paraphrase beyond the source, or hallucinate quotes.
3. If a source has NO relevant content for a construct, say so explicitly \
   in your negative_evidence list -- silence is not acceptable.
4. Apply the EVIDENCE STRENGTH RUBRIC below consistently.
5. Think step-by-step: first identify candidate passages, then evaluate each \
   against the rubric, then classify.

EVIDENCE STRENGTH RUBRIC:
- "strong": Source explicitly defines, operationalises, or empirically tests \
  the concept. The passage would alone justify including this dimension.
  Example: "AI governance maturity requires... [specific framework or definition]"
- "moderate": Source discusses the concept substantively but in an adjacent \
  context (e.g., discusses data governance but not specifically for AI systems).
  Example: A data governance article discussing principles applicable to AI.
- "weak": Source mentions the concept peripherally, or the relevance requires \
  interpretive inference. Include these BUT flag them clearly.
  Example: A single sentence mentioning "AI strategy" in passing.
- DISCARD: If the connection requires more than one logical leap, do NOT \
  include it. Better to have 3 strong extractions than 15 weak ones.
"""

EXTRACT_PROMPT_TEMPLATE = """\
TASK: Extract evidence for the construct "{construct_name}" from the sources below.

THINK STEP-BY-STEP:
1. Read each source and identify passages that relate to the construct.
2. For each candidate passage, ask: "Does this DIRECTLY discuss the concept, \
   or am I projecting relevance onto it?"
3. Apply the evidence strength rubric from your instructions.
4. For each source with NO relevant content, add it to the negative_evidence list.

CONSTRUCT DEFINITION (working):
{construct_def}

DIMENSIONS TO LOOK FOR (be selective -- not every source will address every dimension):
{dimensions}

DISCRIMINANT VALIDITY CHECK:
This construct must be DISTINCT from the other two constructs in the framework:
{discriminant_note}
If a passage seems relevant but actually belongs to another construct, note this \
in your thinking but EXCLUDE it from extractions.

For each relevant passage found, provide:
1. source_id -- the source identifier (e.g. "#01")
2. section -- the section or heading where the passage appears
3. quote -- the exact or close-paraphrase passage (max 150 words)
4. relevance -- which SPECIFIC dimension this supports (from the list above)
5. strength -- "strong", "moderate", or "weak" per the rubric
6. reasoning -- ONE sentence explaining WHY this is strong/moderate/weak evidence

Return JSON with this structure:
{{
  "construct": "{construct_name}",
  "chain_of_thought": "Walk through your reasoning: which sources looked promising, \
which turned out to be irrelevant, and why. 3-5 sentences.",
  "extractions": [
    {{
      "source_id": "#XX",
      "section": "...",
      "quote": "...",
      "relevance": "DIMENSION NAME from the list above",
      "strength": "strong|moderate|weak",
      "reasoning": "Why this evidence qualifies at this strength level"
    }}
  ],
  "negative_evidence": [
    {{
      "source_id": "#XX",
      "reason": "Why this source has no relevant content for this construct"
    }}
  ],
  "synthesis_notes": "Cross-source patterns: what converges, what gaps remain, \
what surprised you. 3-5 sentences."
}}

═══ LITERATURE SOURCES ═══
{source_text}
"""

DEFINITION_ENRICHMENT_PROMPT = """\
You are refining a construct definition for an AMCIS 2026 IS research paper.

Below are evidence extractions from {n_sources} literature sources for the \
construct "{construct_name}".

THINK STEP-BY-STEP:
1. Review the evidence extractions. Separate strong evidence from moderate/weak.
2. Identify recurring themes across MULTIPLE sources (triangulation).
3. Only propose sub-dimensions that have at least 2 supporting sources.
4. For each sub-dimension, articulate what makes it DISTINCT from the others.
5. For each sub-dimension, specify 1-3 OBSERVABLE PRACTICES -- concrete, \
   measurable organisational behaviours that indicate the sub-dimension is present. \
   These must be actionable and auditable (e.g., "Maintains a board-approved AI \
   risk appetite statement reviewed quarterly").
6. For each sub-dimension, propose 1-2 CANDIDATE METRICS or rough survey items \
   that could operationalise this sub-dimension in future empirical work \
   (e.g., "% of AI projects with a documented risk assessment at deployment gate").
7. Note which McKinsey scaling constraint(s) each sub-dimension primarily addresses.
8. Be honest about gaps: if a dimension has only weak evidence, say so.

IMPORTANT -- Source citation discipline:
- When you cite a source, use only the source IDs from the evidence extractions \
  (e.g., [#01], [#09]). These are the ONLY valid references.
- Do NOT invent academic references (e.g., "Smith et al., 2024") that are not \
  in the corpus. If you want to reference a theoretical lens, name the theory \
  but do NOT fabricate author/year citations.

Current working definition:
{current_def}

SOURCE TYPE CLASSIFICATION (for triangulation -- each sub-dimension should \
ideally be supported by at least 2 different source types):
{source_types}

Evidence extractions (with strength ratings):
{evidence_json}

Return JSON:
{{
  "construct": "{construct_name}",
  "enriched_definition": "... (3-5 sentences, with [#XX] citations only from evidence)",
  "theoretical_lens": "Name the theoretical lens without fabricating citations",
  "sub_dimensions": [
    {{
      "id": "XX-N",
      "name": "...",
      "definition": "1-2 sentence definition",
      "observable_practices": ["1-3 concrete, measurable practices that indicate this sub-dimension is present in an organisation"],
      "candidate_metrics": ["1-2 rough survey items or KPIs for future operationalisation"],
      "constraints_addressed": ["Which McKinsey scaling constraint(s) this sub-dimension helps remove"],
      "grounding_sources": ["#XX: specific finding or quote", ...],
      "source_types_represented": ["academic|standard|practitioner -- for triangulation check"],
      "evidence_strength": "strong|moderate|weak",
      "source_count": 0,
      "discriminant_note": "How this sub-dimension differs from adjacent sub-dimensions"
    }}
  ],
  "boundary_conditions": "Under what conditions does this construct NOT apply?",
  "gaps_identified": ["Specific gaps where evidence is thin or missing"],
  "confidence_assessment": "Overall confidence (high/medium/low) with justification"
}}
"""

# ── Construct metadata from original Step 1 ─────────────────────────────────

CONSTRUCTS = [
    {
        "name": "AI Orientation",
        "working_def": (
            "AI Orientation refers to a firm's strategic intent and directional commitment "
            "toward artificial intelligence as a source of competitive advantage and operational "
            "transformation. It encompasses the degree to which senior leadership -- particularly "
            "the CIO and board of directors -- actively shape, prioritize, and resource the "
            "organization's AI agenda."
        ),
        "dimensions": [
            "Strategic intent toward AI (proactive vs. reactive positioning)",
            "CIO centrality in AI agenda-setting",
            "Board-level AI risk and opportunity awareness",
            "Breadth of AI adoption scope (narrow automation vs. agentic transformation)",
            "Resource commitment depth (POC-stage vs. production-scale investment)",
        ],
        "discriminant_note": (
            "AI Orientation is about STRATEGIC INTENT and DIRECTION, not about HOW to "
            "implement safely (that is Trust Readiness) or HOW to build architecturally "
            "(that is Integration Readiness). A passage about 'CIO setting AI priorities' "
            "is AI Orientation; a passage about 'AI risk policy' is Trust Readiness."
        ),
        "relevant_sources": config.ORIENTATION_SOURCES + [
            "#14", "#18", "#03", "#07", "#17", "#31", "#32", "#34",
        ],
    },
    {
        "name": "Trust Readiness",
        "working_def": (
            "Trust Readiness refers to the organizational capability bundle that enables a firm "
            "to deploy and scale AI systems in a manner that is safe, accountable, auditable, and "
            "compliant with applicable governance standards and regulations."
        ),
        "dimensions": [
            "AI risk policy and accountability structures",
            "Agentic threat surface mapping (prompt injection, tool misuse, model poisoning)",
            "AI evaluation and monitoring governance",
            "Data governance and integrity assurance",
            "Regulatory compliance translation capability",
            "AI incident response and recovery",
            "Human override and control mechanisms",
            "Supply chain and third-party AI risk governance",
        ],
        "discriminant_note": (
            "Trust Readiness is about GOVERNANCE, POLICY, and RISK -- the organizational "
            "and regulatory controls. It is NOT about technical architecture choices (that "
            "is Integration Readiness) or strategic direction (that is AI Orientation). "
            "A passage about 'ISO 42001 risk assessment' is Trust Readiness; a passage "
            "about 'RAG pipeline design' is Integration Readiness."
        ),
        "relevant_sources": config.TRUST_SOURCES + [
            "#29", "#20", "#15", "#21", "#27", "#33",
        ],
    },
    {
        "name": "Integration Readiness",
        "working_def": (
            "Integration Readiness refers to the organizational capability bundle that enables "
            "a firm to architect, deploy, and operate agentic AI systems at enterprise scale."
        ),
        "dimensions": [
            "Orchestration pattern selection and design (single vs. multi-agent)",
            "Tool-use boundaries and least-privilege access",
            "Nondeterminism management and output validation",
            "RAG architecture and data grounding",
            "GenAIOps / MLOps lifecycle governance",
            "Scalable modular architecture (archetypes)",
            "Human-in-the-loop architecture patterns",
            "Evaluation and monitoring infrastructure",
        ],
        "discriminant_note": (
            "Integration Readiness is about TECHNICAL ARCHITECTURE and ENGINEERING -- how "
            "systems are designed, deployed, and operated. It is NOT about governance policy "
            "(that is Trust Readiness) or strategic vision (that is AI Orientation). "
            "A passage about 'multi-agent orchestration patterns' is Integration Readiness; "
            "a passage about 'AI ethics policy' is Trust Readiness."
        ),
        "relevant_sources": config.INTEGRATION_SOURCES + [
            "#11", "#08", "#15", "#16", "#17", "#19",
        ],
    },
]


def run():
    """Execute Step 1 agent: extract evidence and enrich construct definitions."""
    print("=" * 70)
    print("STEP 1 AGENT — Evidence Extraction & Construct Enrichment")
    print("=" * 70)

    all_results = []

    for construct in CONSTRUCTS:
        print(f"\n>>> Processing: {construct['name']}")

        # Load relevant sources
        sources = load_sources(construct["relevant_sources"])
        print(f"    Loaded {len(sources)} readable sources "
              f"(of {len(construct['relevant_sources'])} requested)")

        if not sources:
            print(f"    WARNING: No readable sources for {construct['name']}!")
            continue

        # Phase 1: Extract evidence from sources
        print(f"    Phase 1: Extracting evidence...")
        source_context = prepare_source_context(sources)
        dimensions_str = "\n".join(f"  - {d}" for d in construct["dimensions"])

        extract_prompt = EXTRACT_PROMPT_TEMPLATE.format(
            construct_name=construct["name"],
            construct_def=construct["working_def"],
            dimensions=dimensions_str,
            discriminant_note=construct.get("discriminant_note", "N/A"),
            source_text=source_context,
        )

        extractions = chat_json(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": extract_prompt},
            ],
            model=config.EXTRACTION_MODEL,
        )

        n_extractions = len(extractions.get("extractions", []))
        print(f"    Extracted {n_extractions} evidence passages")

        # Phase 2: Enrich construct definition using evidence
        print(f"    Phase 2: Enriching construct definition...")

        # Build source type map for triangulation
        source_type_info = "\n".join(
            f"  {sid}: {config.SOURCE_TYPES.get(sid, 'unknown')}"
            for sid in construct["relevant_sources"]
            if sid in config.SOURCE_TYPES
        )

        enrich_prompt = DEFINITION_ENRICHMENT_PROMPT.format(
            n_sources=len(sources),
            construct_name=construct["name"],
            current_def=construct["working_def"],
            source_types=source_type_info,
            evidence_json=json.dumps(extractions, indent=2),
        )

        enriched = chat_json(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": enrich_prompt},
            ],
            model=config.SYNTHESIS_MODEL,
        )

        enriched["_extractions"] = extractions
        all_results.append(enriched)

        n_subs = len(enriched.get("sub_dimensions", []))
        print(f"    Enriched definition: {n_subs} sub-dimensions identified")

    # ── Write outputs ────────────────────────────────────────────────────────
    _write_markdown(all_results)
    _write_csv(all_results)
    _write_evidence_json(all_results)

    print(f"\n{'='*70}")
    print(f"STEP 1 AGENT COMPLETE")
    print(f"{'='*70}")

    return all_results


def _write_markdown(results: list):
    """Write enriched construct definitions as a Markdown document."""
    lines = [
        "# Step 1 (Enriched) — Construct Definitions with Literature Evidence",
        "",
        "**Generated by**: Agentic evidence extraction pipeline",
        "**Paper**: Strategic AI Orientation Enabled by Trust & Integration Readiness",
        "**Venue**: AMCIS 2026",
        "",
        "---",
        "",
    ]

    for r in results:
        name = r.get("construct", "Unknown")
        lines += [
            f"## Construct: {name}",
            "",
            "### Enriched Definition",
            "",
            r.get("enriched_definition", "N/A"),
            "",
            f"**Theoretical Lens**: {r.get('theoretical_lens', 'N/A')}",
            "",
            f"**Boundary Conditions**: {r.get('boundary_conditions', 'N/A')}",
            "",
        ]

        # Sub-dimensions
        subs = r.get("sub_dimensions", [])
        if subs:
            lines += ["### Sub-Dimensions", ""]
            for s in subs:
                lines += [
                    f"**{s.get('id', '?')} — {s.get('name', '?')}** "
                    f"(evidence: {s.get('evidence_strength', '?')})",
                    "",
                    s.get("definition", ""),
                    "",
                    "Grounding sources:",
                    "",
                ]
                for gs in s.get("grounding_sources", []):
                    lines.append(f"- {gs}")
                lines.append("")

        # Gaps
        gaps = r.get("gaps_identified", [])
        if gaps:
            lines += ["### Identified Gaps", ""]
            for g in gaps:
                lines.append(f"- {g}")
            lines.append("")

        # Evidence extractions
        exts = r.get("_extractions", {}).get("extractions", [])
        if exts:
            lines += ["### Evidence Extraction Log", ""]
            lines.append("| Source | Section | Relevance | Strength | Quote (excerpt) |")
            lines.append("|--------|---------|-----------|----------|-----------------|")
            for e in exts:
                quote = e.get("quote", "")[:100].replace("|", "\\|").replace("\n", " ")
                lines.append(
                    f"| {e.get('source_id','')} | {e.get('section','')[:40]} | "
                    f"{e.get('relevance','')[:40]} | {e.get('strength','')} | "
                    f"{quote}... |"
                )
            lines.append("")

        synthesis = r.get("_extractions", {}).get("synthesis_notes", "")
        if synthesis:
            lines += ["### Cross-Source Synthesis", "", synthesis, ""]

        lines += ["---", ""]

    outpath = os.path.join(config.ENRICHED_DIR, "step1_construct_definitions.md")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Wrote: {outpath}")


def _write_csv(results: list):
    """Write sub-competencies CSV with evidence grounding."""
    rows = []
    for r in results:
        construct = r.get("construct", "")
        bundle = construct  # Will be "AI Orientation", "Trust Readiness", or "Integration Readiness"
        for s in r.get("sub_dimensions", []):
            rows.append({
                "id": s.get("id", ""),
                "bundle": bundle,
                "name": s.get("name", ""),
                "definition": s.get("definition", ""),
                "observable_practices": "; ".join(s.get("observable_practices", [])),
                "candidate_metrics": "; ".join(s.get("candidate_metrics", [])),
                "constraints_addressed": "; ".join(s.get("constraints_addressed", [])),
                "source_types": "; ".join(s.get("source_types_represented", [])),
                "evidence_strength": s.get("evidence_strength", ""),
                "grounding_sources": "; ".join(s.get("grounding_sources", [])),
            })

    if not rows:
        return

    outpath = os.path.join(config.ENRICHED_DIR, "step1_sub_competencies.csv")
    with open(outpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote: {outpath} ({len(rows)} sub-competencies)")


def _write_evidence_json(results: list):
    """Write full evidence extractions as JSON for downstream steps."""
    outpath = os.path.join(config.ENRICHED_DIR, "step1_evidence.json")
    # Strip the _extractions key for cleaner output
    output = []
    for r in results:
        entry = {k: v for k, v in r.items() if k != "_extractions"}
        entry["evidence_extractions"] = r.get("_extractions", {}).get("extractions", [])
        entry["synthesis_notes"] = r.get("_extractions", {}).get("synthesis_notes", "")
        output.append(entry)

    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"  Wrote: {outpath}")


if __name__ == "__main__":
    run()
