"""
Master runner for the agentic analysis pipeline -- AMCIS 2026

Executes all 5 analysis steps in sequence, passing results forward.
Each step reads literature sources using LLM and produces enriched artifacts
in analysis/output/enriched/.

Usage:
    python -m analysis.agents.run_agents          # Run all steps
    python -m analysis.agents.run_agents --step 1 # Run only Step 1
    python -m analysis.agents.run_agents --step 5 # Run only Step 5 (uses cached Steps 1-4)
"""

import argparse, sys, os, time

# Ensure project root is on path
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from scripts.agents import (step1_extract, step2_crosswalk, step3_enrich,
                              step4_synthesize, step5_validate,
                              step6_writing_quality, step7_ref_check,
                              step8_peer_review)
from scripts.agents.llm import print_usage_summary


def main():
    parser = argparse.ArgumentParser(description="AMCIS 2026 Agentic Analysis Pipeline")
    parser.add_argument("--step", type=int, choices=[1, 2, 3, 4, 5, 6, 7, 8],
                        help="Run only a specific step (default: all)")
    args = parser.parse_args()

    t0 = time.time()

    print("=" * 70)
    print("AMCIS 2026 — AGENTIC ANALYSIS PIPELINE v2")
    print("=" * 70)
    print(f"Output directory: analysis/output/enriched/")
    print()

    results = {"step1": None, "step2": None, "step3": None,
               "step4": None, "step5": None, "step6": None,
               "step7": None, "step8": None}
    steps_run = []

    try:
        if args.step is None or args.step == 1:
            t1 = time.time()
            results["step1"] = step1_extract.run()
            steps_run.append(("Step 1 -- Evidence Extraction", time.time() - t1, "OK"))
            print()

        if args.step is None or args.step == 2:
            t1 = time.time()
            results["step2"] = step2_crosswalk.run(step1_results=results["step1"])
            steps_run.append(("Step 2 -- Crosswalk Synthesis", time.time() - t1, "OK"))
            print()

        if args.step is None or args.step == 3:
            t1 = time.time()
            results["step3"] = step3_enrich.run(
                step1_results=results["step1"],
                step2_results=results["step2"],
            )
            steps_run.append(("Step 3 -- Incident Enrichment", time.time() - t1, "OK"))
            print()

        if args.step is None or args.step == 4:
            t1 = time.time()
            results["step4"] = step4_synthesize.run(
                step1_results=results["step1"],
                step2_results=results["step2"],
                step3_results=results["step3"],
            )
            steps_run.append(("Step 4 -- Proposition Synthesis", time.time() - t1, "OK"))
            print()

        if args.step is None or args.step == 5:
            t1 = time.time()
            results["step5"] = step5_validate.run(
                step1_results=results["step1"],
                step2_results=results["step2"],
                step3_results=results["step3"],
                step4_results=results["step4"],
            )
            steps_run.append(("Step 5 -- Claim Validation", time.time() - t1, "OK"))
            print()

        if args.step == 6 or args.step is None:
            t1 = time.time()
            results["step6"] = step6_writing_quality.run()
            steps_run.append(("Step 6 -- Writing Quality", time.time() - t1, "OK"))
            print()

        if args.step == 7 or args.step is None:
            t1 = time.time()
            results["step7"] = step7_ref_check.run()
            steps_run.append(("Step 7 -- Reference Integrity", time.time() - t1, "OK"))
            print()

        if args.step == 8 or args.step is None:
            t1 = time.time()
            results["step8"] = step8_peer_review.run()
            steps_run.append(("Step 8 -- Peer Review Simulation", time.time() - t1, "OK"))
            print()

    except Exception as e:
        steps_run.append((f"FAILED at current step", 0, str(e)))
        print(f"\n  ERROR: {e}")
        import traceback
        traceback.print_exc()

    elapsed = time.time() - t0

    # ── Summary ──────────────────────────────────────────────────────────────
    print()
    print("=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)

    for label, duration, status in steps_run:
        print(f"  [{status:6s}] {label} ({duration:.1f}s)")

    print(f"\n  Total elapsed: {elapsed:.1f}s")

    print_usage_summary()

    # List enriched output files
    enriched_dir = os.path.join(BASE, "analysis", "output", "enriched")
    if os.path.exists(enriched_dir):
        print(f"\nEnriched artifacts:")
        for f in sorted(os.listdir(enriched_dir)):
            size = os.path.getsize(os.path.join(enriched_dir, f))
            print(f"  {f:<55} {size:>8,} bytes")


if __name__ == "__main__":
    main()
