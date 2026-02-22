"""Explore ATLAS data for threat characterization section."""
import pandas as pd
import yaml
import pathlib

BASE = pathlib.Path(".")

# Load ATLAS enriched cases
atlas = pd.read_csv("data/processed/atlas_cases_enriched.csv")
print("ATLAS enriched columns:", list(atlas.columns))
print(f"ATLAS cases: {len(atlas)}")
print()

# Load tactics
with open("data/raw/atlas/data/tactics.yaml") as f:
    tactics = yaml.safe_load(f)
print(f"ATLAS tactics ({len(tactics)}):")
for t in tactics:
    print(f"  {t['id']:20s}  {t['name']}")

# Load mitigations
with open("data/raw/atlas/data/mitigations.yaml") as f:
    mitigations = yaml.safe_load(f)
print(f"\nATLAS mitigations ({len(mitigations)}):")
for m in mitigations:
    print(f"  {m['id']:20s}  {m['name']}")

# Load case studies (individual YAML files in directory)
import glob
cases = []
for fp in sorted(glob.glob("data/raw/atlas/data/case-studies/*.yaml")):
    with open(fp) as f:
        cases.append(yaml.safe_load(f))
print(f"\nATLAS case studies: {len(cases)}")
print(f"Case study keys: {list(cases[0].keys())}")
print(f"Example procedure: {cases[0].get('procedure', [])[:2]}")

# Tactic frequency across cases
from collections import Counter
tactic_counter = Counter()
techniques_per_case = []
for c in cases:
    case_tactics = set()
    procedures = c.get("procedure", [])
    n_techniques = len(procedures)
    techniques_per_case.append(n_techniques)
    for p in procedures:
        tech_id = p.get("technique", "")
        # Extract tactic from technique ID (e.g., AML.T0001 -> tactic comes from technique mapping)
        tactic_counter[tech_id] = tactic_counter.get(tech_id, 0) + 1

print(f"\nTechniques per case: mean={sum(techniques_per_case)/len(techniques_per_case):.1f}, max={max(techniques_per_case)}, min={min(techniques_per_case)}")

# Load techniques to map to tactics
with open("data/raw/atlas/data/techniques.yaml") as f:
    techniques = yaml.safe_load(f)

tech_to_tactic = {}
for t in techniques:
    tid = t["id"]
    tac_refs = t.get("tactics", [])
    for tac in tac_refs:
        tech_to_tactic[tid] = tac

# Now count tactics across case procedures
tactic_freq = Counter()
for c in cases:
    case_tactics = set()
    for p in c.get("procedure", []):
        tech_id = p.get("technique", "")
        tac = tech_to_tactic.get(tech_id, "Unknown")
        case_tactics.add(tac)
    for tac in case_tactics:
        tactic_freq[tac] += 1

tactic_names = {t["id"]: t["name"] for t in tactics}
print(f"\nTactic frequency (cases using each):")
for tac, count in tactic_freq.most_common():
    name = tactic_names.get(tac, tac)
    print(f"  {tac:20s}  {name:40s}  {count:3d} cases ({count/len(cases)*100:.0f}%)")

# Mitigation frequency
mit_counter = Counter()
for c in cases:
    for p in c.get("procedure", []):
        for m_ref in p.get("mitigations", []):
            mit_counter[m_ref] += 1

mit_names = {m["id"]: m["name"] for m in mitigations}
print(f"\nMitigation frequency (procedure references):")
for mid, count in mit_counter.most_common(15):
    name = mit_names.get(mid, mid)
    print(f"  {mid:20s}  {name:50s}  {count:3d}")

# Chain dependencies
print(f"\nAttack chain analysis:")
chain_pairs = Counter()
for c in cases:
    procs = c.get("procedure", [])
    # ordered by step
    tac_sequence = []
    for p in procs:
        tech_id = p.get("technique", "")
        tac = tech_to_tactic.get(tech_id, "Unknown")
        if tac not in tac_sequence:
            tac_sequence.append(tac)
    for i in range(len(tac_sequence) - 1):
        pair = (tac_sequence[i], tac_sequence[i+1])
        chain_pairs[pair] += 1

print("Top attack chain transitions (tactic A -> B):")
for (a, b), count in chain_pairs.most_common(10):
    a_name = tactic_names.get(a, a)
    b_name = tactic_names.get(b, b)
    print(f"  {a_name:30s} -> {b_name:30s}  {count} cases")
