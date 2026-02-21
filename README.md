# AMCIS 2026 — Strategic AI Orientation Enabled by Trust & Integration Readiness

Research project for the **Americas Conference on Information Systems (AMCIS) 2026**.

## Thesis

CIOs shape a firm's **AI orientation** (strategic intent / direction for AI), but the ability to realise that orientation depends on two enabling capability bundles:

1. **Trust / Governance Readiness** — grounded in NIST AI RMF, EU AI Act, OWASP Top-10 for LLMs, and MITRE ATLAS.
2. **Integration / Architecture Readiness** — grounded in agentic-AI design patterns, Azure Well-Architected AI guidance, and GenAIOps practices.

## Repository Structure

```
├── Goal.txt                          # Research goals & design overview
├── Planning - Concepts, Framework…   # Conceptual framework (HTM export)
├── requirements.txt                  # Python dependencies
├── Literature/                       # Source documents (HTML, Markdown, PDF)
│   ├── atlas-data/                   # MITRE ATLAS adversarial-threat data
│   ├── aiid-data/                    # AI Incident Database snapshot
│   └── eo13960-data/                 # EO 13960 federal AI inventory
├── analysis/                         # Python analysis pipeline
│   ├── run_all.py                    # Master pipeline runner (original 4 steps)
│   ├── cross_taxonomy_mapping.py     # Cross-taxonomy bridging table
│   ├── prepare_datasets.py           # Analysis-ready dataset preparation
│   ├── generate_figures.py           # Publication-ready figures
│   ├── profile_sources.py            # Source profiling script
│   ├── profile_eo13960.py            # EO 13960 deep governance profiling
│   └── output/                       # Generated artifacts (CSV, Markdown, PNG)
│       ├── cross_taxonomy_map.csv    # 126 links: ATLAS × AIID × EO 13960 → McKinsey
│       ├── aiid_incidents_classified.csv  # Merged AIID + CSET + GMF
│       ├── atlas_cases_enriched.csv  # Case studies + constraint tags
│       ├── eo13960_scored.csv        # Governance readiness scores
│       ├── unified_evidence_base.csv # Long-format stacked evidence
│       ├── research_angles_summary.md # Co-author briefing document
│       ├── figures/                  # Publication-ready visualizations
│       └── enriched/                 # LLM-enriched artifacts
```

### Data Sources (3 secondary data repositories)

| Source | Records | Type | Licence |
|--------|--------:|------|---------|
| MITRE ATLAS | 52 case studies, 16 tactics, 155 techniques, 35 mitigations | Adversarial threat knowledge base | Apache 2.0 |
| AI Incident Database (AIID) | 1,362 incidents, 6,681 reports | Real-world AI failure repository | CC BY-SA 4.0 |
| EO 13960 Federal AI Inventory | 1,757 use cases × 62 variables × 38 agencies | Government AI practice data | Public domain |

### McKinsey "Constraints to Scale" Alignment

The cross-taxonomy mapping anchors all three data sources to McKinsey's
Exhibit 5 barriers (Feb 2026, "The new CIO mandate"):

| ID | Constraint | % | Primary Data Evidence |
|----|-----------|---:|----------------------|
| C1 | Talent / capability gaps | 31% | ATLAS (reconnaissance), AIID (misuse) |
| C2 | Integration complexity | 29% | ATLAS (lateral movement, agent segmentation), AIID (latency) |
| C3 | Security / reliability / hallucinations | 26% | ATLAS (65 links), AIID (generalization, bias), EO 13960 (Tier-2 gap) |
| C4 | Regulatory / privacy / compliance | 24% | ATLAS (exfiltration), AIID (transparency, bias), EO 13960 (safeguards) |
| C5 | Lack of modern data foundations | 21% | ATLAS (collection/discovery), AIID (data noise) |
| C7 | Difficulty measuring ROI / value | 17% | EO 13960 (post-deploy monitoring) |
| C8 | Internal resistance / change management | 16% | ATLAS (HITL), AIID (misuse), EO 13960 (stakeholders) |

### Analysis Pipeline

| Step | Script | Purpose |
|------|--------|---------|
| 1 | `step1_construct_definitions.py` | Scoping review — construct definitions & sub-competencies |
| 2 | `step2_crosswalk.py` | Crosswalk coding — governance × architecture matrix |
| 3 | `step3_atlas_incident_coding.py` | Incident validation via MITRE ATLAS case studies |
| 4 | `step4_strategic_linkage.py` | Strategic linkage — propositions |

Run the full pipeline from the project root:

```bash
python analysis/run_all.py
```

## Key Artifacts (in `analysis/output/`)

- **step1_construct_definitions.md / step1_sub_competencies.csv** — Construct boundaries
- **step2_crosswalk_matrix.csv / step2_competency_statements.csv** — Governance ↔ architecture crosswalk
- **step3_incident_coding.csv / step3_tactic_frequency.csv / step3_mitigation_gaps.csv** — ATLAS incident mapping
- **step4_propositions.md / step4_propositions.csv** — Testable propositions

### Agentic Pipeline (in `analysis/output/enriched/`)

The `analysis/agents/` directory contains an LLM-powered enrichment pipeline that
reads literature sources, extracts evidence passages, and generates grounded
artifacts with auditable citation trails.

```bash
# Run full agentic pipeline
python -m analysis.agents.run_agents

# Run a single step
python -m analysis.agents.run_agents --step 1
```

| Step | Agent | Purpose |
|------|-------|---------|
| 1 | `step1_extract.py` | Extract evidence from literature → enriched construct definitions |
| 2 | `step2_crosswalk.py` | Generate crosswalk with source-passage citations |
| 3 | `step3_enrich.py` | Fix mitigation mapping + LLM competency gap descriptions |
| 4 | `step4_synthesize.py` | Compute cross-step statistics + grounded propositions |

Requires: `OPENAI_API_KEY` environment variable. Uses `gpt-4.1-mini` for extraction
and `gpt-4.1` for synthesis.

## License

Private academic research — all rights reserved.
