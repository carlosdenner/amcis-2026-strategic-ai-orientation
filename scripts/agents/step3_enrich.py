"""
Step 3 Agent -- Incident Validation & Coverage Mapping

Reads MITRE ATLAS case studies as an adversarial-incident corpus, codes each
incident by harm type, failure mode, and implied competency gap, then produces
a COVERAGE MAP showing which framework sub-competencies are validated by
real-world incidents. This is the "negative-case" validation layer that
strengthens the claim that the competency framework covers real failure modes.
"""

import csv, json, os, yaml
from collections import defaultdict, Counter
from . import config
from .llm import chat_json

# ── Correct mitigation category → competency mapping ────────────────────────
# The original pipeline used wrong category keys. The actual ATLAS categories
# are: "Technical - ML", "Technical - Cyber", "Policy"

MITIGATION_CATEGORY_TO_COMPETENCY = {
    "Technical - ML":    "Integration Readiness — ML Lifecycle & Model Controls",
    "Technical - Cyber": "Trust Readiness — Cybersecurity & Technical Controls",
    "Policy":            "Trust Readiness — AI Governance & Policy",
}

# Tactic → domain mapping (kept from original, it's correct)
TACTIC_TO_DOMAIN = {
    "AML.TA0000": ("Trust Readiness",       "TR-1", "Model Access Governance"),
    "AML.TA0001": ("Integration Readiness",  "IR-2", "AI Attack Staging Defense"),
    "AML.TA0002": ("Trust Readiness",        "TR-2", "Threat Intelligence & Reconnaissance Defense"),
    "AML.TA0003": ("Integration Readiness",  "IR-6", "Resource & Supply Chain Controls"),
    "AML.TA0004": ("Integration Readiness",  "IR-2", "Access Boundary & Initial Access Controls"),
    "AML.TA0005": ("Integration Readiness",  "IR-1", "Execution Controls & Sandboxing"),
    "AML.TA0006": ("Trust Readiness",        "TR-3", "Persistence Detection & Monitoring"),
    "AML.TA0007": ("Trust Readiness",        "TR-3", "Defense Evasion Detection"),
    "AML.TA0008": ("Trust Readiness",        "TR-2", "Discovery & Enumeration Controls"),
    "AML.TA0009": ("Trust Readiness",        "TR-4", "Data Collection & Exfiltration Prevention"),
    "AML.TA0010": ("Trust Readiness",        "TR-4", "Data Exfiltration Controls"),
    "AML.TA0011": ("Trust Readiness",        "TR-6", "Impact Containment & Recovery"),
    "AML.TA0012": ("Integration Readiness",  "IR-2", "Privilege & Identity Management"),
    "AML.TA0013": ("Trust Readiness",        "TR-4", "Credential & Secret Management"),
    "AML.TA0014": ("Integration Readiness",  "IR-8", "C2 Detection & Network Controls"),
    "AML.TA0015": ("Integration Readiness",  "IR-2", "Lateral Movement Prevention"),
}

INCIDENT_ENRICHMENT_PROMPT = """\
You are an IS researcher analyzing MITRE ATLAS AI security incidents for an \
AMCIS 2026 paper on CIO competencies for AI governance and integration.

THINK STEP-BY-STEP for each incident:
1. Read the incident summary and identify what WENT WRONG.
2. Classify the HARM TYPE -- what kind of damage occurred or could have occurred.
3. Determine whether the root cause was a MISSING CONTROL (prevention), \
   a MISSED DETECTION (detection), or an INADEQUATE RESPONSE (response).
4. Map to the MOST RELEVANT sub-competency ID(s) -- be selective, not everything is TR-1.
5. Determine whether the dominant capability gap is governance (Trust) or \
   architecture (Integration) by asking: would a POLICY change or an \
   ENGINEERING change have prevented this?

HARM TYPE CLASSIFICATION (select the PRIMARY harm):
- "security": Confidentiality, integrity, or availability of systems/data was compromised
- "privacy": Personal or sensitive data was exposed, leaked, or misused
- "reliability": System produced incorrect, unreliable, or degraded outputs
- "autonomy_misuse": AI system took autonomous actions beyond intended scope or authority
- "safety": Physical safety or wellbeing of people was threatened
- "bias_discrimination": Outputs exhibited unfair bias or discriminatory behaviour
- "intellectual_property": Training data, model weights, or proprietary knowledge was stolen
- "supply_chain": Third-party components or data sources introduced vulnerabilities

FAILURE MODE RUBRIC -- apply these definitions STRICTLY:

"prevention_failure": The attack succeeded because NO CONTROL existed to \
block it. The organisation lacked the policy, mechanism, or capability entirely.
  EXAMPLE: A model was poisoned during training because no data provenance \
  checks existed. (No control = prevention failure)
  EXAMPLE: Prompt injection altered agent behaviour because no input \
  validation layer was deployed. (No defense = prevention failure)

"detection_failure": Controls WERE in place, but the attack evaded them or \
operated below detection thresholds. The organisation had defenses but they \
were insufficient to NOTICE the attack.
  EXAMPLE: An adversary slowly exfiltrated training data over weeks without \
  triggering anomaly detection alerts. (Had monitoring, but missed it)
  EXAMPLE: Model degradation due to distribution drift went unnoticed until \
  downstream business metrics collapsed. (Had no model monitoring)

"response_failure": The attack WAS detected (or could have been), but the \
organisation's response was too slow, inadequate, or absent.
  EXAMPLE: Adversarial examples were detected in production but the team \
  lacked a playbook to quarantine and retrain. (Detected, no response plan)
  EXAMPLE: A data breach was identified within hours but disclosure to \
  regulators took 3 months. (Slow institutional response)

DECISION RULE: If unsure, ask: "Was there a control that COULD have caught this?"
- No control existed -> prevention_failure
- Control existed but failed/was evaded -> detection_failure
- Attack was detected but response failed -> response_failure

TRUST VS. INTEGRATION SPLIT:
- "trust-dominant": The root cause is a GOVERNANCE gap (missing policy, \
  accountability structure, risk process, regulatory compliance)
- "integration-dominant": The root cause is an ARCHITECTURE gap (missing \
  technical control, monitoring infrastructure, deployment safeguard)
- "both": ONLY use this when the incident genuinely involves equal failures \
  in both governance AND architecture. This should be rare (~20-30% of cases), \
  not the default.

Sub-competency framework:
Trust Readiness: TR-1 (Risk Policy), TR-2 (Threat Mapping), TR-3 (Monitoring), \
TR-4 (Data Governance), TR-5 (Regulatory Compliance), TR-6 (Incident Response), \
TR-7 (Human Override), TR-8 (Supply Chain Risk)
Integration Readiness: IR-1 (Orchestration), IR-2 (Tool-Use Boundaries), \
IR-3 (Nondeterminism), IR-4 (RAG Architecture), IR-5 (GenAIOps), \
IR-6 (Modular Architecture), IR-7 (HITL Architecture), IR-8 (Eval Infrastructure)

Incidents:
{incidents_json}

Return JSON:
{{
  "enrichments": [
    {{
      "case_study_id": "AML.CSXXXX",
      "chain_of_thought": "2-3 sentences: what happened, what was missing, why you classified it this way",
      "harm_type": "security|privacy|reliability|autonomy_misuse|safety|bias_discrimination|intellectual_property|supply_chain",
      "competency_gap_description": "1-2 sentence academic description of the missing capability",
      "primary_sub_competencies": ["TR-X or IR-Y -- pick 1-2 most relevant, not a long list"],
      "failure_mode": "prevention_failure|detection_failure|response_failure",
      "failure_mode_reasoning": "1 sentence explaining your failure mode classification",
      "trust_integration_split": "trust-dominant|integration-dominant|both",
      "split_reasoning": "1 sentence explaining your split classification"
    }}
  ]
}}
"""


def run(step1_results: list = None, step2_results: list = None):
    """Execute Step 3 agent: validate framework coverage via ATLAS incidents."""
    print("=" * 70)
    print("STEP 3 AGENT -- Incident Validation & Coverage Mapping")
    print("=" * 70)

    # ── Load ATLAS data ──────────────────────────────────────────────────────
    with open(config.ATLAS_DIST, encoding="utf-8") as f:
        atlas = yaml.safe_load(f)

    matrix       = atlas["matrices"][0]
    case_studies  = atlas["case-studies"]
    tactics_data  = {t["id"]: t for t in matrix["tactics"]}
    techniques    = {t["id"]: t for t in matrix["techniques"]}
    mitigations   = {m["id"]: m for m in matrix["mitigations"]}

    print(f"Loaded: {len(tactics_data)} tactics, {len(techniques)} techniques, "
          f"{len(mitigations)} mitigations, {len(case_studies)} case studies")

    # ── Build technique → mitigation mapping ─────────────────────────────────
    tech_to_mits = defaultdict(list)
    for mid, m in mitigations.items():
        cats = m.get("category", [])
        cat_str = cats[0] if isinstance(cats, list) and cats else str(cats)
        for tech_ref in m.get("techniques", []):
            tid = tech_ref if isinstance(tech_ref, str) else tech_ref.get("id", "")
            if tid:
                tech_to_mits[tid].append({"id": mid, "name": m["name"], "category": cat_str})

    # ── Code each case study ─────────────────────────────────────────────────
    rows = []
    tactic_freq = Counter()
    mitigation_gap_freq = Counter()
    domain_freq = Counter()

    for cs in case_studies:
        cs_id   = cs.get("id", "")
        cs_name = cs.get("name", "")
        cs_date = str(cs.get("incident-date", ""))
        cs_type = cs.get("case-study-type", "")
        summary = str(cs.get("summary", ""))[:400].replace("\n", " ")
        procedures = cs.get("procedure", []) or []
        target = cs.get("target", {}) or {}
        actor  = cs.get("actor", {}) or {}
        target_str = target.get("name","") if isinstance(target, dict) else str(target)
        actor_str  = actor.get("name","") if isinstance(actor, dict) else str(actor)

        used_techniques = set()
        used_tactics = set()
        for step in procedures:
            tac = step.get("tactic", "")
            tid = step.get("technique", "")
            if tac:
                used_tactics.add(tac)
                tactic_freq[tac] += 1
            if tid:
                used_techniques.add(tid)

        # Derive competency domains from tactics (improved mapping)
        domains = []
        sub_comp_ids = set()
        for t in used_tactics:
            info = TACTIC_TO_DOMAIN.get(t)
            if info:
                bundle, sc_id, label = info
                domains.append(f"{bundle} — {label}")
                sub_comp_ids.add(sc_id)
                domain_freq[f"{bundle} — {label}"] += 1

        # Find applicable mitigations (controls that would address used techniques)
        applicable_mits = {}
        for tid in used_techniques:
            for m in tech_to_mits.get(tid, []):
                applicable_mits[m["id"]] = m
        for m in applicable_mits.values():
            mitigation_gap_freq[m["id"]] += 1

        # Correct competency gap from mitigation categories
        comp_gaps = set()
        for m in applicable_mits.values():
            cat = m.get("category", "")
            gap = MITIGATION_CATEGORY_TO_COMPETENCY.get(cat, f"Uncategorized ({cat})")
            comp_gaps.add(gap)

        rows.append({
            "case_study_id": cs_id,
            "name": cs_name,
            "incident_date": cs_date,
            "type": cs_type,
            "actor": actor_str,
            "target": target_str,
            "summary": summary,
            "tactics_used": "; ".join(sorted(used_tactics)),
            "techniques_used": "; ".join(sorted(used_techniques)),
            "technique_count": len(used_techniques),
            "competency_domains": "; ".join(sorted(set(domains))),
            "sub_competency_ids": "; ".join(sorted(sub_comp_ids)),
            "missing_controls": "; ".join(f'{m["id"]}: {m["name"]}'
                                          for m in list(applicable_mits.values())[:6]),
            "competency_gaps": "; ".join(sorted(comp_gaps)),
        })

    # ── LLM enrichment: generate competency gap descriptions ────────────────
    print(f"\n  Enriching {len(rows)} incidents with LLM-generated gap descriptions...")

    # Send incidents in smaller batches for better LLM attention
    enrichments = {}
    batch_size = 5  # Smaller batches = better per-incident reasoning
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i+batch_size]
        batch_summaries = [
            {"case_study_id": r["case_study_id"], "name": r["name"],
             "summary": r["summary"][:300],
             "type": r.get("type", ""),
             "actor": r.get("actor", ""),
             "target": r.get("target", ""),
             "tactics_used": r["tactics_used"],
             "missing_controls": r["missing_controls"][:300],
             "competency_gaps": r["competency_gaps"]}
            for r in batch
        ]
        print(f"    Batch {i//batch_size+1}: {batch[0]['case_study_id']}..{batch[-1]['case_study_id']}")

        result = chat_json(
            messages=[
                {"role": "system", "content": "You are an IS researcher analyzing AI security incidents."},
                {"role": "user", "content": INCIDENT_ENRICHMENT_PROMPT.format(
                    incidents_json=json.dumps(batch_summaries, indent=2)
                )},
            ],
            model=config.EXTRACTION_MODEL,
        )

        for e in result.get("enrichments", []):
            enrichments[e["case_study_id"]] = e

    # Merge LLM enrichments into rows
    for row in rows:
        e = enrichments.get(row["case_study_id"], {})
        row["harm_type"] = e.get("harm_type", "")
        row["llm_gap_description"] = e.get("competency_gap_description", "")
        row["llm_sub_competencies"] = "; ".join(e.get("primary_sub_competencies", []))
        row["failure_mode"] = e.get("failure_mode", "")
        row["failure_mode_reasoning"] = e.get("failure_mode_reasoning", "")
        row["trust_integration_split"] = e.get("trust_integration_split", "")
        row["split_reasoning"] = e.get("split_reasoning", "")
        row["chain_of_thought"] = e.get("chain_of_thought", "")

    # ── Write outputs ────────────────────────────────────────────────────────
    _write_incident_coding(rows)
    _write_tactic_frequency(tactic_freq, tactics_data)
    _write_mitigation_gaps(mitigation_gap_freq, mitigations)
    _write_coverage_map(rows)
    _write_enrichment_json(rows)

    # ── Print summary ────────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("STEP 3 VALIDATION SUMMARY")
    print(f"{'='*70}")
    print(f"Case studies coded: {len(rows)}")
    print(f"Unique tactics: {len(tactic_freq)}")
    print(f"Unique mitigation gaps: {len(mitigation_gap_freq)}")

    # Harm type distribution
    harm_counts = Counter(r.get("harm_type", "") for r in rows)
    print(f"\nHarm type distribution:")
    for ht, cnt in harm_counts.most_common():
        print(f"  {ht or 'unclassified'}: {cnt}")

    # Failure mode distribution
    fm_counts = Counter(r.get("failure_mode","") for r in rows)
    print(f"\nFailure mode distribution:")
    for fm, cnt in fm_counts.most_common():
        print(f"  {fm or 'unclassified'}: {cnt}")

    # Trust vs Integration split
    split_counts = Counter(r.get("trust_integration_split","") for r in rows)
    print(f"\nTrust vs Integration dominance:")
    for s, cnt in split_counts.most_common():
        print(f"  {s or 'unclassified'}: {cnt}")

    # Coverage map summary
    sc_freq = Counter()
    for r in rows:
        for sc in r.get("llm_sub_competencies", "").split("; "):
            sc = sc.strip()
            if sc:
                sc_freq[sc] += 1
    all_scs = ["TR-1","TR-2","TR-3","TR-4","TR-5","TR-6","TR-7","TR-8",
               "IR-1","IR-2","IR-3","IR-4","IR-5","IR-6","IR-7","IR-8"]
    covered = [sc for sc in all_scs if sc_freq.get(sc, 0) > 0]
    uncovered = [sc for sc in all_scs if sc_freq.get(sc, 0) == 0]
    print(f"\nFramework coverage: {len(covered)}/{len(all_scs)} sub-competencies validated")
    if uncovered:
        print(f"  UNCOVERED: {', '.join(uncovered)}")

    return rows


def _write_incident_coding(rows):
    outpath = os.path.join(config.ENRICHED_DIR, "step3_incident_coding.csv")
    if not rows:
        return
    with open(outpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote: {outpath} ({len(rows)} rows)")


def _write_tactic_frequency(tactic_freq, tactics_data):
    tac_summary = sorted(
        [{"tactic_id": k,
          "tactic_name": tactics_data.get(k, {}).get("name", "?"),
          "incident_count": v,
          "bundle": TACTIC_TO_DOMAIN.get(k, ("?","?","?"))[0],
          "sub_competency_id": TACTIC_TO_DOMAIN.get(k, ("?","?","?"))[1],
          "competency_domain": TACTIC_TO_DOMAIN.get(k, ("?","?","?"))[2]}
         for k, v in tactic_freq.items()],
        key=lambda x: -x["incident_count"]
    )
    outpath = os.path.join(config.ENRICHED_DIR, "step3_tactic_frequency.csv")
    if tac_summary:
        with open(outpath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=tac_summary[0].keys())
            writer.writeheader()
            writer.writerows(tac_summary)
        print(f"  Wrote: {outpath}")


def _write_mitigation_gaps(mitigation_gap_freq, mitigations):
    def get_cat(m):
        cats = m.get("category", [])
        return cats[0] if isinstance(cats, list) and cats else str(cats)

    gaps = sorted(
        [{"mitigation_id": k,
          "mitigation_name": mitigations.get(k, {}).get("name", "?"),
          "category": get_cat(mitigations.get(k, {})),
          "incident_count": v,
          "competency_gap": MITIGATION_CATEGORY_TO_COMPETENCY.get(
              get_cat(mitigations.get(k, {})), "Uncategorized")}
         for k, v in mitigation_gap_freq.items()],
        key=lambda x: -x["incident_count"]
    )
    outpath = os.path.join(config.ENRICHED_DIR, "step3_mitigation_gaps.csv")
    if gaps:
        with open(outpath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=gaps[0].keys())
            writer.writeheader()
            writer.writerows(gaps)
        print(f"  Wrote: {outpath}")


def _write_enrichment_json(rows):
    outpath = os.path.join(config.ENRICHED_DIR, "step3_enrichments.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"  Wrote: {outpath}")


def _write_coverage_map(rows):
    """Write the incident-to-competency coverage map.
    This is a key Goal deliverable: shows which framework sub-competencies
    are empirically validated by real ATLAS incidents (negative-case evidence)."""

    # Define the full sub-competency framework
    SC_LABELS = {
        "TR-1": "Risk Policy & Accountability",
        "TR-2": "Threat Mapping & Reconnaissance Defense",
        "TR-3": "Monitoring & Detection",
        "TR-4": "Data Governance & Exfiltration Prevention",
        "TR-5": "Regulatory Compliance",
        "TR-6": "Incident Response & Recovery",
        "TR-7": "Human Override & Control",
        "TR-8": "Supply Chain & Third-Party Risk",
        "IR-1": "Orchestration & Execution Controls",
        "IR-2": "Tool-Use Boundaries & Access Control",
        "IR-3": "Nondeterminism Management",
        "IR-4": "RAG Architecture & Data Grounding",
        "IR-5": "GenAIOps / MLOps Lifecycle",
        "IR-6": "Modular Architecture & Resource Controls",
        "IR-7": "HITL Architecture Patterns",
        "IR-8": "Evaluation & Monitoring Infrastructure",
    }

    # Count incidents per sub-competency
    sc_incidents = defaultdict(list)
    for r in rows:
        for sc in r.get("llm_sub_competencies", "").split("; "):
            sc = sc.strip()
            if sc and sc in SC_LABELS:
                sc_incidents[sc].append(r["case_study_id"])

    # Count harm types per sub-competency
    sc_harm_types = defaultdict(Counter)
    for r in rows:
        harm = r.get("harm_type", "")
        for sc in r.get("llm_sub_competencies", "").split("; "):
            sc = sc.strip()
            if sc and sc in SC_LABELS and harm:
                sc_harm_types[sc][harm] += 1

    # Write CSV coverage map
    coverage_rows = []
    for sc_id in sorted(SC_LABELS.keys()):
        incidents = sc_incidents.get(sc_id, [])
        harm_dist = sc_harm_types.get(sc_id, Counter())
        bundle = "Trust Readiness" if sc_id.startswith("TR") else "Integration Readiness"
        coverage_rows.append({
            "sub_competency_id": sc_id,
            "sub_competency_name": SC_LABELS[sc_id],
            "bundle": bundle,
            "incident_count": len(incidents),
            "coverage_status": "validated" if len(incidents) >= 3 else
                              "partial" if len(incidents) >= 1 else "uncovered",
            "incident_ids": "; ".join(incidents[:10]),
            "primary_harm_types": "; ".join(f"{h}({c})" for h, c in harm_dist.most_common(3)),
        })

    outpath = os.path.join(config.ENRICHED_DIR, "step3_coverage_map.csv")
    with open(outpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=coverage_rows[0].keys())
        writer.writeheader()
        writer.writerows(coverage_rows)

    validated = sum(1 for r in coverage_rows if r["coverage_status"] == "validated")
    partial = sum(1 for r in coverage_rows if r["coverage_status"] == "partial")
    uncovered = sum(1 for r in coverage_rows if r["coverage_status"] == "uncovered")
    print(f"  Wrote: {outpath} (coverage: {validated} validated, "
          f"{partial} partial, {uncovered} uncovered)")

    # Write Markdown coverage map (the "incident-mapped validation appendix")
    md_lines = [
        "# Step 3 -- Incident-Mapped Validation Appendix (Coverage Map)",
        "",
        "**Source**: MITRE ATLAS adversarial ML case studies",
        "**Purpose**: Validate that the Trust & Integration Readiness framework",
        "covers real-world AI failure modes (negative-case evidence)",
        "",
        "## Coverage Summary",
        "",
        f"- **Validated** (3+ incidents): {validated} sub-competencies",
        f"- **Partial** (1-2 incidents): {partial} sub-competencies",
        f"- **Uncovered** (0 incidents): {uncovered} sub-competencies",
        f"- **Total incidents coded**: {len(rows)}",
        "",
        "## Trust Readiness Coverage",
        "",
        "| Sub-Competency | Incidents | Status | Primary Harm Types |",
        "|----------------|-----------|--------|-------------------|",
    ]
    for r in coverage_rows:
        if r["bundle"] == "Trust Readiness":
            md_lines.append(
                f"| {r['sub_competency_id']}: {r['sub_competency_name']} | "
                f"{r['incident_count']} | {r['coverage_status']} | "
                f"{r['primary_harm_types'][:60]} |"
            )
    md_lines += [
        "",
        "## Integration Readiness Coverage",
        "",
        "| Sub-Competency | Incidents | Status | Primary Harm Types |",
        "|----------------|-----------|--------|-------------------|",
    ]
    for r in coverage_rows:
        if r["bundle"] == "Integration Readiness":
            md_lines.append(
                f"| {r['sub_competency_id']}: {r['sub_competency_name']} | "
                f"{r['incident_count']} | {r['coverage_status']} | "
                f"{r['primary_harm_types'][:60]} |"
            )

    # Harm type summary across all incidents
    harm_total = Counter(r.get("harm_type", "") for r in rows if r.get("harm_type"))
    md_lines += [
        "",
        "## Harm Type Distribution (All Incidents)",
        "",
        "| Harm Type | Count | Percentage |",
        "|-----------|-------|------------|",
    ]
    for ht, cnt in harm_total.most_common():
        pct = cnt / len(rows) * 100
        md_lines.append(f"| {ht} | {cnt} | {pct:.1f}% |")

    md_lines.append("")

    mdpath = os.path.join(config.ENRICHED_DIR, "step3_coverage_map.md")
    with open(mdpath, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"  Wrote: {mdpath}")


if __name__ == "__main__":
    run()
