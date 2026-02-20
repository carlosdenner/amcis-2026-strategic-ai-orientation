"""
Step 3 -- Incident Validation via MITRE ATLAS Case Studies
Methodology: parse each case study -> extract failure mode, techniques used,
missing controls (mitigations NOT present), implied competency gap.
Output: CSV table for paper appendix + summary statistics.
"""

import yaml, os, csv, json
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS_DIST = os.path.join(BASE, "Literature", "atlas-data", "dist", "ATLAS.yaml")
OUT_DIR = os.path.join(BASE, "analysis", "output")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Load ATLAS data from resolved dist file ──────────────────────────────────

with open(ATLAS_DIST, encoding="utf-8") as f:
    atlas = yaml.safe_load(f)

matrix      = atlas["matrices"][0]
case_studies = atlas["case-studies"]

tactics     = {t["id"]: t for t in matrix["tactics"]}
techniques  = {t["id"]: t for t in matrix["techniques"]}
mitigations = {m["id"]: m for m in matrix["mitigations"]}

# Build: technique -> mitigations that address it
tech_to_mitigations = defaultdict(list)
for mid, m in mitigations.items():
    # category is a list in this dataset
    cats = m.get("category", [])
    cat_str = cats[0] if isinstance(cats, list) and cats else str(cats)
    for tech_ref in m.get("techniques", []):
        tid = tech_ref if isinstance(tech_ref, str) else tech_ref.get("id", "")
        # strip subtechnique suffix for parent lookup too
        if tid:
            tech_to_mitigations[tid].append({"id": mid, "name": m["name"], "category": cat_str})
            parent = tid.split(".")[0] if "." in tid else None
            if parent and parent != tid:
                tech_to_mitigations[parent].append({"id": mid, "name": m["name"], "category": cat_str})

print(f"Loaded: {len(tactics)} tactics, {len(techniques)} techniques, "
      f"{len(mitigations)} mitigations, {len(case_studies)} case studies")

# ── Competency gap taxonomy ──────────────────────────────────────────────────
# Map ATLAS tactic IDs to framework competency domains

TACTIC_TO_DOMAIN = {
    "AML.TA0000": "Trust Readiness -- Model Access Governance",
    "AML.TA0001": "Integration Readiness -- AI Attack Staging Defense",
    "AML.TA0002": "Trust Readiness -- Threat Intelligence & Reconnaissance Defense",
    "AML.TA0003": "Integration Readiness -- Resource & Supply Chain Controls",
    "AML.TA0004": "Integration Readiness -- Access Boundary & Initial Access Controls",
    "AML.TA0005": "Integration Readiness -- Execution Controls & Sandboxing",
    "AML.TA0006": "Trust Readiness -- Persistence Detection & Monitoring",
    "AML.TA0007": "Trust Readiness -- Defense Evasion Detection",
    "AML.TA0008": "Trust Readiness -- Discovery & Enumeration Controls",
    "AML.TA0009": "Trust Readiness -- Data Collection & Exfiltration Prevention",
    "AML.TA0010": "Trust Readiness -- Data Exfiltration Controls",
    "AML.TA0011": "Trust Readiness -- Impact Containment & Recovery",
    "AML.TA0012": "Integration Readiness -- Privilege & Identity Management",
    "AML.TA0013": "Trust Readiness -- Credential & Secret Management",
    "AML.TA0014": "Integration Readiness -- C2 Detection & Network Controls",
    "AML.TA0015": "Integration Readiness -- Lateral Movement Prevention",
}

MITIGATION_CATEGORY_TO_COMPETENCY = {
    "Detect":          "Trust Readiness -- Monitoring & Eval Governance",
    "Govern":          "Trust Readiness -- AI Governance & Policy",
    "Protect":         "Trust Readiness -- Technical Controls & Hardening",
    "Recover":         "Trust Readiness -- Incident Response & Recovery",
    "Respond":         "Trust Readiness -- Incident Response & Recovery",
    "ML":              "Integration Readiness -- ML Lifecycle Controls",
    "Training":        "Integration Readiness -- Training Data Governance",
    "Inference":       "Integration Readiness -- Inference & Deployment Controls",
}

# ── Process each case study ──────────────────────────────────────────────────

rows = []
tactic_freq   = defaultdict(int)
technique_freq = defaultdict(int)
domain_freq   = defaultdict(int)
mitigation_gap_freq = defaultdict(int)

for cs in case_studies:
    cs_id   = cs.get("id", "")
    cs_name = cs.get("name", "")
    cs_date = str(cs.get("incident-date", ""))
    cs_type = cs.get("case-study-type", "")
    summary = str(cs.get("summary", ""))[:300].replace("\n", " ")

    procedures = cs.get("procedure", []) or []
    target     = cs.get("target", {}) or {}
    actor      = cs.get("actor",  {}) or {}

    target_str = target.get("name", "") if isinstance(target, dict) else str(target)
    actor_str  = actor.get("name",  "") if isinstance(actor,  dict) else str(actor)

    # Collect all techniques used in this case study
    used_technique_ids = set()
    used_tactic_ids    = set()
    for step in procedures:
        # In dist/ATLAS.yaml tactic and technique are plain string IDs
        tac_id = step.get("tactic", "")
        tid    = step.get("technique", "")
        if tac_id:
            used_tactic_ids.add(tac_id)
            tactic_freq[tac_id] += 1
        if tid:
            used_technique_ids.add(tid)
            technique_freq[tid] += 1

    # Derive domains from tactics
    domains = sorted(set(TACTIC_TO_DOMAIN.get(t, "Unknown") for t in used_tactic_ids))

    # Identify missing mitigations (controls that WOULD address used techniques but weren't applied)
    applicable_mitigations = {}
    for tid in used_technique_ids:
        for m in tech_to_mitigations.get(tid, []):
            applicable_mitigations[m["id"]] = m
    missing_controls = [f'{m["id"]}: {m["name"]}' for m in applicable_mitigations.values()]
    for m in applicable_mitigations.values():
        mitigation_gap_freq[m["id"]] += 1

    # Competency gaps from mitigation categories
    comp_gaps = sorted(set(
        MITIGATION_CATEGORY_TO_COMPETENCY.get(m.get("category",""), "Trust Readiness -- General Governance")
        for m in applicable_mitigations.values()
    ))
    for d in domains:
        domain_freq[d] += 1

    rows.append({
        "case_study_id":    cs_id,
        "name":             cs_name,
        "incident_date":    cs_date,
        "type":             cs_type,
        "actor":            actor_str,
        "target":           target_str,
        "summary":          summary,
        "tactics_used":     "; ".join(sorted(used_tactic_ids)),
        "techniques_used":  "; ".join(sorted(used_technique_ids)),
        "technique_count":  len(used_technique_ids),
        "competency_domains": "; ".join(domains),
        "missing_controls": "; ".join(missing_controls[:5]),  # top 5 for readability
        "competency_gaps":  "; ".join(comp_gaps),
    })

# ── Write main incident coding table ────────────────────────────────────────

out_csv = os.path.join(OUT_DIR, "step3_incident_coding.csv")
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print(f"\nWrote: {out_csv} ({len(rows)} rows)")

# ── Write tactic frequency summary ──────────────────────────────────────────

tac_summary = sorted(
    [{"tactic_id": k, "tactic_name": tactics.get(k,{}).get("name","?"),
      "incident_count": v, "competency_domain": TACTIC_TO_DOMAIN.get(k,"?")}
     for k, v in tactic_freq.items()],
    key=lambda x: -x["incident_count"]
)
out_tac = os.path.join(OUT_DIR, "step3_tactic_frequency.csv")
with open(out_tac, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=tac_summary[0].keys())
    writer.writeheader()
    writer.writerows(tac_summary)
print(f"Wrote: {out_tac}")

# ── Write mitigation gap frequency (most-needed controls) ───────────────────

def get_cat_str(m):
    cats = m.get("category", [])
    return cats[0] if isinstance(cats, list) and cats else str(cats)

mit_gap_summary = sorted(
    [{"mitigation_id": k,
      "mitigation_name": mitigations.get(k,{}).get("name","?"),
      "category": get_cat_str(mitigations.get(k,{})),
      "incident_count": v,
      "competency_gap": MITIGATION_CATEGORY_TO_COMPETENCY.get(
          get_cat_str(mitigations.get(k,{})), "Trust Readiness -- General Governance")}
     for k, v in mitigation_gap_freq.items()],
    key=lambda x: -x["incident_count"]
)
out_mit = os.path.join(OUT_DIR, "step3_mitigation_gaps.csv")
if mit_gap_summary:
    with open(out_mit, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=mit_gap_summary[0].keys())
        writer.writeheader()
        writer.writerows(mit_gap_summary)
    print(f"Wrote: {out_mit}")
else:
    print("WARNING: No mitigation gaps found -- technique IDs may not match mitigation technique refs")

# ── Print console summary ────────────────────────────────────────────────────

print("\n" + "="*60)
print("STEP 3 SUMMARY -- INCIDENT VALIDATION")
print("="*60)
print(f"Total case studies coded: {len(rows)}")
print(f"Unique tactics observed:  {len(tactic_freq)}")
print(f"Unique techniques used:   {len(technique_freq)}")
print(f"Unique mitigation gaps:   {len(mitigation_gap_freq)}")

print("\nTop 10 tactics by incident frequency:")
for t in tac_summary[:10]:
    print(f"  [{t['incident_count']:2d}x] {t['tactic_id']} {t['tactic_name']}")
    print(f"        -> {t['competency_domain']}")

print("\nTop 10 most-needed missing controls:")
for m in mit_gap_summary[:10]:
    print(f"  [{m['incident_count']:2d}x] {m['mitigation_id']} {m['mitigation_name']} ({m['category']})")
    print(f"        -> {m['competency_gap']}")

print("\nCompetency domain coverage:")
for d, cnt in sorted(domain_freq.items(), key=lambda x: -x[1]):
    bundle = "TRUST" if "Trust" in d else "INTEGRATION"
    print(f"  [{cnt:2d}x] [{bundle}] {d}")
