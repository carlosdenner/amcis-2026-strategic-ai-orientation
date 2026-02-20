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

Your task: extract evidence from provided literature sources to ground three \
constructs. For each source, identify specific passages (quote or close paraphrase) \
relevant to the construct, noting the source ID and section/heading where found.

Be precise: cite actual content from the sources. Do NOT fabricate quotes. \
If a source has no relevant content for a construct, say so explicitly.
"""

EXTRACT_PROMPT_TEMPLATE = """\
Below are the texts of several literature sources. For each source, extract \
passages relevant to the construct "{construct_name}".

Construct definition (working): {construct_def}

Key dimensions to look for:
{dimensions}

For each relevant passage found, provide:
1. source_id — the source identifier (e.g. "#01")
2. section — the section or heading where the passage appears
3. quote — the exact or close-paraphrase passage (max 150 words)
4. relevance — which dimension or aspect of the construct this supports
5. strength — "direct" (explicitly discusses this concept) or "indirect" (provides supporting context)

Return JSON with this structure:
{{
  "construct": "{construct_name}",
  "extractions": [
    {{
      "source_id": "#XX",
      "section": "...",
      "quote": "...",
      "relevance": "...",
      "strength": "direct|indirect"
    }}
  ],
  "synthesis_notes": "Brief note on cross-source patterns and gaps (2-3 sentences)"
}}

═══ LITERATURE SOURCES ═══
{source_text}
"""

DEFINITION_ENRICHMENT_PROMPT = """\
You are refining a construct definition for an AMCIS 2026 IS research paper.

Below are evidence extractions from {n_sources} literature sources for the \
construct "{construct_name}". Using this evidence, produce an enriched construct \
definition that:

1. Maintains theoretical rigor (upper echelons, dynamic capabilities, institutional theory as appropriate)
2. Integrates specific evidence from the sources (with source ID citations)
3. Identifies sub-dimensions grounded in the literature
4. Notes any gaps where additional sources would strengthen the definition
5. Is written in academic IS prose suitable for an AMCIS paper

Current working definition:
{current_def}

Evidence extractions:
{evidence_json}

Return JSON:
{{
  "construct": "{construct_name}",
  "enriched_definition": "... (3-5 sentences, with [#XX] citations)",
  "theoretical_lens": "...",
  "sub_dimensions": [
    {{
      "id": "XX-N",
      "name": "...",
      "definition": "...",
      "grounding_sources": ["#XX: quote or finding", ...],
      "evidence_strength": "strong|moderate|weak"
    }}
  ],
  "boundary_conditions": "...",
  "gaps_identified": ["..."]
}}
"""

# ── Construct metadata from original Step 1 ─────────────────────────────────

CONSTRUCTS = [
    {
        "name": "AI Orientation",
        "working_def": (
            "AI Orientation refers to a firm's strategic intent and directional commitment "
            "toward artificial intelligence as a source of competitive advantage and operational "
            "transformation. It encompasses the degree to which senior leadership — particularly "
            "the CIO and board of directors — actively shape, prioritize, and resource the "
            "organization's AI agenda."
        ),
        "dimensions": [
            "Strategic intent toward AI (proactive vs. reactive positioning)",
            "CIO centrality in AI agenda-setting",
            "Board-level AI risk and opportunity awareness",
            "Breadth of AI adoption scope (narrow automation vs. agentic transformation)",
            "Resource commitment depth (POC-stage vs. production-scale investment)",
        ],
        "relevant_sources": config.ORIENTATION_SOURCES + ["#14", "#18"],
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
        "relevant_sources": config.TRUST_SOURCES + ["#29", "#20"],
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
        "relevant_sources": config.INTEGRATION_SOURCES + ["#11", "#08"],
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
        enrich_prompt = DEFINITION_ENRICHMENT_PROMPT.format(
            n_sources=len(sources),
            construct_name=construct["name"],
            current_def=construct["working_def"],
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
