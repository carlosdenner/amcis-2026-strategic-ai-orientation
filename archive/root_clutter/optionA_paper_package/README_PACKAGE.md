# Option A Paper Package — Handoff Document

**Project:** AMCIS 2026 — "Strategic AI Orientation Enabled by Trust & Integration Readiness"  
**Chosen Angle:** Option A — Threat → Gap → Safeguard  
**Research Question:** *How do adversarial AI threats and real-world AI failures expose governance readiness gaps in organizational AI deployment?*  
**Date:** February 22, 2026  
**Purpose:** Comprehensive handoff package for drafting the 10-page AMCIS paper.

---

## 1. Project Overview

We are writing a 10-page conference paper for AMCIS 2026 that triangulates three public secondary data sources — MITRE ATLAS, the AI Incident Database, and the U.S. Federal AI Use Case Inventory — to reveal systematic governance readiness gaps in organizational AI deployment. Our CIO-centric theoretical lens (upper echelons + dynamic managerial capabilities) frames these gaps as missing trust readiness and integration readiness capabilities.

We ran 400 automated experiments using AstaLabs AutoDiscovery (a Bayesian surprise-based data exploration engine) across sessions on our consolidated datasets: 100 experiments in Session 1 (processed datasets only) and 300 experiments in Session 2 (full raw data from all three sources). We must now distill this massive evidence base into a coherent, publication-worthy 10-page story.

---

## 2. File Inventory

### Core Documents

| File | What it contains | Use for |
|------|-----------------|---------|
| `docs/Goal.txt` | Original project blueprint — thesis, method design, artifact plan | Framing & scope |
| `docs/research_angles_summary.md` | Three research angle options, Option A confirmed, updated analysis plan with 6 propositions | Strategy & next steps |
| `paper/paper.md` | **Current paper draft** — Abstract, Intro, Theoretical Background, Methodology complete. Findings, Discussion, Implications, Conclusion are TODO | Writing continuation |

### Data Pipeline Outputs

| File | What it contains |
|------|-----------------|
| `data/processed/step1_construct_definitions.md` | Full construct definitions: AI Orientation, Trust Readiness (TR-1 to TR-8), Integration Readiness (IR-1 to IR-8) |
| `data/processed/step1_sub_competencies.csv` | 16 sub-competencies (8 TR + 8 IR) with descriptions and source mappings |
| `data/processed/step2_competency_statements.csv` | 42 competency statements derived from crosswalk |
| `data/processed/step2_crosswalk_matrix.csv` | Cross-taxonomy bridging table mapping ATLAS ↔ AIID ↔ EO 13960 via McKinsey constraints |
| `data/processed/step3_incident_coding.csv` | 52 ATLAS case studies coded by tactics, techniques, and competency gaps |
| `data/processed/step3_mitigation_gaps.csv` | Missing controls per incident |
| `data/processed/step3_tactic_frequency.csv` | Tactic frequency distribution across incidents |
| `data/processed/step4_propositions.csv` | 5 propositions with grounding sources, evidence, and falsifiability |
| `data/processed/step4_propositions.md` | Same propositions in detailed narrative form |
| `data/processed/unified_evidence_base.csv` | Stacked long-format dataset linking all three sources |

### Raw Data

| File | Records |
|------|---------|
| `data/raw/atlas/` | MITRE ATLAS YAML (52 case studies, 16 tactics, 155 techniques, 35 mitigations) |
| `data/raw/aiid/` | AI Incident Database MongoDB snapshot (1,362 incidents) |
| `data/raw/eo13960/` | EO 13960 Federal AI inventory CSV (1,757 use cases × 62 variables) |

### AstaLabs Experiment Archives

| Archive | Experiments | Key Analysis File |
|---------|:-----------:|-------------------|
| `data/astalabs_experiments_session1/` | 100 | `ANALYSIS_by_research_angle.md` — All 100 experiments mapped to Options A/B/C |
| `data/astalabs_experiments_session2/` | 300 | `ANALYSIS_option_A.md` — All 300 experiments organized into Threat → Gap → Safeguard pillars |

Each experiment folder (`EXP_NNN_node_X_Y/`) contains:
- `report.md` — Full analysis report with statistical findings
- `code.py` — Executable Python analysis code
- `experiment.json` — Metadata (hypothesis, surprise scores, outcome)

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/00_profile_sources.py` | Profile raw data sources (completeness, distributions) |
| `scripts/01_cross_taxonomy_mapping.py` | Build cross-taxonomy bridging table |
| `scripts/02_prepare_datasets.py` | Generate analysis-ready CSVs |
| `scripts/03_generate_figures.py` | Produce publication-ready figures |
| `scripts/04_profile_eo13960.py` | Deep profile of EO 13960 governance variables |
| `scripts/05_prepare_astalabs_discovery.py` | Consolidate data for AstaLabs AutoDiscovery |
| `scripts/06_fetch_astalabs_experiments.py` | Fetch experiments from AstaLabs API |
| `scripts/07_archive_astalabs_experiments.py` | Archive experiments into structured folders |

### Literature Library (34 sources)

Located in `literature/`. Key references indexed:
- #01: CIO Role in Digital Transformation (Springer 2023)
- #02: Strategic Directions for AI — CIOs and Boards (MISQ)
- #04: Responsible AI Governance Review (ScienceDirect)
- #07: Gartner CIO Agenda 2026
- #15: McKinsey Agentic AI Safety Playbook
- #20: BCG CIO's Role in AI Transformation
- #21: NIST AI RMF 1.0
- #22: NIST GenAI Profile
- #23: ISO/IEC 42001
- #25: ISACA COBIT for AI
- #26: EU AI Act
- #29: OWASP Top 10 LLM Applications
- #32: McKinsey New CIO Mandate 2026

---

## 3. What the Paper Draft Already Contains

The current draft (`paper/paper.md`, 261 lines) has:

### Complete Sections:
- **Abstract** (~250 words) — Full, publication-ready
- **Introduction** (~600 words) — Frames the governance gap problem, introduces three data sources, previews contributions
- **Theoretical Background** (~1,200 words) — CIO Role & AI Orientation, Dynamic Managerial Capabilities, Trust Readiness (with 4 sub-competencies), Integration Readiness (with 6 sub-competencies), Complementarity argument
- **Methodology** (~1,500 words) — Research design (convergent triangulation), data source descriptions (Table 1), cross-taxonomy mapping procedure, analysis-ready dataset preparation, figure generation, reproducibility

### TODO Sections:
- **Findings** — Empty. Needs to present the Threat → Gap → Safeguard evidence.
- **Propositions** — Has the original 5 propositions (P1–P5) but needs updating to reflect the 6 new data-grounded propositions from the AstaLabs analysis.
- **Discussion** — Empty.
- **Implications** — Empty.
- **Limitations** — Empty.
- **Conclusion** — Empty.
- **References** — Placeholder.

---

## 4. The Evidence: What 400 Experiments Tell Us

### Session 1 Meta-Findings (100 experiments)

- **82% of hypotheses contradicted** — mostly testing Trust vs Integration as distinct silos
- Attack complexity is increasing over time (r=0.38, p=0.006)
- Complex attacks expose broader competency gaps (r=0.83, p<0.001)
- Trust and Integration are **deeply intertwined** — not independent silos (strongest meta-finding)
- Framework source predicts competency domain: OWASP→Integration, NIST→Trust (Fisher p=0.018)

### Session 2 Meta-Findings (300 experiments)

- **67% contradicted**, **17% supported** (richer data → more confirmations)
- **28 Tier-1 citable experiments** organized into Threat → Gap → Safeguard

### The Six Propositions (Data-Grounded, from Session 2)

**P1. Risk-Tiering Failure** (9 convergent experiments)
Risk-based governance doesn't work in practice. High-impact and rights-impacting systems show no higher governance compliance than low-impact systems. EXP_146, 207, 230, 256 (all contradicted: high-impact ≠ more independent evaluation/impact assessment).

**P2. Commercial Opacity Barrier** (14 convergent experiments)
The single most robust finding. Vendor-supplied AI consistently shows lower code access, data documentation, appeal processes, and independent evaluation. EXP_106, 131, 174, 202, 210, 237, 245, 247, 257, 284, 291, 293, 299.

**P3. Sector-Specific Threat Fingerprints** (5 convergent experiments)
Finance → Economic harm, Healthcare → Physical harm, Government → Civil Rights harm. Confirmed by EXP_158, 170, 187, 242, 252. Biometrics → Civil Rights specifically (EXP_168, p<0.01). Fairness failures → Intangible harm (χ²=12.97, p=0.0003, EXP_173).

**P4. Threat-Reality Misalignment** (5 cross-source experiments)
ATLAS threat research targets different sectors than AIID real-world incidents, and neither matches EO 13960 governance investment patterns. EXP_108 (Risk-Investment Mismatch), EXP_164 (Threat-Reality Mismatch), EXP_156 (adversarial → intangible harm; accidental → physical harm).

**P5. Governance Bundle Effect** (7 convergent experiments)
When governance IS implemented, controls cluster: Assessment→Testing→Evaluation (V&V bundle); Assessment→Notice→Consultation (Accountability bundle). EXP_066, 167, 206, 224 (strongest: surprise +0.581), 261, 265.

**P6. Forced Participation Paradox** (4 convergent experiments)
Public-facing AI systems provide higher transparency (Notice, Appeal) but lower user agency (Opt-Out). Citizens can learn about government AI but cannot refuse it. EXP_085, 134, 160, 180.

### Additional Confirmed Findings

- GenAI incidents exploded post-2022 (EXP_177, 183) but Robotics/AV have higher severity per incident (EXP_271)
- EO 13960 had no measurable effect on bias mitigation (EXP_182, 241, 268)
- Autonomy does NOT predict harm type — 15 experiments all contradicted (sector and technology modality are the real predictors)
- Governance does NOT decay over lifecycle — it was never substantively there in the first place
- Agency type is NOT a strong predictor — near-zero deep governance is universal
- Adversarial attacks cause primarily intangible harm; accidental failures cause physical harm (EXP_156)
- Stakeholder consultation is completely absent across the entire EO 13960 dataset (EXP_184)
- Attack chain structure validated: Collection→Exfiltration sequential dependency (EXP_220)

---

## 5. The Challenge: 10-Page Coherent Story

### Page Budget (AMCIS format, ~1,000 words/page)

| Section | Target Pages | Target Words |
|---------|:-----------:|:------------:|
| Abstract | 0.25 | 250 |
| Introduction | 1.25 | 1,250 |
| Theoretical Background | 1.5 | 1,500 |
| Methodology | 1.5 | 1,500 |
| Findings | 2.5 | 2,500 |
| Discussion & Propositions | 1.5 | 1,500 |
| Implications & Conclusion | 1.0 | 1,000 |
| References | 0.5 | — |
| **Total** | **10** | **~9,500** |

### Key Decisions for the Draft

1. **How many propositions?** The original draft has 5 (P1–P5 from theoretical grounding). The experiments suggest 6 new data-grounded ones. We need to decide: revise the original 5 to incorporate the empirical findings, or replace with the new 6?

2. **Depth vs. Breadth:** We have 28 Tier-1 experiments. We cannot present all of them. The paper needs to select ~8–10 key findings and present them with enough statistical detail to be credible.

3. **The contradictions as a story:** 67–82% of hypotheses were contradicted. This IS the story — the gap between what frameworks prescribe and what organizations actually do. The paper should frame the contradictions as evidence of the governance gap, not as failed experiments.

4. **Figures:** We need 3–5 figures maximum. Recommended set (from ChatGPT synthesis):

   **Figure 1 — "The Governance Drop-off: Surface Compliance vs. Substantive Safeguards"** *(priority: HIGH)*
   - Type: Grouped bar chart (Tier 1 vs Tier 2 safeguards)
   - Data: EO 13960 counts/percentages (ATO 62.7%, internal review 60.7% vs impact assessment 8.9%, monitoring 8.5%, independent eval 6.8%, disparity mitigation 5.9%)
   - Supports: §4.1 — governance theater; the 62.7%→5.9% drop-off
   - Size: Half-page

   **Figure 2 — "Commercial Opacity as a Governance Barrier"** *(priority: HIGH)*
   - Type: Radar chart or two-panel bar chart (Vendor/COTS vs In-house)
   - Data: EO governance indicators most affected by procurement: code access, data documentation, appeal process, independent evaluation; annotate with EXP_245, EXP_291, EXP_131, EXP_299
   - Supports: §4.4 — novel, most robust finding; 14 convergent experiments
   - Size: Half-page

   **Figure 3 — "Sector–Harm Fingerprints in Real-World Incidents"** *(priority: MEDIUM)*
   - Type: Heatmap (sector × harm type)
   - Data: AIID sector classification crossed with harm categories; highlight finance/economic, healthcare/physical, government/civil-rights clusters; annotate EXP_158/170/173/252
   - Supports: §4.2 — sector specificity; debunks one-size governance
   - Size: Half-page (or quarter-page if simplified to top 5 sectors)

   **Figure 4 — "Threat–Reality–Practice Divergence"** *(priority: HIGH)*
   - Type: Sankey / alluvial flow diagram (three columns)
   - Data: ATLAS sector distribution → AIID incident sector distribution → EO 13960 deployment sectors; emphasize mismatch; annotate EXP_164 and EXP_108
   - Supports: §4.3 — triangulation contribution; threat–reality mismatch
   - Size: Half-page

   **Figure 5 — "Two-Speed Risk Landscape: GenAI Volume vs. Physical-World Severity"** *(priority: LOW — cuttable if page-tight)*
   - Type: Line chart (incident counts over time by modality) + small inset bar for severity by modality
   - Data: AIID incidents pre/post 2022 (GenAI vs robotics/AV) + severity comparison (EXP_271)
   - Supports: §4.2 — temporal explosion + severity divergence
   - Size: Quarter-page

   **If strict 3-figure limit:** Prioritize Figures 1, 2, and 4 — they jointly carry the core contribution and novelty.

5. **Propositions are now reconciled:** The original P1–P5 (theoretical) have been reconciled with the six Session 2 empirical patterns into P1–P6: (1) CIO centrality, (2) TR×IR complementarity mechanism, (3) governance theater / risk-tiering failure, (4) commercial opacity barrier, (5) sector-calibrated governance, (6) transparency-without-agency paradox. Each proposition includes evidence mapping and falsifiability criteria.

---

## 6. Recommended Paper Structure

### Revised Outline

1. **Introduction** (1.25 pages)
   - Hook: 92% deploying AI, 1% at scale
   - Problem: The governance gap (62.7% → 5.9%)
   - Three data sources + triangulation contribution
   - Preview of findings

2. **Theoretical Background** (1.5 pages)
   - Upper echelons → CIO centrality → AI orientation
   - Dynamic managerial capabilities → TR + IR
   - Conceptual model figure
   - Original 5 propositions (streamlined)

3. **Methodology** (1.5 pages)
   - Three data sources (Table 1)
   - Cross-taxonomy mapping approach
   - AstaLabs AutoDiscovery: 400 automated experiments (Bayesian surprise)
   - Convergent triangulation design

4. **Findings** (2.5 pages)
   - **4.1 Threat Characterization** (0.5 page): Sector-harm fingerprints, GenAI explosion, attack chain structure
   - **4.2 Governance Gap Identification** (1.0 page): Risk-tiering failure, commercial opacity, EO 13960 ineffectiveness, universal shallow governance
   - **4.3 Cross-Source Triangulation** (0.5 page): Threat-Reality Mismatch, Risk-Investment Mismatch
   - **4.4 Safeguard Patterns** (0.5 page): Governance bundles, Assessment-Action gap, Forced Participation Paradox

5. **Discussion** (1.5 pages)
   - How findings refine/extend the 5 propositions
   - The "governance theater" interpretation
   - Commercial procurement as structural barrier (new theoretical contribution)
   - Trust/Integration interdependence confirmed

6. **Implications and Conclusion** (1.0 pages)
   - For CIOs: bundle-based governance, vendor governance clauses, sector calibration
   - For researchers: replicable framework, open data, testable propositions
   - Limitations: federal-only, secondary data, U.S. context
   - Future work: primary data validation, international comparison

---

## 7. Combined Session 1 + Session 2 Stats

| Metric | Session 1 | Session 2 | Combined |
|--------|:---------:|:---------:|:--------:|
| Total experiments | 100 | 300 | 400 |
| Succeeded | 99 | 297 | 396 |
| Failed | 1 | 3 | 4 |
| Contradicted | 68 | 200 | 268 (67.7%) |
| Weakened | 14 | 19 | 33 (8.3%) |
| Neutral | 8 | 29 | 37 (9.3%) |
| Supported | 9 | 52 | 61 (15.4%) |
| Tier 1 (citable) | 7 | 28 | 35 |
