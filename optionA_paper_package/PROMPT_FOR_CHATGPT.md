# ChatGPT Prompt — AMCIS 2026 Option A Paper Draft

> **Instructions:** Copy everything below the line into a new ChatGPT conversation (GPT-4o or o3 recommended). Then upload the following files when prompted:
>
> **Required uploads (in order of priority):**
> 1. `optionA_paper_package/README_PACKAGE.md` — this handoff document (the prompt references it)
> 2. `paper/paper.md` — current paper draft (has Abstract through Methodology complete)
> 3. `data/astalabs_experiments_session2/ANALYSIS_option_A.md` — Session 2 analysis (Threat → Gap → Safeguard)
> 4. `data/astalabs_experiments_session1/ANALYSIS_by_research_angle.md` — Session 1 analysis
> 5. `data/processed/step4_propositions.md` — Original 5 propositions with full grounding
> 6. `data/processed/step1_construct_definitions.md` — Construct definitions (AI Orientation, TR, IR)
> 7. `docs/research_angles_summary.md` — Research angles + updated analysis plan
>
> **Optional uploads (if ChatGPT context window allows):**
> 8. `data/processed/step1_sub_competencies.csv` — 16 sub-competencies (TR-1 to TR-8, IR-1 to IR-8)
> 9. `data/processed/step2_crosswalk_matrix.csv` — Cross-taxonomy bridging table
> 10. `data/processed/step3_incident_coding.csv` — 52 ATLAS cases coded
> 11. `docs/Goal.txt` — Original project blueprint

---

## PROMPT

You are an expert IS (Information Systems) researcher helping draft a 10-page conference paper for AMCIS 2026. I am uploading a comprehensive package of files. Please read them all carefully before responding.

### Context

We are writing a paper titled **"Strategic AI Orientation Enabled by Trust & Integration Readiness: A Secondary-Data Analysis of Governance Gaps in AI Deployment"** for AMCIS 2026 (Americas Conference on Information Systems).

**Research question (Option A — confirmed):** *How do adversarial AI threats and real-world AI failures expose governance readiness gaps in organizational AI deployment?*

**Theoretical lens:** Upper echelons theory + dynamic managerial capabilities → CIO-driven AI orientation → enabled by Trust Readiness (governance capability bundle) and Integration Readiness (architecture capability bundle) as strategic complements.

**Three data sources (all public):**
1. MITRE ATLAS — 52 adversarial case studies, 16 tactics, 155 techniques, 35 mitigations
2. AI Incident Database (AIID) — 1,362 real-world AI incidents
3. EO 13960 Federal AI Use Case Inventory — 1,757 federal AI use cases × 62 governance variables

**Automated experiment engine:** We used AstaLabs AutoDiscovery (Bayesian surprise-based data exploration) to run 400 automated experiments across our consolidated datasets:
- Session 1 (100 experiments) — used processed datasets only (competency statements, crosswalk, incident coding)
- Session 2 (300 experiments) — used full raw data from all three sources

**Key findings from 400 experiments:**
- 67.7% of hypotheses were **contradicted** — this IS the story (governance frameworks prescribe things organizations don't do)
- 15.4% were **supported** — these provide the positive empirical grounding
- The paper draft (paper.md) has Abstract through Methodology **complete**. Findings through Conclusion are **TODO**.

### What I Need

Please help me complete the paper by doing the following **in sequence**:

#### Step 1: Read and Synthesize
Read all uploaded files. Then provide a brief synthesis (1 paragraph) confirming you understand:
- The theoretical model (AI Orientation → TR × IR → Value)
- The three data sources and cross-taxonomy mapping approach
- The 6 empirical propositions from AstaLabs experiments (P1–P6)
- The 5 original theoretical propositions (P1–P5 from step4_propositions.md)
- What sections of paper.md are complete vs. TODO

#### Step 2: Propose a Reconciled Proposition Set
The original paper has 5 theoretical propositions (P1–P5). The experiments generated 6 empirical findings. Propose a **reconciled set of propositions** (ideally 5–6) that:
- Keep the theoretical grounding of the originals (CIO centrality, TR, IR, complementarity, regulatory pressure)
- Incorporate the strongest empirical evidence from the experiments (risk-tiering failure, commercial opacity, sector fingerprints, threat-reality mismatch, governance bundles)
- Are testable, falsifiable, and suitable for an AMCIS research-in-progress or completed research paper
- Map each proposition to specific experiments as evidence

#### Step 3: Draft the Findings Section (~2,500 words)
Write the **Findings** section for `paper.md`, organized as:
1. **4.1 The Governance Gap: Surface Compliance vs. Substantive Safeguards** — Present the 62.7% → 5.9% drop-off with supporting experiment evidence
2. **4.2 Threat Landscape: Sector-Specific Harm Fingerprints** — Present sector-harm associations, GenAI temporal explosion, autonomy findings
3. **4.3 Cross-Source Triangulation: Where Threats, Incidents, and Governance Diverge** — Present the Threat-Reality Mismatch and Risk-Investment Mismatch findings
4. **4.4 Structural Barriers: Commercial Opacity and Procurement Governance** — Present the commercial opacity findings (14 convergent experiments)
5. **4.5 Governance Architecture: Bundling Effects and the Assessment-Action Gap** — Present control co-occurrence patterns and the Forced Participation Paradox

For each subsection:
- Lead with the finding statement
- Cite specific experiments (e.g., "EXP_146, n=1,718, p<0.0001")
- Include key statistics (chi-square values, proportions, surprise scores)
- Keep the tone academic but accessible — AMCIS audience is IS researchers and practitioners
- Use tables where appropriate to present convergent evidence

#### Step 4: Draft the Discussion Section (~1,500 words)
Write the **Discussion** section that:
1. Interprets the findings through the theoretical lens (how do they support/refine the propositions?)
2. Explains the "governance theater" phenomenon (compliance checkboxes without substance)
3. Positions commercial procurement as a novel theoretical contribution (structural barrier to governance capability)
4. Connects to the Trust/Integration interdependence finding from Session 1
5. Addresses the "contradictions as evidence" framing — why 68% contradicted hypotheses strengthens rather than weakens the paper

#### Step 5: Draft Implications, Limitations, and Conclusion (~1,000 words)
- **Research implications:** Replicable framework, open data, proposition testing opportunities
- **Practice implications:** Bundle-based governance, vendor governance clauses, sector-calibrated frameworks, CIO capability development
- **Limitations:** Federal-only sample, U.S. context, secondary data, text-mining approximations, AstaLabs as exploratory (not confirmatory)
- **Conclusion:** 3–4 sentence summary emphasizing the governance gap contribution

#### Step 6: Suggest 3–5 Figures
Recommend specific figures (with layout descriptions) that would maximize the paper's visual impact within the 10-page constraint. For each, specify:
- Title
- Type (bar chart, radar, Sankey, heatmap, etc.)
- Data to include
- Which finding it supports
- Approximate size (quarter-page, half-page, full-page)

### Formatting Requirements
- AMCIS 2026 uses APA 7th edition referencing
- 10-page limit including references but excluding appendices
- Use the academic IS tone already established in the existing draft
- Tables and figures count toward the page limit
- Reference the literature files by their index number (e.g., [#20] for BCG CIO Role) — I will format proper citations later

### Important Notes
- The existing Abstract, Introduction, Theoretical Background, and Methodology in `paper.md` are **final** — do not rewrite them. Write only the TODO sections.
- The AstaLabs experiments are **exploratory not confirmatory** — frame findings accordingly (e.g., "our exploratory analysis reveals..." not "we prove...")
- The 400 experiments are the empirical backbone but the paper should cite specific experiments sparingly — summarize convergent evidence patterns rather than listing every experiment number
- Prioritize the **Commercial Opacity** finding — it is the most novel and most robustly supported
- The **contradictions as evidence** framing is essential: the mass contradictions (68% of hypotheses falsified) collectively demonstrate that governance frameworks describe an ideal world that doesn't exist in practice

---

*End of prompt. Upload the files listed above and paste this entire prompt into the conversation.*
