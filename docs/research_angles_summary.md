# AMCIS 2026 — Research Angle Options

**Date:** February 21, 2026  
**Purpose:** Summarize three candidate research angles using our secondary data sources for co-author review.

---

## Secondary Data Sources

We have acquired three **publicly available, structured secondary data sources** to ground the paper empirically:

| # | Source | What it contains | Scale |
|---|--------|-----------------|-------|
| 1 | **MITRE ATLAS** | Adversarial threat matrix for AI systems — tactics, techniques, mitigations, and case studies of attacks on AI/ML | 16 tactics, 155 techniques, 35 mitigations, 52 case studies |
| 2 | **AI Incident Database (AIID)** | Catalogue of real-world AI harms and failures (bias, safety, privacy, misinformation, etc.) with structured taxonomies | 1,362 incidents, 6,681 media reports, 214+ classifications |
| 3 | **EO 13960 Federal AI Use Case Inventory** | U.S. federal government inventory of all agency AI deployments with 62 governance & integration variables | 1,757 use cases across 38 agencies |

### Source URLs

- **MITRE ATLAS:** https://atlas.mitre.org/ (GitHub data: https://github.com/mitre-atlas/atlas-data)
- **AI Incident Database (AIID):** https://incidentdatabase.ai/ (snapshots: https://incidentdatabase.ai/research/snapshots/)
- **EO 13960 Federal AI Use Case Inventory:** https://www.cio.gov/policies-and-priorities/Executive-Order-13960-AI-Use-Case-Inventories-Reference (GitHub data: https://github.com/ombegov/2024-Federal-AI-Use-Case-Inventory)

---

## Key Data Insight — The Governance Gap (verified)

The EO 13960 dataset (1,757 use cases × 62 variables × 38 agencies) reveals a **striking governance gap** between surface-level compliance and substantive AI risk management.

### Tier 1 — Basic Controls (~61% completion)

| Safeguard | Count | % of 1,757 |
|-----------|------:|-----------:|
| Authorization to Operate (ATO) | 1,102 | **62.7%** |
| Internal review / approval | 1,067 | **60.7%** |

### Tier 2 — Deep Governance Safeguards (~6–9% completion)

| Safeguard | Count | % of 1,757 |
|-----------|------:|-----------:|
| Impact assessment | 157 | 8.9% |
| Post-deployment monitoring | 149 | 8.5% |
| Adverse impact assessment | 152 | 8.7% |
| Real-world testing | 149 | 8.5% |
| Autonomous decision impact | 152 | 8.7% |
| Stakeholder consultation | 145 | 8.3% |
| Opt-out mechanism | 144 | 8.2% |
| Appeal process | 143 | 8.1% |
| AI use notice to public | 140 | 8.0% |
| Independent evaluation | 119 | 6.8% |
| Key risk identification | 115 | 6.5% |
| **Disparity / bias mitigation** | **104** | **5.9%** |

### Even among mandatory cases (227 rights/safety-impacting use cases), only 16–23% report safeguards

| Safeguard | Count | % of 227 |
|-----------|------:|---------:|
| Impact assessment | 51 | 22.5% |
| Key risk identification | 49 | 21.6% |
| Post-deployment monitoring | 44 | 19.4% |
| Real-world testing | 44 | 19.4% |
| Independent evaluation | 41 | 18.1% |
| Disparity / bias mitigation | 37 | **16.3%** |

**Interpretation:** Organizations check the basic compliance boxes (ATO, internal review) but largely skip the deeper governance work that frameworks like NIST AI RMF, EU AI Act, and MITRE ATLAS require. Bias mitigation is the weakest safeguard at both levels. The 125 compliance extension requests confirm this is a practice gap, not just a reporting gap.

---

## Three Research Angle Options

### Angle A: Threat → Gap → Safeguard (Recommended)

**Research question:** *How do adversarial AI threats and real-world AI failures expose governance readiness gaps in organizational AI deployment?*

**Method:**
1. Map **ATLAS tactics/mitigations** to categories of AI risk (adversarial/security threats)
2. Map **AIID incidents** to categories of AI harm (broader: bias, safety, privacy, misinformation)
3. Compare both against **EO 13960 governance safeguard variables** to identify where practice lags threat reality
4. Derive CIO competency gaps from the mismatches

**Strengths:**
- Triangulates across threat data (what *can* go wrong), incident data (what *has* gone wrong), and practice data (what orgs *are doing*)
- The 62.7% → 5.9–8.9% governance drop-off is a verified, data-grounded finding
- Even among mandatory rights/safety use cases, only 16–23% report deep safeguards
- Novel — no prior work connects all three sources

**Risks:**
- Requires careful cross-taxonomy mapping between ATLAS, AIID, and EO 13960 categories
- Coding effort is non-trivial

**Feasibility:** Medium | **Novelty:** High

---

### Angle B: Integration Maturity Clustering

**Research question:** *What patterns of AI governance and integration readiness exist across federal agencies, and how do maturity gaps relate to AI harm types?*

**Method:**
1. Use the 62-variable **EO 13960** dataset to build agency-level readiness profiles
2. Cluster agencies by governance + architecture maturity patterns (e.g., dev stage, infrastructure, PII handling, review completeness)
3. Cross-reference clusters with **AIID** sector-level incident data to show which maturity gaps correspond to higher harm incidence

**Strengths:**
- Highly quantitative — clustering, descriptive stats, possible regression
- EO 13960 is a rich structured dataset (1,757 × 62)
- Clear, methodologically clean approach

**Risks:**
- Federal-only scope limits generalizability to private sector (a limitation to acknowledge)
- AIID → EO sector matching is approximate (government vs. industry sectors)

**Feasibility:** High | **Novelty:** Medium

---

### Angle C: Combined CIO Competency Framework

**Research question:** *What competency bundles — spanning trust/governance and integration/architecture — must CIOs develop to enable strategic AI orientation?*

**Method:**
1. ATLAS + AIID → Map the full threat/incident landscape
2. EO 13960 → Map governance & integration practices actually in use
3. Gap analysis → Identify where practice doesn't match threat/incident reality
4. Synthesize gaps into CIO competency dimensions, grounded in literature

**Strengths:**
- Full realization of the thesis (trust readiness + integration readiness → AI orientation)
- Highest potential contribution

**Risks:**
- Likely too broad for a single AMCIS paper (10-page limit)
- Could be shallow across many dimensions rather than deep in any one

**Feasibility:** Low (for one paper) | **Novelty:** Very High

---

## Recommendation

**Angle A** offers the best balance for AMCIS 2026:
- The governance completeness gap (62% → 7%) is a compelling, data-grounded finding
- Triangulating three distinct public data sources is methodologically novel
- The scope is bounded enough for a 10-page conference paper
- Angle C can be positioned as the broader research agenda, with this paper contributing one empirically grounded piece

---

## Decision: Option A Confirmed (Feb 22, 2026)

Co-author agreed with the recommendation. **Option A (Threat → Gap → Safeguard)** is the chosen research angle.

---

## Analysis Plan — Option A: Threat → Gap → Safeguard

**Status:** AstaLabs AutoDiscovery experiments completed (Session 1: 100 experiments, Session 2: 300 experiments). Full analysis documents available:
- Session 1 analysis: `data/astalabs_experiments_session1/ANALYSIS_by_research_angle.md`
- Session 2 Option A analysis: `data/astalabs_experiments_session2/ANALYSIS_option_A.md`

### Evidence Inventory (400 experiments total)

| Source | Tier 1 (Citable) | Tier 2 (Directional) | Tier 3 (Informative Contradictions) | Total |
|--------|:-:|:-:|:-:|:-:|
| Session 1 | 7 | 10 | 15 | 100 |
| Session 2 | 28 | 35 | 50+ | 300 |
| **Combined** | **35** | **45** | **65+** | **400** |

### Six Propositions for the Paper

| # | Proposition | Evidence Base | Convergent Experiments |
|---|------------|---------------|:---------------------:|
| P1 | Risk-tiering fails in practice | EXP_146, 207, 230, 256, 282, 290 (S2) | 9 |
| P2 | Commercial procurement = primary governance barrier | EXP_106, 131, 174, 202, 210, 237, 245, 247, etc. (S2) | 14 |
| P3 | Sector-specific threat fingerprints | EXP_158, 168, 170, 187, 242, 252 (S2) | 5 |
| P4 | Threat-Reality Misalignment (ATLAS ≠ AIID ≠ EO 13960) | EXP_108, 156, 164 (S2); EXP_017/041 (S1) | 5 |
| P5 | Governance controls bundle in coherent clusters | EXP_066, 167, 206, 224, 261, 265 (S2) | 7 |
| P6 | Forced Participation Paradox | EXP_085, 134, 160, 180 (S2) | 4 |

### Next Steps

1. ~~Decide which angle to pursue~~ ✅ Option A confirmed
2. ~~Run AstaLabs AutoDiscovery experiments~~ ✅ 400 experiments complete
3. ~~Analyze experiments for chosen angle~~ ✅ Analysis documents complete
4. **Generate publication-quality figures:**
   - Governance gap histogram (62.7% ATO → 5.9% Disparity Mitigation)
   - Commercial vs In-House governance radar chart
   - Sector-harm heatmap (AIID)
   - Temporal GenAI explosion line chart
   - Threat-Reality Mismatch Sankey diagram
5. **Draft paper outline** aligned with P1–P6 propositions
6. **Write the paper** (10-page AMCIS format)
7. **Literature integration** — connect findings to vendor lock-in, AI ethics, regulatory design literatures
