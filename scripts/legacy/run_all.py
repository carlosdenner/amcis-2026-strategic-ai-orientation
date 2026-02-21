"""
Master pipeline runner -- AMCIS 2026
Executes all 4 methodology steps in sequence and prints a consolidated summary.
Run from the project root: python analysis/run_all.py
"""

import subprocess, sys, os, time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEPS = [
    ("Step 1 -- Scoping Review: Construct Definitions", "analysis/step1_construct_definitions.py"),
    ("Step 2 -- Crosswalk Coding: Governance x Architecture Matrix", "analysis/step2_crosswalk.py"),
    ("Step 3 -- Incident Validation: MITRE ATLAS Case Studies", "analysis/step3_atlas_incident_coding.py"),
    ("Step 4 -- Strategic Linkage: Propositions", "analysis/step4_strategic_linkage.py"),
]

print("=" * 70)
print("AMCIS 2026 -- Strategic AI Orientation Analysis Pipeline")
print("=" * 70)
print()

results = []
for label, script in STEPS:
    print(f">>> {label}")
    print("-" * 70)
    t0 = time.time()
    result = subprocess.run(
        [sys.executable, os.path.join(BASE, script)],
        cwd=BASE,
        capture_output=False,
    )
    elapsed = time.time() - t0
    status = "OK" if result.returncode == 0 else "FAILED"
    results.append((label, script, status, elapsed))
    print(f"    [{status}] in {elapsed:.1f}s")
    print()

print("=" * 70)
print("PIPELINE COMPLETE")
print("=" * 70)
for label, script, status, elapsed in results:
    print(f"  [{status:6s}] {label}")

print()
print("Output artifacts in: analysis/output/")
out_dir = os.path.join(BASE, "analysis", "output")
for f in sorted(os.listdir(out_dir)):
    size = os.path.getsize(os.path.join(out_dir, f))
    print(f"  {f:<45} {size:>8,} bytes")
