"""
Step 5 Agent -- Claim Validation & Cross-Step Consistency

Performs adversarial validation on the entire pipeline output:
1. Evidence Audit: checks that all [#XX] citations actually exist in sources
2. Cross-Step Consistency: verifies Step 4 claims match Step 2-3 data
3. Claim Strength Scoring: rates each proposition's overall evidence quality
4. Gap Report: identifies where the pipeline's claims outrun its evidence
"""

import csv, json, os, re
from collections import Counter, defaultdict
from . import config
from .literature_loader import load_all_readable
from .llm import chat_json

SYSTEM_PROMPT = """\
You are a CRITICAL REVIEWER of an academic IS research paper. Your role is to \
find weaknesses, unsupported claims, and logical gaps -- NOT to validate or praise.

Your review standards:
1. A claim without traceable evidence in the corpus is UNSUPPORTED.
2. A statistic that doesn't match computed data is an ERROR.
3. A citation to a source that doesn't discuss the cited topic is MISLEADING.
4. Confidence inflation (saying "strong evidence" when evidence is thin) is a RED FLAG.
5. If you find no issues, say so -- but look hard first.
"""

VALIDATION_PROMPT = """\
You are reviewing the final output of an automated research pipeline for an \
AMCIS 2026 paper. Below are:

1. The 5 grounded propositions (from Step 4)
2. The computed crosswalk statistics (from Step 2)
3. The computed incident statistics (from Step 3)
4. A summary of the literature corpus available

Your task: Identify ALL issues in the following categories.

ISSUE CATEGORIES:
A. CITATION ERRORS: Claims that cite [#XX] but the source doesn't actually \
   discuss what's claimed. (Check against the corpus summary.)
B. STATISTIC MISMATCHES: Numbers in proposition rationales that don't match \
   the computed statistics provided.
C. OVERCLAIMED EVIDENCE: Assertions stated with high confidence but supported \
   by only 1 source or only indirect evidence.
D. LOGICAL GAPS: Steps in the argument where the inferential leap is too large.
E. MISSING COUNTER-EVIDENCE: Evidence in the corpus that CONTRADICTS a \
   proposition but is not acknowledged.
F. CROSS-STEP INCONSISTENCIES: Where Step 4 claims something that Step 2 or \
   Step 3 data doesn't support.

PROPOSITIONS TO REVIEW:
{propositions_json}

COMPUTED STEP 2 STATISTICS:
{step2_stats}

COMPUTED STEP 3 STATISTICS:
{step3_stats}

CORPUS SUMMARY (available sources):
{corpus_summary}

Return JSON:
{{
  "validation_issues": [
    {{
      "issue_id": "V-01",
      "category": "A|B|C|D|E|F",
      "proposition_id": "P1|P2|P3|P4|P5|GENERAL",
      "severity": "critical|major|minor",
      "description": "Specific description of the issue",
      "evidence": "What in the data supports this finding",
      "recommendation": "How to fix or mitigate this issue"
    }}
  ],
  "proposition_scores": [
    {{
      "proposition_id": "P1",
      "evidence_strength": "strong|moderate|weak",
      "corpus_support": "Number of corpus sources that directly support this",
      "key_vulnerability": "The single biggest weakness of this proposition",
      "overall_assessment": "1-2 sentence summary"
    }}
  ],
  "pipeline_assessment": {{
    "overall_quality": "high|medium|low",
    "strongest_proposition": "PX -- justification",
    "weakest_proposition": "PX -- justification",
    "critical_fixes_needed": ["list of must-fix items before publication"],
    "confidence_in_framework": "Your honest assessment of the framework's evidence base"
  }}
}}
"""


def run(step1_results=None, step2_results=None, step3_results=None,
        step4_results=None):
    """Execute Step 5: validate claims and check cross-step consistency."""
    print("=" * 70)
    print("STEP 5 AGENT -- Claim Validation & Cross-Step Consistency")
    print("=" * 70)

    # ── Load all prior step outputs ──────────────────────────────────────────
    step4_data = _load_step_data(step4_results, "step4_propositions.json")
    step2_stats = _compute_step2_stats(step2_results)
    step3_stats = _compute_step3_stats(step3_results)
    corpus_summary = _build_corpus_summary()

    if not step4_data:
        print("  ERROR: No Step 4 data available. Run Steps 1-4 first.")
        return None

    print(f"  Loaded {len(step4_data)} propositions for validation")
    print(f"  Corpus summary: {len(corpus_summary)} chars")

    # ── Phase 1: Automated citation checking ─────────────────────────────────
    print("\n  Phase 1: Automated citation checking...")
    auto_issues = _automated_citation_check(step4_data)
    print(f"    Found {len(auto_issues)} automated issues")

    # ── Phase 2: LLM-powered adversarial review ─────────────────────────────
    print("\n  Phase 2: LLM adversarial review...")
    prompt = VALIDATION_PROMPT.format(
        propositions_json=json.dumps(step4_data, indent=2)[:80_000],
        step2_stats=step2_stats,
        step3_stats=step3_stats,
        corpus_summary=corpus_summary,
    )

    llm_review = chat_json(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        model=config.SYNTHESIS_MODEL,
        max_tokens=config.MAX_OUTPUT_TOKENS,
    )
    if isinstance(llm_review, list):
        llm_review = {"validation_issues": llm_review}

    # ── Phase 3: Cross-step consistency checks ───────────────────────────────
    print("\n  Phase 3: Cross-step consistency checks...")
    consistency_issues = _cross_step_consistency(step2_results, step3_results,
                                                  step4_data)
    print(f"    Found {len(consistency_issues)} consistency issues")

    # ── Merge all findings ───────────────────────────────────────────────────
    all_issues = auto_issues + llm_review.get("validation_issues", []) + consistency_issues

    # Deduplicate by description similarity (rough)
    seen = set()
    unique_issues = []
    for issue in all_issues:
        key = (issue.get("proposition_id", ""), issue.get("category", ""),
               issue.get("description", "")[:80])
        if key not in seen:
            seen.add(key)
            unique_issues.append(issue)

    # Number the issues sequentially
    for i, issue in enumerate(unique_issues, 1):
        issue["issue_id"] = f"V-{i:02d}"

    result = {
        "validation_issues": unique_issues,
        "proposition_scores": llm_review.get("proposition_scores", []),
        "pipeline_assessment": llm_review.get("pipeline_assessment", {}),
    }

    # ── Write outputs ────────────────────────────────────────────────────────
    _write_validation_report(result)
    _write_issues_csv(unique_issues)
    _write_json(result)

    # ── Print summary ────────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("STEP 5 VALIDATION SUMMARY")
    print(f"{'='*70}")
    severity_counts = Counter(i.get("severity", "") for i in unique_issues)
    category_counts = Counter(i.get("category", "") for i in unique_issues)
    print(f"  Total issues: {len(unique_issues)}")
    print(f"  By severity: {dict(severity_counts)}")
    print(f"  By category: {dict(category_counts)}")

    assessment = result.get("pipeline_assessment", {})
    print(f"  Overall quality: {assessment.get('overall_quality', 'N/A')}")
    print(f"  Strongest: {assessment.get('strongest_proposition', 'N/A')}")
    print(f"  Weakest: {assessment.get('weakest_proposition', 'N/A')}")

    fixes = assessment.get("critical_fixes_needed", [])
    if fixes:
        print(f"  Critical fixes needed ({len(fixes)}):")
        for fix in fixes:
            print(f"    - {fix}")

    return result


def _load_step_data(passed_data, filename):
    """Load step data from passed results or enriched output file."""
    if passed_data:
        return passed_data
    path = os.path.join(config.ENRICHED_DIR, filename)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None


def _automated_citation_check(propositions: list) -> list:
    """Check that all [#XX] citations reference actual corpus sources."""
    valid_ids = set(config.LITERATURE_FILES.keys())
    issues = []

    for prop in propositions:
        pid = prop.get("proposition_id", prop.get("id", "?"))
        # Check across all text fields
        text_fields = ["rationale", "crosswalk_evidence", "atlas_evidence"]
        for field in text_fields:
            text = prop.get(field, "")
            if not text:
                continue
            cited = set(re.findall(r"\[?(#\d+)\]?", text))
            for cid in cited:
                if cid not in valid_ids:
                    issues.append({
                        "issue_id": "AUTO",
                        "category": "A",
                        "proposition_id": pid,
                        "severity": "major",
                        "description": f"Citation {cid} in '{field}' does not match any corpus source",
                        "evidence": f"Valid source IDs: {sorted(valid_ids)[:10]}...",
                        "recommendation": f"Remove or replace citation {cid}",
                    })

        # Check grounding sources
        for src in prop.get("grounding_sources", []):
            src_ids = re.findall(r"#\d+", str(src))
            for sid in src_ids:
                if sid not in valid_ids:
                    issues.append({
                        "issue_id": "AUTO",
                        "category": "A",
                        "proposition_id": pid,
                        "severity": "minor",
                        "description": f"Grounding source reference {sid} not in corpus",
                        "evidence": f"Source text: {str(src)[:100]}",
                        "recommendation": "Remove non-corpus reference from grounding sources",
                    })

    return issues


def _cross_step_consistency(step2_results, step3_results, step4_data) -> list:
    """Check consistency between steps."""
    issues = []

    # Load step2 data
    if not step2_results:
        path = os.path.join(config.ENRICHED_DIR, "step2_crosswalk_evidence.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                step2_results = json.load(f)

    # Load step3 data
    if not step3_results:
        path = os.path.join(config.ENRICHED_DIR, "step3_enrichments.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                step3_results = json.load(f)

    if step2_results:
        # Check: Step 4 claims about bundle distribution match Step 2 data
        bundle_counts = Counter(r.get("bundle", "") for r in step2_results)
        total_reqs = len(step2_results)

        for prop in step4_data:
            text = prop.get("crosswalk_evidence", "")
            # Look for specific numbers claimed about requirements
            claimed_numbers = re.findall(r"(\d+)\s*(?:of\s*)?(?:\d+\s*)?(?:requirements?|reqs?)", text)
            for num in claimed_numbers:
                n = int(num)
                if n > total_reqs:
                    issues.append({
                        "issue_id": "CONSIST",
                        "category": "F",
                        "proposition_id": prop.get("proposition_id", prop.get("id", "?")),
                        "severity": "major",
                        "description": f"Claims {n} requirements but Step 2 only has {total_reqs}",
                        "evidence": f"Step 2 total: {total_reqs}, Bundle distribution: {dict(bundle_counts)}",
                        "recommendation": "Update to use actual computed statistics",
                    })

    if step3_results:
        # Check: Step 4 claims about incident counts match Step 3 data
        total_incidents = len(step3_results)
        fm_counts = Counter(r.get("failure_mode", "") for r in step3_results)

        for prop in step4_data:
            text = prop.get("atlas_evidence", "")
            claimed_incidents = re.findall(r"(\d+)\s*(?:of\s*)?(?:\d+\s*)?(?:incidents?|case.?stud)", text)
            for num in claimed_incidents:
                n = int(num)
                if n > total_incidents * 1.5:  # allow some rounding
                    issues.append({
                        "issue_id": "CONSIST",
                        "category": "F",
                        "proposition_id": prop.get("proposition_id", prop.get("id", "?")),
                        "severity": "major",
                        "description": f"Claims {n} incidents but Step 3 only has {total_incidents}",
                        "evidence": f"Step 3 total: {total_incidents}, Failure modes: {dict(fm_counts)}",
                        "recommendation": "Update to use actual computed statistics",
                    })

    return issues


def _compute_step2_stats(step2_results) -> str:
    """Reuse Step 4's stat computation for consistency."""
    # Import Step 4's function to avoid duplication
    from .step4_synthesize import _compute_step2_stats as s4_stats
    return s4_stats(step2_results)


def _compute_step3_stats(step3_results) -> str:
    """Reuse Step 4's stat computation for consistency."""
    from .step4_synthesize import _compute_step3_stats as s4_stats
    return s4_stats(step3_results)


def _build_corpus_summary() -> str:
    """Build a summary of available corpus sources for validation context."""
    lines = ["Available corpus sources:"]
    for sid, meta in sorted(config.LITERATURE_FILES.items()):
        lines.append(f"  {sid}: {meta['label']} [{meta['type']}]")
    return "\n".join(lines)


def _write_validation_report(result: dict):
    """Write the validation report as Markdown."""
    lines = [
        "# Step 5 -- Claim Validation & Cross-Step Consistency Report",
        "",
        "**Generated by**: Adversarial validation agent",
        "**Paper**: Strategic AI Orientation Enabled by Trust & Integration Readiness",
        "**Venue**: AMCIS 2026",
        "",
        "---",
        "",
    ]

    # Pipeline assessment
    assessment = result.get("pipeline_assessment", {})
    lines += [
        "## Pipeline Assessment",
        "",
        f"**Overall Quality**: {assessment.get('overall_quality', 'N/A')}",
        "",
        f"**Strongest Proposition**: {assessment.get('strongest_proposition', 'N/A')}",
        "",
        f"**Weakest Proposition**: {assessment.get('weakest_proposition', 'N/A')}",
        "",
        f"**Framework Confidence**: {assessment.get('confidence_in_framework', 'N/A')}",
        "",
    ]

    fixes = assessment.get("critical_fixes_needed", [])
    if fixes:
        lines += ["### Critical Fixes Needed", ""]
        for fix in fixes:
            lines.append(f"1. {fix}")
        lines.append("")

    # Proposition scores
    scores = result.get("proposition_scores", [])
    if scores:
        lines += [
            "## Proposition Evidence Scores",
            "",
            "| Proposition | Evidence Strength | Corpus Support | Key Vulnerability |",
            "|-------------|------------------|----------------|-------------------|",
        ]
        for s in scores:
            lines.append(
                f"| {s.get('proposition_id', '')} | {s.get('evidence_strength', '')} | "
                f"{s.get('corpus_support', '')} | {s.get('key_vulnerability', '')[:60]} |"
            )
        lines.append("")

    # Validation issues
    issues = result.get("validation_issues", [])
    if issues:
        lines += ["## Validation Issues", ""]

        # Group by severity
        for severity in ["critical", "major", "minor"]:
            sev_issues = [i for i in issues if i.get("severity") == severity]
            if sev_issues:
                lines += [f"### {severity.upper()} Issues ({len(sev_issues)})", ""]
                for issue in sev_issues:
                    lines += [
                        f"**{issue.get('issue_id', '?')}** [{issue.get('category', '?')}] "
                        f"Proposition {issue.get('proposition_id', '?')}",
                        "",
                        f"> {issue.get('description', '')}",
                        "",
                        f"*Evidence*: {issue.get('evidence', '')}",
                        "",
                        f"*Recommendation*: {issue.get('recommendation', '')}",
                        "",
                    ]

    outpath = os.path.join(config.ENRICHED_DIR, "step5_validation_report.md")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Wrote: {outpath}")


def _write_issues_csv(issues: list):
    """Write validation issues as CSV."""
    if not issues:
        return
    fieldnames = ["issue_id", "category", "proposition_id", "severity",
                  "description", "evidence", "recommendation"]
    outpath = os.path.join(config.ENRICHED_DIR, "step5_validation_issues.csv")
    with open(outpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(issues)
    print(f"  Wrote: {outpath} ({len(issues)} issues)")


def _write_json(result: dict):
    """Write full validation result as JSON."""
    outpath = os.path.join(config.ENRICHED_DIR, "step5_validation.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"  Wrote: {outpath}")


if __name__ == "__main__":
    run()
