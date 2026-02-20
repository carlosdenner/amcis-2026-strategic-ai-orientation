"""
Step 4 Agent — Proposition Grounding & Synthesis

Reads outputs from Steps 1-3, computes actual statistics (not hardcoded),
and uses LLM to compose evidence paragraphs with real citations for each
of the 5 theoretical propositions.
"""

import csv, json, os
from collections import Counter
from . import config
from .llm import chat_json

SYSTEM_PROMPT = """\
You are an IS theory scholar composing grounded propositions for an AMCIS 2026 \
paper. Each proposition must be supported by computed evidence from the \
paper's own analysis (crosswalk statistics, incident coding frequencies) \
AND literature citations. Write in rigorous academic IS prose.
"""

PROPOSITION_SHELLS = [
    {
        "id": "P1",
        "label": "CIO Centrality → AI Orientation",
        "statement": (
            "The greater the CIO's centrality in the firm's strategic decision-making "
            "(as reflected in reporting structure, board access, and AI agenda ownership), "
            "the stronger the firm's AI orientation."
        ),
        "theoretical_lens": "Upper Echelons Theory (Hambrick & Mason, 1984); Strategic Choice Theory",
        "role_in_model": "Antecedent (independent variable)",
        "mechanism": "CIO attention allocation and strategic agenda-setting",
    },
    {
        "id": "P2",
        "label": "Trust Readiness mediates/moderates AI Orientation → Realized Value",
        "statement": (
            "Higher trust readiness (governance capability bundle) strengthens the conversion "
            "of AI orientation into production-scale AI value by reducing incident risk, "
            "enabling auditability, and satisfying regulatory license-to-operate requirements."
        ),
        "theoretical_lens": "Dynamic Capabilities (Teece et al., 1997); Responsible AI Governance",
        "role_in_model": "Mediator/Moderator (enabler of orientation → value conversion)",
        "mechanism": (
            "Trust readiness reduces the probability and severity of AI incidents, "
            "satisfies regulatory license-to-operate requirements, and builds stakeholder "
            "confidence enabling broader deployment authorization."
        ),
    },
    {
        "id": "P3",
        "label": "Integration Readiness mediates/moderates AI Orientation → Realized Value",
        "statement": (
            "Higher integration readiness (architecture capability bundle) strengthens the "
            "conversion of AI orientation into production-scale AI value by enabling reusable "
            "agentic architectures, operational AI lifecycle management, and scalable "
            "deployment without accumulating prohibitive technical debt."
        ),
        "theoretical_lens": "Dynamic Capabilities; Enterprise Architecture; IT Infrastructure Flexibility",
        "role_in_model": "Mediator/Moderator (enabler of orientation → value conversion)",
        "mechanism": (
            "Integration readiness reduces time-to-production for AI use cases, enables "
            "reuse via archetypes, prevents shadow IT via governed architecture, and ensures "
            "operational sustainability via GenAIOps practices."
        ),
    },
    {
        "id": "P4",
        "label": "Trust × Integration Readiness Complementarity",
        "statement": (
            "Trust readiness and integration readiness are strategic complements: the marginal "
            "value of each capability bundle is higher when the other bundle is also present, "
            "such that weak architecture undermines governance effectiveness and weak governance "
            "constrains safe architecture deployment."
        ),
        "theoretical_lens": "Complementarity Theory (Milgrom & Roberts, 1990); NIST interdependence",
        "role_in_model": "Interaction effect (joint moderator of orientation → value)",
        "mechanism": (
            "Architectural controls provide the technical substrate that makes governance "
            "policies enforceable and measurable. Governance policies provide the "
            "authorization and boundary conditions for safe architecture deployment."
        ),
    },
    {
        "id": "P5",
        "label": "Regulatory Pressure → Trust Readiness Salience → AI Orientation Agenda",
        "statement": (
            "External regulatory pressure (EU AI Act or equivalent) increases the strategic "
            "salience of trust readiness, elevating governance capability-building onto the "
            "CIO and board AI orientation agenda as a license-to-operate condition."
        ),
        "theoretical_lens": "Institutional Theory (DiMaggio & Powell, 1983); Coercive Isomorphism",
        "role_in_model": "Boundary condition / contextual moderator",
        "mechanism": (
            "Regulatory mandates create coercive isomorphic pressure that elevates trust "
            "readiness from operational compliance to strategic priority."
        ),
    },
]

PROPOSITION_GROUNDING_PROMPT = """\
You are grounding proposition {prop_id} ("{prop_label}") for an AMCIS 2026 paper.

Proposition statement: {prop_statement}
Theoretical lens: {theoretical_lens}
Mechanism: {mechanism}
Role in model: {role_in_model}

Below are COMPUTED STATISTICS from the paper's own analysis pipeline. Use these \
exact numbers (do not invent different ones) to compose evidence paragraphs.

STEP 2 STATISTICS (Crosswalk Analysis):
{step2_stats}

STEP 3 STATISTICS (ATLAS Incident Validation):
{step3_stats}

STEP 1 EVIDENCE (Construct Extraction Summary):
{step1_summary}

Compose:
1. An evidence-grounded RATIONALE paragraph (3-5 sentences) integrating both \
   literature citations and computed statistics from Steps 2-3.
2. A CROSSWALK EVIDENCE paragraph citing specific Step 2 statistics.
3. An ATLAS EVIDENCE paragraph citing specific Step 3 incident statistics.
4. A FALSIFIABILITY note (2-3 sentences) explaining how this proposition could \
   be tested or falsified.
5. A list of GROUNDING SOURCES (literature references supporting this proposition).

Return JSON:
{{
  "proposition_id": "{prop_id}",
  "rationale": "...",
  "crosswalk_evidence": "...",
  "atlas_evidence": "...",
  "falsifiability_note": "...",
  "grounding_sources": ["source 1", "source 2", ...]
}}
"""


def run(step1_results=None, step2_results=None, step3_results=None):
    """Execute Step 4 agent: ground propositions with computed evidence."""
    print("=" * 70)
    print("STEP 4 AGENT — Proposition Grounding & Synthesis")
    print("=" * 70)

    # ── Compute statistics from Steps 2 & 3 outputs ─────────────────────────
    step2_stats = _compute_step2_stats(step2_results)
    step3_stats = _compute_step3_stats(step3_results)
    step1_summary = _summarize_step1(step1_results)

    print(f"  Computed Step 2 stats: {len(step2_stats)} lines")
    print(f"  Computed Step 3 stats: {len(step3_stats)} lines")

    # ── Generate grounded propositions ───────────────────────────────────────
    all_propositions = []

    for prop in PROPOSITION_SHELLS:
        print(f"\n  Grounding {prop['id']}: {prop['label']}...")

        prompt = PROPOSITION_GROUNDING_PROMPT.format(
            prop_id=prop["id"],
            prop_label=prop["label"],
            prop_statement=prop["statement"],
            theoretical_lens=prop["theoretical_lens"],
            mechanism=prop["mechanism"],
            role_in_model=prop["role_in_model"],
            step2_stats=step2_stats,
            step3_stats=step3_stats,
            step1_summary=step1_summary,
        )

        result = chat_json(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            model=config.SYNTHESIS_MODEL,
        )

        # Merge shell + grounded evidence
        full_prop = {**prop, **result}
        all_propositions.append(full_prop)
        print(f"    Sources: {len(result.get('grounding_sources', []))}")

    # ── Write outputs ────────────────────────────────────────────────────────
    _write_markdown(all_propositions)
    _write_csv(all_propositions)
    _write_json(all_propositions)

    print(f"\n{'='*70}")
    print(f"STEP 4 AGENT COMPLETE — {len(all_propositions)} propositions grounded")
    print(f"{'='*70}")

    return all_propositions


def _compute_step2_stats(step2_results: list = None) -> str:
    """Compute statistics from Step 2 crosswalk results."""
    # Try to load from enriched output if not passed
    if not step2_results:
        path = os.path.join(config.ENRICHED_DIR, "step2_crosswalk_evidence.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                step2_results = json.load(f)

    if not step2_results:
        # Fallback: load from original CSV
        path = os.path.join(config.OUT_DIR, "step2_crosswalk_matrix.csv")
        if os.path.exists(path):
            return _compute_step2_stats_from_csv(path)
        return "Step 2 data not available."

    total_reqs = len(step2_results)
    bundle_counts = Counter(r.get("bundle", "") for r in step2_results)

    # Control frequency
    ctrl_freq = Counter()
    for r in step2_results:
        for c in r.get("applicable_controls", []):
            ctrl_freq[c] += 1

    # Count by source
    source_counts = Counter()
    # Try to identify source from req_id prefix
    for r in step2_results:
        rid = r.get("req_id", "")
        if rid.startswith("NIST-GEN"):
            source_counts["NIST GenAI Profile"] += 1
        elif rid.startswith("NIST"):
            source_counts["NIST AI RMF 1.0"] += 1
        elif rid.startswith("EU"):
            source_counts["EU AI Act"] += 1
        elif rid.startswith("OWASP"):
            source_counts["OWASP Top 10 LLM"] += 1

    lines = [
        f"Total governance requirements mapped: {total_reqs}",
        f"Bundle distribution: {dict(bundle_counts)}",
        f"Source distribution: {dict(source_counts)}",
        f"Top 10 most-demanded architecture controls:",
    ]
    for ctrl, cnt in ctrl_freq.most_common(10):
        lines.append(f"  [{cnt} reqs] {ctrl}")

    # Cross-bundle controls (appear in both Trust and Integration requirements)
    trust_ctrls = set()
    integ_ctrls = set()
    for r in step2_results:
        bundle = r.get("bundle", "")
        for c in r.get("applicable_controls", []):
            if "Trust" in bundle:
                trust_ctrls.add(c)
            elif "Integration" in bundle:
                integ_ctrls.add(c)
    cross_bundle = trust_ctrls & integ_ctrls
    lines.append(f"Controls appearing in BOTH bundles: {len(cross_bundle)} of {len(ctrl_freq)}")
    for c in sorted(cross_bundle):
        lines.append(f"  - {c}")

    # EU AI Act specific stats
    eu_reqs = [r for r in step2_results if r.get("req_id", "").startswith("EU")]
    if eu_reqs:
        eu_ctrls = Counter()
        for r in eu_reqs:
            for c in r.get("applicable_controls", []):
                eu_ctrls[c] += 1
        lines.append(f"EU AI Act requirements: {len(eu_reqs)}, spanning {len(eu_ctrls)} distinct controls")

    return "\n".join(lines)


def _compute_step2_stats_from_csv(path: str) -> str:
    """Fallback: compute stats from original CSV."""
    from . import step2_crosswalk as s2
    controls = s2.ARCH_CONTROLS
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    ctrl_freq = Counter()
    for row in rows:
        for ctrl in controls:
            if row.get(ctrl) == "X":
                ctrl_freq[ctrl] += 1

    lines = [
        f"Total governance requirements: {len(rows)}",
        f"Architecture controls: {len(controls)}",
        f"Top controls by demand:",
    ]
    for ctrl, cnt in ctrl_freq.most_common(10):
        lines.append(f"  [{cnt} reqs] {ctrl}")
    return "\n".join(lines)


def _compute_step3_stats(step3_results: list = None) -> str:
    """Compute statistics from Step 3 incident results."""
    # Try to load from enriched output
    if not step3_results:
        path = os.path.join(config.ENRICHED_DIR, "step3_enrichments.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                step3_results = json.load(f)

    if not step3_results:
        # Fallback: load from original CSVs
        return _compute_step3_stats_from_csv()

    total = len(step3_results)

    # Failure mode distribution
    fm_counts = Counter(r.get("failure_mode", "") for r in step3_results)

    # Trust vs Integration dominance
    split_counts = Counter(r.get("trust_integration_split", "") for r in step3_results)

    # Tactic frequency from rows
    tactic_freq = Counter()
    for r in step3_results:
        for t in r.get("tactics_used", "").split("; "):
            t = t.strip()
            if t:
                tactic_freq[t] += 1

    # Sub-competency frequency (from LLM enrichments)
    sc_freq = Counter()
    for r in step3_results:
        for sc in r.get("llm_sub_competencies", "").split("; "):
            sc = sc.strip()
            if sc:
                sc_freq[sc] += 1

    lines = [
        f"Total incidents coded: {total}",
        f"Failure mode distribution: {dict(fm_counts)}",
        f"Trust vs Integration dominance: {dict(split_counts)}",
        f"Top 10 tactics by frequency:",
    ]
    for tac, cnt in tactic_freq.most_common(10):
        info = PROPOSITION_SHELLS  # placeholder
        lines.append(f"  [{cnt}x] {tac}")

    if sc_freq:
        lines.append(f"Top 10 sub-competency gaps (LLM-identified):")
        for sc, cnt in sc_freq.most_common(10):
            lines.append(f"  [{cnt}x] {sc}")

    # Mitigation gap data
    mit_path = os.path.join(config.ENRICHED_DIR, "step3_mitigation_gaps.csv")
    if os.path.exists(mit_path):
        with open(mit_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            mit_rows = sorted(list(reader),
                             key=lambda x: -int(x.get("incident_count", 0)))
        lines.append(f"Top 10 missing mitigations (most-needed controls):")
        for m in mit_rows[:10]:
            lines.append(f"  [{m['incident_count']}x] {m['mitigation_id']} "
                         f"{m['mitigation_name']} ({m.get('category','')})")

    return "\n".join(lines)


def _compute_step3_stats_from_csv() -> str:
    """Fallback: compute stats from original CSVs."""
    lines = []
    for fname, label in [("step3_tactic_frequency.csv", "Tactic frequency"),
                          ("step3_mitigation_gaps.csv", "Mitigation gaps")]:
        path = os.path.join(config.OUT_DIR, fname)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            lines.append(f"\n{label} ({len(rows)} entries):")
            for r in rows[:10]:
                lines.append(f"  {r}")
    return "\n".join(lines) or "Step 3 data not available."


def _summarize_step1(step1_results: list = None) -> str:
    """Summarize Step 1 evidence for proposition grounding."""
    if not step1_results:
        path = os.path.join(config.ENRICHED_DIR, "step1_evidence.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                step1_results = json.load(f)

    if not step1_results:
        return "Step 1 evidence not available."

    lines = []
    for construct in step1_results:
        name = construct.get("construct", "")
        subs = construct.get("sub_dimensions", [])
        exts = construct.get("evidence_extractions", [])
        gaps = construct.get("gaps_identified", [])
        lines.append(f"\n{name}: {len(subs)} sub-dimensions, {len(exts)} evidence extractions")
        for s in subs[:4]:
            lines.append(f"  {s.get('id','')}: {s.get('name','')} "
                         f"[{s.get('evidence_strength','')}]")
        if gaps:
            lines.append(f"  Gaps: {'; '.join(gaps[:3])}")

    return "\n".join(lines)


def _write_markdown(propositions: list):
    """Write grounded propositions as Markdown."""
    lines = [
        "# Step 4 (Enriched) — Propositions with Computed Evidence",
        "",
        "**Generated by**: Agentic synthesis pipeline",
        "**Paper**: Strategic AI Orientation Enabled by Trust & Integration Readiness",
        "**Venue**: AMCIS 2026",
        "",
        "## Conceptual Model",
        "",
        "```",
        "Upper Echelons / Strategic Choice Layer",
        "  CIO Centrality + Board AI Awareness",
        "           |",
        "           v",
        "     AI ORIENTATION  <---- Regulatory Pressure (P5)",
        "           |",
        "    ______/ \\______",
        "   |                |",
        "   v                v",
        "TRUST           INTEGRATION",
        "READINESS       READINESS",
        "   |                |",
        "   |_____ x ________|   <-- Complementarity (P4)",
        "           |",
        "           v",
        "   REALIZED AI VALUE",
        "```",
        "",
        "---",
        "",
    ]

    for p in propositions:
        lines += [
            f"## {p['id']}: {p['label']}",
            "",
            f"**Proposition {p['id']}**: {p['statement']}",
            "",
            f"**Theoretical Lens**: {p.get('theoretical_lens', '')}",
            "",
            f"**Role in Model**: {p.get('role_in_model', '')}",
            "",
            f"**Mechanism**: {p.get('mechanism', '')}",
            "",
            "### Rationale (Evidence-Grounded)",
            "",
            p.get("rationale", "N/A"),
            "",
            "### Crosswalk Evidence (Step 2)",
            "",
            p.get("crosswalk_evidence", "N/A"),
            "",
            "### ATLAS Evidence (Step 3)",
            "",
            p.get("atlas_evidence", "N/A"),
            "",
            "### Falsifiability",
            "",
            p.get("falsifiability_note", "N/A"),
            "",
            "### Grounding Sources",
            "",
        ]
        for s in p.get("grounding_sources", []):
            lines.append(f"- {s}")
        lines += ["", "---", ""]

    outpath = os.path.join(config.ENRICHED_DIR, "step4_propositions.md")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Wrote: {outpath}")


def _write_csv(propositions: list):
    """Write propositions as CSV evidence table."""
    rows = []
    for p in propositions:
        rows.append({
            "proposition_id": p["id"],
            "label": p["label"],
            "statement": p["statement"],
            "theoretical_lens": p.get("theoretical_lens", ""),
            "role_in_model": p.get("role_in_model", ""),
            "mechanism": p.get("mechanism", ""),
            "rationale": p.get("rationale", ""),
            "crosswalk_evidence": p.get("crosswalk_evidence", ""),
            "atlas_evidence": p.get("atlas_evidence", ""),
            "falsifiability": p.get("falsifiability_note", ""),
            "sources": "; ".join(p.get("grounding_sources", [])),
        })

    if not rows:
        return

    outpath = os.path.join(config.ENRICHED_DIR, "step4_propositions.csv")
    with open(outpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote: {outpath} ({len(rows)} propositions)")


def _write_json(propositions: list):
    """Write full propositions as JSON."""
    outpath = os.path.join(config.ENRICHED_DIR, "step4_propositions.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(propositions, f, indent=2, ensure_ascii=False)
    print(f"  Wrote: {outpath}")


if __name__ == "__main__":
    run()
