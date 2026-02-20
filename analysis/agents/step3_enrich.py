"""
Step 3 Agent — Incident Coding Enrichment

Reads ATLAS case studies, fixes the mitigation-to-competency mapping,
and uses LLM to generate natural-language competency gap descriptions
for each incident, grounded in the framework's sub-competencies.
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

Below is a batch of ATLAS case study incidents. For each incident, provide:

1. A concise competency gap description (1-2 sentences) explaining what \
   organizational capability was missing, framed in terms of Trust Readiness \
   (governance/policy) or Integration Readiness (architecture/engineering).
2. Map to the most relevant sub-competency ID(s) from this framework:
   Trust Readiness: TR-1 (Risk Policy), TR-2 (Threat Mapping), TR-3 (Monitoring), \
   TR-4 (Data Governance), TR-5 (Regulatory Compliance), TR-6 (Incident Response), \
   TR-7 (Human Override), TR-8 (Supply Chain Risk)
   Integration Readiness: IR-1 (Orchestration), IR-2 (Tool-Use Boundaries), \
   IR-3 (Nondeterminism), IR-4 (RAG Architecture), IR-5 (GenAIOps), \
   IR-6 (Modular Architecture), IR-7 (HITL Architecture), IR-8 (Eval Infrastructure)
3. Classify the primary failure mode as: "prevention_failure" (attack succeeded \
   because controls weren't in place), "detection_failure" (attack went undetected), \
   or "response_failure" (attack was detected but response was inadequate).

Incidents:
{incidents_json}

Return JSON:
{{
  "enrichments": [
    {{
      "case_study_id": "AML.CSXXXX",
      "competency_gap_description": "...",
      "primary_sub_competencies": ["TR-X", "IR-Y"],
      "failure_mode": "prevention_failure|detection_failure|response_failure",
      "trust_integration_split": "trust-dominant|integration-dominant|both"
    }}
  ]
}}
"""


def run(step1_results: list = None, step2_results: list = None):
    """Execute Step 3 agent: enrich ATLAS incident coding."""
    print("=" * 70)
    print("STEP 3 AGENT — Incident Coding Enrichment")
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

    # Send incidents in batches for LLM enrichment
    enrichments = {}
    batch_size = 13
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i+batch_size]
        batch_summaries = [
            {"case_study_id": r["case_study_id"], "name": r["name"],
             "summary": r["summary"][:200],
             "tactics_used": r["tactics_used"],
             "missing_controls": r["missing_controls"][:200],
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
        row["llm_gap_description"] = e.get("competency_gap_description", "")
        row["llm_sub_competencies"] = "; ".join(e.get("primary_sub_competencies", []))
        row["failure_mode"] = e.get("failure_mode", "")
        row["trust_integration_split"] = e.get("trust_integration_split", "")

    # ── Write outputs ────────────────────────────────────────────────────────
    _write_incident_coding(rows)
    _write_tactic_frequency(tactic_freq, tactics_data)
    _write_mitigation_gaps(mitigation_gap_freq, mitigations)
    _write_enrichment_json(rows)

    # ── Print summary ────────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("STEP 3 AGENT SUMMARY")
    print(f"{'='*70}")
    print(f"Case studies coded: {len(rows)}")
    print(f"Unique tactics: {len(tactic_freq)}")
    print(f"Unique mitigation gaps: {len(mitigation_gap_freq)}")

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


if __name__ == "__main__":
    run()
