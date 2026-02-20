"""
Step 2 Agent — Crosswalk Synthesis with Source Citations

Reads governance/regulatory sources and architecture/integration sources,
then generates the crosswalk matrix with evidence trails:
  governance requirement → architecture control → evidence passage → competency statement.
"""

import csv, json, os
from . import config
from .literature_loader import load_sources, prepare_source_context
from .llm import chat_json

SYSTEM_PROMPT = """\
You are a rigorous IS research analyst performing a structured crosswalk \
analysis for an AMCIS 2026 paper. You map governance requirements from \
normative frameworks (NIST AI RMF, EU AI Act, OWASP) to architecture controls \
from practitioner guidance (agentic AI patterns, GenAIOps, enterprise architecture).

Critical rules:
1. Every mapping must cite a specific passage from the provided sources.
2. If no source evidence supports a mapping, do NOT create it.
3. Competency statements must be natural academic prose, not templates.
4. Classify each competency into "Trust Readiness" or "Integration Readiness" \
   based on whether the primary capability demand is governance/policy (Trust) \
   or architecture/engineering (Integration).
"""

# ── Governance requirements from normative sources ───────────────────────────
# These are the same 42 requirements from the original Step 2 but we'll enrich
# the mappings with LLM-extracted evidence.

GOVERNANCE_REQUIREMENTS = [
    {"id":"NIST-GV-1","source":"NIST AI RMF 1.0","function":"GOVERN","requirement":"Policies, processes, procedures and practices for mapping, measuring, and managing AI risks are in place, transparent, and implemented effectively."},
    {"id":"NIST-GV-2","source":"NIST AI RMF 1.0","function":"GOVERN","requirement":"Accountability structures empower appropriate teams and individuals for AI risk management."},
    {"id":"NIST-GV-3","source":"NIST AI RMF 1.0","function":"GOVERN","requirement":"Organizational culture considers and communicates AI risk."},
    {"id":"NIST-GV-4","source":"NIST AI RMF 1.0","function":"GOVERN","requirement":"Organizational teams are committed to a culture that considers AI risk."},
    {"id":"NIST-GV-5","source":"NIST AI RMF 1.0","function":"GOVERN","requirement":"Senior leadership and board members understand and contribute to AI risk management."},
    {"id":"NIST-GV-6","source":"NIST AI RMF 1.0","function":"GOVERN","requirement":"Policies address AI risks from third-party software, data, and supply chain."},
    {"id":"NIST-MP-1","source":"NIST AI RMF 1.0","function":"MAP","requirement":"Context established for AI system risks through understanding of intended purpose, impacts, and deployment context."},
    {"id":"NIST-MP-2","source":"NIST AI RMF 1.0","function":"MAP","requirement":"Scientific findings and organizational practices integrated to characterize AI risks."},
    {"id":"NIST-MP-3","source":"NIST AI RMF 1.0","function":"MAP","requirement":"AI risks and benefits mapped and prioritized by likelihood and magnitude of impact."},
    {"id":"NIST-MP-4","source":"NIST AI RMF 1.0","function":"MAP","requirement":"Risks and benefits understood by the organization and relevant AI actors."},
    {"id":"NIST-MP-5","source":"NIST AI RMF 1.0","function":"MAP","requirement":"Practices and personnel for supporting AI risk identification are in place."},
    {"id":"NIST-MS-1","source":"NIST AI RMF 1.0","function":"MEASURE","requirement":"AI risk measurement approaches are identified and applied."},
    {"id":"NIST-MS-2","source":"NIST AI RMF 1.0","function":"MEASURE","requirement":"AI system evaluated for trustworthy characteristics."},
    {"id":"NIST-MS-3","source":"NIST AI RMF 1.0","function":"MEASURE","requirement":"AI system performance or assurance criteria are measured."},
    {"id":"NIST-MS-4","source":"NIST AI RMF 1.0","function":"MEASURE","requirement":"Feedback about efficacy of measurement incorporated into organizational processes."},
    {"id":"NIST-MG-1","source":"NIST AI RMF 1.0","function":"MANAGE","requirement":"A plan for managing AI risks is developed, monitored, and in place."},
    {"id":"NIST-MG-2","source":"NIST AI RMF 1.0","function":"MANAGE","requirement":"Strategies to maximize AI benefits and minimize negative impacts are planned, implemented, and documented."},
    {"id":"NIST-MG-3","source":"NIST AI RMF 1.0","function":"MANAGE","requirement":"AI risks and benefits from third-party entities are managed."},
    {"id":"NIST-MG-4","source":"NIST AI RMF 1.0","function":"MANAGE","requirement":"Risk treatments including response, recovery, and communication plans are put in place."},
    {"id":"NIST-GEN-1","source":"NIST GenAI Profile","function":"GOVERN","requirement":"Policies address GenAI-specific risks: hallucination, data provenance, and synthetic content."},
    {"id":"NIST-GEN-2","source":"NIST GenAI Profile","function":"MAP","requirement":"Agentic AI risks including prompt injection, tool misuse, and autonomous action boundaries are identified."},
    {"id":"NIST-GEN-3","source":"NIST GenAI Profile","function":"MEASURE","requirement":"GenAI outputs evaluated for accuracy, bias, toxicity, and alignment with intended use."},
    {"id":"NIST-GEN-4","source":"NIST GenAI Profile","function":"MANAGE","requirement":"Human oversight mechanisms in place for high-stakes agentic decisions."},
    {"id":"EU-1","source":"EU AI Act (2024/1689)","function":"GOVERNANCE","requirement":"High-risk AI systems must implement a risk management system throughout the lifecycle (Art. 9)."},
    {"id":"EU-2","source":"EU AI Act (2024/1689)","function":"GOVERNANCE","requirement":"High-risk AI systems must use high-quality data with appropriate data governance (Art. 10)."},
    {"id":"EU-3","source":"EU AI Act (2024/1689)","function":"TRANSPARENCY","requirement":"High-risk AI systems must maintain technical documentation sufficient to assess compliance (Art. 11)."},
    {"id":"EU-4","source":"EU AI Act (2024/1689)","function":"TRANSPARENCY","requirement":"High-risk AI systems must enable logging of events throughout operation (Art. 12)."},
    {"id":"EU-5","source":"EU AI Act (2024/1689)","function":"TRANSPARENCY","requirement":"High-risk AI systems must be transparent and provide information to deployers (Art. 13)."},
    {"id":"EU-6","source":"EU AI Act (2024/1689)","function":"HUMAN OVERSIGHT","requirement":"High-risk AI systems must allow effective human oversight including ability to intervene and override (Art. 14)."},
    {"id":"EU-7","source":"EU AI Act (2024/1689)","function":"ACCURACY & ROBUSTNESS","requirement":"High-risk AI systems must achieve appropriate accuracy, robustness, and cybersecurity (Art. 15)."},
    {"id":"EU-8","source":"EU AI Act (2024/1689)","function":"GOVERNANCE","requirement":"GPAI model providers must maintain technical documentation and comply with copyright law (Art. 53)."},
    {"id":"EU-9","source":"EU AI Act (2024/1689)","function":"GOVERNANCE","requirement":"GPAI models with systemic risk must perform adversarial testing and incident reporting (Art. 55)."},
    {"id":"OWASP-1","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM01 Prompt Injection: Attackers manipulate LLMs via crafted inputs to cause unintended actions."},
    {"id":"OWASP-2","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM02 Sensitive Information Disclosure: LLMs may reveal confidential data in responses."},
    {"id":"OWASP-3","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM03 Supply Chain Vulnerabilities: LLM pipelines depend on third-party components with potential vulnerabilities."},
    {"id":"OWASP-4","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM04 Data and Model Poisoning: Training data or model weights manipulated to introduce vulnerabilities."},
    {"id":"OWASP-5","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM05 Improper Output Handling: Insufficient validation of LLM outputs before passing to downstream systems."},
    {"id":"OWASP-6","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM06 Excessive Agency: LLM agents granted excessive permissions or autonomy beyond what is needed."},
    {"id":"OWASP-7","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM07 System Prompt Leakage: System prompts containing sensitive instructions are exposed."},
    {"id":"OWASP-8","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM08 Vector and Embedding Weaknesses: Vulnerabilities in vector stores and embedding pipelines."},
    {"id":"OWASP-9","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM09 Misinformation: LLMs produce factually incorrect content presented as authoritative."},
    {"id":"OWASP-10","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM10 Unbounded Consumption: LLM applications vulnerable to resource exhaustion and denial-of-service."},
]

ARCH_CONTROLS = [
    "Single-Agent Orchestration Pattern",
    "Multi-Agent Orchestration Pattern",
    "Tool-Use Boundaries & Least-Privilege Access",
    "Human-in-the-Loop Approval Gates",
    "Nondeterminism Controls & Output Validation",
    "RAG Architecture & Data Grounding",
    "GenAIOps / MLOps Lifecycle Governance",
    "Evaluation & Monitoring Infrastructure",
    "Prompt Management & Secret Handling",
    "Scalable Modular Architecture (Archetypes)",
    "AI Risk Policy & Accountability Structures",
    "Threat Modeling & Red-Teaming",
    "Incident Response & Recovery Playbooks",
    "Audit Logging & Telemetry",
    "Regulatory Compliance Documentation",
    "Supply Chain & Vendor Risk Controls",
    "Data Governance & Access Controls",
    "Human Override & Control Mechanisms",
]

CROSSWALK_PROMPT = """\
You are performing a crosswalk analysis for an IS research paper.

Below are GOVERNANCE REQUIREMENTS from normative sources and a list of \
ARCHITECTURE CONTROLS from practitioner guidance. Also provided are the \
full texts of relevant literature sources.

For each governance requirement, determine:
1. Which architecture controls address it (select from the provided list ONLY)
2. Cite specific evidence from the literature sources supporting each mapping
3. Generate a natural-language competency statement (academic prose) that \
   describes the organizational capability needed to satisfy this requirement \
   through the identified controls
4. Classify as "Trust Readiness" or "Integration Readiness" based on whether \
   the PRIMARY capability demand is governance/policy (Trust) or \
   architecture/engineering (Integration)

Process requirements in this batch: {batch_ids}

ARCHITECTURE CONTROLS (select from these only):
{controls_list}

GOVERNANCE REQUIREMENTS:
{requirements_json}

LITERATURE SOURCES:
{source_text}

Return JSON:
{{
  "crosswalk": [
    {{
      "req_id": "...",
      "applicable_controls": ["control name", ...],
      "bundle": "Trust Readiness|Integration Readiness",
      "competency_statement": "Natural-language competency statement (1-2 sentences)...",
      "evidence": [
        {{
          "control": "control name",
          "source_id": "#XX",
          "passage": "Supporting passage (max 80 words)...",
          "reasoning": "Why this control addresses the requirement (1 sentence)"
        }}
      ]
    }}
  ]
}}
"""


def run(step1_results: list = None):
    """Execute Step 2 agent: generate crosswalk with evidence citations."""
    print("=" * 70)
    print("STEP 2 AGENT — Crosswalk Synthesis with Evidence")
    print("=" * 70)

    # Load governance + architecture literature sources
    all_source_ids = list(set(
        config.TRUST_SOURCES + config.INTEGRATION_SOURCES +
        config.REGULATORY_SOURCES + ["#29", "#20", "#11"]
    ))
    sources = load_sources(all_source_ids)
    print(f"Loaded {len(sources)} readable literature sources")

    source_context = prepare_source_context(sources, max_total_chars=400_000)
    controls_str = "\n".join(f"  - {c}" for c in ARCH_CONTROLS)

    # Process in batches to stay within token limits
    batch_size = 10
    all_crosswalk = []

    for i in range(0, len(GOVERNANCE_REQUIREMENTS), batch_size):
        batch = GOVERNANCE_REQUIREMENTS[i:i+batch_size]
        batch_ids = [r["id"] for r in batch]
        print(f"\n  Processing batch: {batch_ids[0]}..{batch_ids[-1]} ({len(batch)} requirements)")

        prompt = CROSSWALK_PROMPT.format(
            batch_ids=", ".join(batch_ids),
            controls_list=controls_str,
            requirements_json=json.dumps(batch, indent=2),
            source_text=source_context,
        )

        result = chat_json(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            model=config.SYNTHESIS_MODEL,
            max_tokens=config.MAX_OUTPUT_TOKENS,
        )

        batch_crosswalk = result.get("crosswalk", [])
        all_crosswalk.extend(batch_crosswalk)
        print(f"    Generated {len(batch_crosswalk)} crosswalk entries")

    # ── Write outputs ────────────────────────────────────────────────────────
    _write_crosswalk_matrix(all_crosswalk)
    _write_competency_statements(all_crosswalk)
    _write_evidence_json(all_crosswalk)

    print(f"\n{'='*70}")
    print(f"STEP 2 AGENT COMPLETE — {len(all_crosswalk)} requirements mapped")
    print(f"{'='*70}")

    return all_crosswalk


def _write_crosswalk_matrix(crosswalk: list):
    """Write the crosswalk matrix CSV (requirements × controls)."""
    # Build a lookup from req_id to original requirement
    req_lookup = {r["id"]: r for r in GOVERNANCE_REQUIREMENTS}

    rows = []
    for entry in crosswalk:
        rid = entry.get("req_id", "")
        req = req_lookup.get(rid, {})
        applicable = set(entry.get("applicable_controls", []))
        row = {
            "req_id": rid,
            "source": req.get("source", ""),
            "function": req.get("function", ""),
            "requirement": req.get("requirement", ""),
            "bundle": entry.get("bundle", ""),
            "competency_statement": entry.get("competency_statement", ""),
        }
        for ctrl in ARCH_CONTROLS:
            row[ctrl] = "X" if ctrl in applicable else ""
        rows.append(row)

    fieldnames = ["req_id", "source", "function", "requirement", "bundle",
                  "competency_statement"] + ARCH_CONTROLS
    outpath = os.path.join(config.ENRICHED_DIR, "step2_crosswalk_matrix.csv")
    with open(outpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote: {outpath} ({len(rows)} rows × {len(ARCH_CONTROLS)} controls)")


def _write_competency_statements(crosswalk: list):
    """Write competency statements CSV with evidence."""
    rows = []
    for i, entry in enumerate(crosswalk, 1):
        evidence_summary = "; ".join(
            f"[{e.get('source_id','')}] {e.get('reasoning','')}"
            for e in entry.get("evidence", [])[:4]
        )
        rows.append({
            "competency_id": f"COMP-{i:02d}",
            "req_id": entry.get("req_id", ""),
            "bundle": entry.get("bundle", ""),
            "competency_statement": entry.get("competency_statement", ""),
            "applicable_controls": "; ".join(entry.get("applicable_controls", [])),
            "evidence_summary": evidence_summary,
        })

    if not rows:
        return

    outpath = os.path.join(config.ENRICHED_DIR, "step2_competency_statements.csv")
    with open(outpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote: {outpath} ({len(rows)} statements)")


def _write_evidence_json(crosswalk: list):
    """Write full crosswalk with evidence as JSON."""
    outpath = os.path.join(config.ENRICHED_DIR, "step2_crosswalk_evidence.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(crosswalk, f, indent=2, ensure_ascii=False)
    print(f"  Wrote: {outpath}")


if __name__ == "__main__":
    run()
