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
├── Literature/                       # Source documents (HTML, Markdown, PDF)
│   └── atlas-data/                   # MITRE ATLAS adversarial-threat data
├── analysis/                         # Python analysis pipeline (4 steps)
│   ├── run_all.py                    # Master pipeline runner
│   ├── step1_construct_definitions.py
│   ├── step2_crosswalk.py
│   ├── step3_atlas_incident_coding.py
│   ├── step4_strategic_linkage.py
│   └── output/                       # Generated artifacts (CSV, Markdown)
```

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
