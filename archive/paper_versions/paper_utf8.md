---
bibliography: references.bib
csl: apa.csl
link-citations: true
reference-doc: reference.docx
---

# Governance Readiness Gaps in Organizational AI Deployment: A Triangulated Analysis of Threats, Incidents, and Practice

*Full Paper*

<!-- AMCIS PCS fields, abstract, keywords, and authors entered in the submission system, not in this file.

**Abstract.** Artificial intelligence has shifted from boardroom aspiration to organizational imperative, yet governance readiness lags far behind deployment pace. Drawing on dynamic capabilities and institutional decoupling, we investigate how *trust readiness* (governance capability) and *integration readiness* (implementation capability) shape the link between organizational AI portfolio scope and operational deployment. Triangulating MITRE ATLAS, the AI Incident Database, and the U.S. EO 13960 Federal AI Use Case Inventory (1,757 deployments), our analysis reveals governance theater. A majority of federal AI deployments report internal review approval, yet only a small fraction report substantive safeguards such as impact assessments, bias mitigation, or independent evaluation. Risk-tiering does not rescue governance depth. Splitting trust readiness into surface compliance and substantive safeguards uncovers a suppression effect: surface approvals facilitate deployment while substantive safeguards dampen it, a divergence masked when both are aggregated into a single trust readiness score. Integration readiness remains the dominant predictor of operational deployment. Among vendor-developed systems, evaluability constraints, specifically limits on control rights and system access, emerge as a structural antecedent of governance failure.

**Keywords:** AI governance, governance theater, trust readiness, integration readiness, AI evaluation, AI deployment
-->

---

## Introduction

Artificial intelligence has shifted from boardroom aspiration to organizational imperative. McKinsey's latest global survey reports that 88% of organizations now use AI in at least one business function, yet the majority remain in piloting stages and only about one-third have begun scaling [@mckinseyai2025]. Over 50% of firms cite legacy IT architectures as the primary barrier [@bcg2025]. The gap between AI ambition and AI realization is widening, not narrowing.

We investigate this gap through a governance lens. Using the U.S. Federal AI Use Case Inventory (1,757 deployments across 38 agencies), we find that while a majority of AI systems report internal review approval, only a small fraction report substantive safeguards such as impact assessments, bias mitigation, or independent evaluation. This steep "surface-to-substance" drop-off is not merely organizational immaturity; it constitutes *governance theater*, a form of institutional decoupling [@meyer1977] in which organizations adopt formal governance structures while the operational routines needed to enact them remain absent.

Documenting governance theater raises a harder question: *why does it persist?* Despite proliferating governance frameworks, from NIST AI Risk Management Framework (RMF) [@nist2023] to the EU AI Act [@euaiact2024] and beyond, substantive safeguards remain rare even under federal mandate. Recent IS syntheses of responsible AI governance propose integrative frameworks yet emphasize that empirical work connecting governance designs to enacted routines and outcomes remains underdeveloped [@papagiannidis2025]. We argue that the explanation lies not in awareness deficits but in *capability constraints*. Governance demands architectural hooks to be enforceable, and commercial procurement introduces evaluability constraints, specifically limits on control rights and system access, that block organizations from executing those hooks. Vendors are pervasive in AI deployment because AI systems require specialized technical expertise that most organizations do not build in-house; this structural dependence means that governance constraints originating in procurement are not incidental but endemic [@bcg2025]. If governance theater persists even where mandates and classification requirements both exist, the constraint must lie deeper than regulatory design.

We frame this argument through the lens of dynamic capabilities [@teece2007], building on recent work positioning AI governance as an organizational capability [@papagiannidis2025]. We posit that AI deployment and scalability require two capability bundles: *trust readiness* (TR), governance capabilities spanning risk management, compliance, and accountability, and *integration readiness* (IR), the organizational and technical capacity to integrate, operate, and scale AI in production. We theorize these bundles as potential strategic complements [@milgrom1990]—a relationship also conditioned by institutional pressures toward decoupling [@meyer1977]—yet our evidence reveals a more fundamental problem: commercial procurement constrains the control rights needed to execute substantive safeguards even when policies demand them [@bcg2025].

To ground this argument, we triangulate three publicly available secondary data sources not previously connected in IS research. MITRE ATLAS provides 52 adversarial case studies (what *can* go wrong). The AI Incident Database contributes 1,362 incidents (what *has* gone wrong). The EO 13960 Federal AI Use Case Inventory supplies 1,757 deployments (what organizations *are actually doing*). Through this triangulated analysis, we demonstrate that risk-tiered AI governance frequently functions as governance theater and identify evaluability constraints as binding barriers. We also provide a replicable analytical framework that other researchers can extend with public data.

---

## Theoretical Background

Dynamic capabilities theory posits that organizations sustain competitive advantage by sensing emerging opportunities and threats, seizing them through investment and design, and reconfiguring routines as environments shift [@teece2007]. In AI contexts, sensing means recognizing governance requirements, evaluating vendor risk, and tracking regulatory change. Seizing requires building the governance and integration routines that convert strategic intent into deployed systems. Reconfiguring entails updating those routines as threat landscapes, regulations, and portfolios evolve. The Chief Information Officer (CIO) role has evolved from technology steward to strategic partner in this process [@chawla2023], and practitioner surveys confirm that strategy, speed, and risk mastery now define the CIO agenda [@mckinsey2026; @bcg2025; @gartner2026], and IS research confirms that CIO and board strategic directions for AI are critical enablers of deployment at scale [@li2021]. We take organizational AI portfolio scope as a contextual starting point, operationalized via an agency-level proxy; our propositions focus on the downstream capability mechanisms, trust readiness and integration readiness, that convert portfolio scope into operational deployment. Figure 1 depicts the theoretical framework.

![Figure 1. Theoretical Framework: Organizational AI Portfolio Scope, Trust Readiness, Integration Readiness, and Evaluability Constraints](figures/fig0_framework.png)

We operationalize this framework through two capability bundles. **Trust readiness** (TR) encompasses risk management, compliance, adversarial threat modeling, incident response, and stakeholder accountability, grounded in normative frameworks including NIST AI RMF [@nist2023], the EU AI Act [@euaiact2024], and the MITRE ATLAS adversarial threat taxonomy. TR spans a continuum from *surface compliance* (TR-surface, 0–2: internal review boards and authorization to operate) to *substantive safeguards* (TR-substantive, 0–7: impact assessment, independent evaluation, real-world testing, post-deployment monitoring, AI notice, bias mitigation, and appeal processes). Substantive safeguards demand deep technical access, cross-functional coordination, and sustained investment. We define *governance theater* as the condition where TR-surface > 0 but TR-substantive = 0: organizations exhibit formal authorization artifacts without the operational safeguards needed to make authorization meaningful. Our composite TR index (0–9) aggregates both tiers, but our analysis also estimates them separately, revealing a suppression effect masked by the composite. The distribution of federal AI systems across this continuum serves as the paper's core empirical anchor.

**Integration readiness** (IR) covers the architecture needed for AI in production: data pipeline governance, evaluation infrastructure, deployment controls, and code/model access. Concretely, IR captures the capacity to integrate, operate, and scale AI systems: data catalogs, documentation, provisioned infrastructure, source-code access, and component reuse. Critically, IR supplies the *enforcement hooks* that make governance actionable: without telemetry infrastructure, audit logging is impossible; without evaluation pipelines, bias testing cannot be conducted; without code access, independent review is foreclosed. We term this boundary condition *governance implementability*: the degree to which an organization has the control rights and technical access needed to carry out governance routines. Implementability depends on access to model artifacts, telemetry, and evaluation interfaces; when procurement or outsourcing restricts these rights, it collapses and decoupling persists even under mandate. @bcg2025 find that over 50% of firms identify legacy IT architecture as the primary barrier to AI scaling, underscoring IR's strategic importance as a dynamic capability rather than a fixed asset.

Institutional theory shows that organizations routinely adopt formal structures to signal conformity while decoupling those structures from day-to-day operations [@meyer1977; @bromley2012]. @ali2023 document how this dynamic extends to AI ethics, where organizational structures create barriers between stated commitments and operational practice. We adopt the term *governance theater* to describe this pattern in AI governance: the systematic adoption of authorization artifacts without the operational safeguards needed to make authorization meaningful. Our empirical analysis tests whether a large-scale federal AI inventory exhibits governance theater and identifies the structural mechanisms that sustain it.

We theorize that trust readiness and integration readiness are potential strategic complements [@milgrom1990]: governance controls require architectural hooks to be *enforceable* (bias testing needs evaluation pipelines; independent review needs code access), and architectural patterns require governance boundaries to be *safe*. However, we predict that this complementarity is *conditional on governance maturity*: when TR remains theatrical, meaning surface compliance without operational substance, it cannot interact productively with IR. We therefore expect integration readiness to be the binding constraint in current deployments, with complementarity emerging only as substantive governance deepens beyond current levels.

---

## Methodology

We follow a convergent triangulation design [@creswell2018] using three publicly available data sources. Table 1 summarizes each source.

**Table 1.** Data sources

| Source | Records | Coverage | Licence |
|--------|--------:|----------|---------|
| MITRE ATLAS v4.x | 52 case studies; 16 tactics; 155 techniques; 35 mitigations | Adversarial AI threats | Apache 2.0 |
| AI Incident Database (AIID) | 1,362 incidents; 6,681 reports | Real-world AI harms (CSET: 201 classified; GMF: 278 classified) | CC BY-SA 4.0 |
| EO 13960 Federal AI Use Case Inventory | 1,757 use cases; 38 agencies; 62 variables | Governance and integration practice | Public domain |

We use ATLAS for adversarial threat coverage, AIID for realized harms, and EO 13960 for reported governance and integration practice across 62 variables per use case. AIID includes two structured taxonomies: CSET (Center for Security and Emerging Technology) for harm types and sectors, and GMF (Goals, Methods, and Failures) for technical failure modes.

**Cross-taxonomy mapping.** Because the three data sources use distinct classification schemes, we construct a bridging table that maps elements from each source to a common set of organizing constructs, anchored to CIO-reported constraints to AI scaling [@mckinsey2026]. The mapping links 126 elements across all three sources via rule-based assignments with explicit rationale. Monte Carlo sensitivity analysis (1,000 iterations at 10-20% perturbation) confirms mapping stability (mean $\rho$=0.95) [@creswell2018]. Importantly, the paper's core findings, namely governance drop-off, IR dominance, and evaluability constraints, are computed directly from EO 13960 variables and are not mediated by the cross-taxonomy map.

**Pathway model.** To provide a preliminary test of the theorized Orientation → TR $\times$ IR → Deployment pathway, we estimate nested logistic regressions at the use-case level (n=1,757) predicting operational deployment status. Trust readiness (TR, 0-9) counts nine governance safeguard indicators: ATO, internal review, impact assessment, real-world testing, independent evaluation, post-deployment monitoring, AI notice, disparity mitigation, and appeal process. Integration readiness (IR, 0-7) counts seven architecture indicators: data catalog, documentation, custom code, source-code access, provisioned infrastructure, timely resources, and code/data reuse. Orientation—the agency-level AI portfolio scope proxy (z-scored log portfolio size + topic breadth)—captures the scale and diversity of an agency's AI investments as an indicator of sensing activity, not executive strategic intent. Controls include development method and rights/safety classification. We estimate four nested models: (M1) controls only; (M2) + orientation; (M3) + composite TR + IR; (M4) TR split into surface (0–2) and substantive (0–7) components.

**Exploratory analysis.** We employ a Bayesian-surprise-based exploratory analysis engine that programmatically generates and tests hypotheses from the data schema. Across 400 experiments (Session 1: 100; Session 2: 300), 67.7% of hypotheses were contradicted, a result we treat as substantive evidence of governance gaps rather than methodological failure. The engine serves as a hypothesis-generation tool. Findings reported in the paper rest on convergent multi-experiment evidence and are confirmed through standard statistical tests (logistic regression, chi-square). All analysis code and data are available in the companion repository.

---

## Findings

Our findings are exploratory. The Bayesian-surprise engine generated candidate patterns; all quantitative results reported below are confirmed through standard statistical tests.

### Governance Theater: Depth Collapse and Tiering Failure

Federal AI deployments exhibit high surface compliance but strikingly low substantive safeguards. Across 1,757 EO 13960 use cases, internal review is reported by 60.7% and Authorization to Operate (ATO) by 37.2%, yet substantive safeguards, including impact assessment, independent evaluation, bias mitigation, and the like, cluster in the 5-9% range. This ~55 percentage-point gap between internal review and the substantive safeguard floor shows that review processes exist but the operational governance work that frameworks prescribe remains rare.

![Figure 2. The Governance Drop-off: Surface Compliance vs. Substantive Safeguards (EO 13960)](figures/fig1_governance_dropoff.png)

This gap persists precisely where governance should intensify. Among the 227 use cases flagged as rights- or safety-impacting, deep safeguards rise but remain limited: impact assessment reaches 22.5%, independent evaluation 18.1%, and bias mitigation 16.3%. Even in this mandatory subset, the gap is attenuated rather than eliminated.

Risk-tiering, the foundational design principle of contemporary AI governance, fails to rescue governance depth. Governance theater (TR-surface > 0, TR-substantive = 0) characterizes 53.9% of non-flagged systems and 63.0% of rights- or safety-impacting systems, indicating that risk classification *worsens* rather than rescues the surface-substance gap. High-impact systems are no more likely to report independent evaluation (EXP_146, n=1,718, p<0.0001; contradicted), nor are rights-impacting systems more likely to report impact assessment (EXP_207, n=1,757; contradicted). Multiple experiments replicate this null—meaning that across different subsets and specifications, high-impact classification consistently fails to predict deeper safeguard adoption. In institutional-theory terms, this constitutes policy-practice decoupling [@meyer1977; @bromley2012]: adopted classification policies do not translate into differentiated operational practice.

A preliminary pathway test reinforces this interpretation. Table 2 reports nested logistic regressions predicting operational deployment (52.4% of use cases). In M3, the composite trust readiness index shows no independent effect (p≈0.10), while integration readiness dominates (OR [odds ratio]=1.37, p<0.001). M4 splits TR into surface (0–2) and substantive (0–7) components, revealing a suppression effect: TR-surface facilitates deployment (OR=1.39, p<0.01) as procedural authorizations remove administrative barriers, while TR-substantive dampens it (OR=0.92, p<0.05) as genuine scrutiny introduces friction. This divergence is the quantitative signature of governance theater. Integration readiness remains the dominant predictor (OR=1.25, p<0.001), and model fit improves (AIC: 2,089.4 → 2,080.4). Notably, vendor procurement is positively associated with operational deployment in these models (OR=0.71–1.11 across M1–M4), which may appear to contradict H4. This reflects a composition effect: vendor-procured systems are more likely to be operationally deployed (vendors deliver working systems quickly) while simultaneously showing weaker substantive safeguards---consistent with H4---because deployment and governance depth are decoupled outcomes.

**Table 2.** Nested logistic regression: DV = Operational deployment (0/1)

| Variable | M1 | M2 | M3 | M4 |
|:---------|:--:|:--:|:--:|:--:|
| Constant | -0.357\*\*\* (0.063) | -0.387\*\*\* (0.064) | -1.200\*\*\* (0.093) | -1.231\*\*\* (0.094) |
| Vendor | 1.109\*\*\* (0.119) | 1.171\*\*\* (0.121) | 0.813\*\*\* (0.130) | 0.708\*\*\* (0.134) |
| Mixed dev. | 0.955\*\*\* (0.166) | 0.960\*\*\* (0.167) | 0.436\* (0.178) | 0.326+ (0.182) |
| Rights/safety | 0.487\*\* (0.158) | 0.588\*\*\* (0.161) | 0.928\*\*\* (0.175) | 0.897\*\*\* (0.175) |
| Orientation | | -0.195\*\*\* (0.059) | -0.273\*\*\* (0.065) | -0.271\*\*\* (0.066) |
| TR (composite) | | | -0.054 (0.033) | |
| TR-surface (0–2) | | | | 0.332\*\* (0.121) |
| TR-substantive (0–7) | | | | -0.083\* (0.034) |
| IR | | | 0.316\*\*\* (0.025) | 0.224\*\*\* (0.037) |
| *N* | 1,757 | 1,757 | 1,757 | 1,757 |
| Pseudo R² | 0.055 | 0.059 | 0.147 | 0.151 |
| AIC | 2,306.7 | 2,297.6 | 2,089.4 | 2,080.4 |

+p<0.10; \*p<0.05; \*\*p<0.01; \*\*\*p<0.001. Standard errors in parentheses.

### Binding Constraints: Evaluability Constraints and Architectural Enforceability

Commercial procurement is a consistently supported predictor of governance under-implementation, operating as an evaluability constraint that restricts the control rights needed to translate governance commitments into implementable safeguards.

Restricting to use cases with identified development method (n=1,107; vendor: 481, in-house: 439, mixed: 187) and excluding 650 records with unspecified development method and near-zero governance reporting, vendor-developed systems report weaker substantive governance. The deficit is most pronounced for safeguards requiring deep system access: impact assessment in vendor systems (6.4%) trails in-house systems (10.3%).

![Figure 3. Evaluability Constraints as a Governance Barrier: Vendor-Supplied vs. In-House AI Systems (EO 13960)](figures/fig2_commercial_opacity.png)

Multivariate logistic regressions (n=1,107) control for impact classification, public-facing status, and operational stage. Impact assessment, the safeguard requiring the deepest vendor cooperation, shows a robust deficit: vendor-developed systems are roughly half as likely to report it (OR=0.43, 95% CI [0.25, 0.72], p=0.002). The effect is robust to the addition of agency fixed effects (OR=0.47, p=0.046). Notably, the bivariate vendor direction reverses when the 650 records with unspecified development method are included, because these effectively blank submissions inflate the non-vendor reference group, a sample composition artifact rather than a true positive vendor effect. By contrast, independent evaluation, performable by external parties, shows no vendor effect ($\text{OR} \approx 1.0$), confirming that the barrier is specific to activities requiring internal system access. Transparency deficits cascade into accountability: code access strongly predicts appeal processes (OR=7.52, p<0.001) and independent evaluation (OR=19.48, p<0.001).

Integration readiness provides the architectural context for these patterns. The IR index (mean=3.15, median=3) substantially outpaces the TR index (mean=1.49, median=1), and operational deployment rates differ sharply by IR level: 33% for low-IR (0-2), 57% for mid-IR (3-4), and 73% for high-IR (5-7). Where governance *is* present, it appears as coherent capability bundles rather than isolated controls. Impact assessment predicts real-world testing (surprise +0.581), and high-IR systems are nine times more likely to exhibit bundled deep safeguards (14.9% vs. 1.6%, $\chi^2$=87.3, p<0.001; Spearman $\rho$=0.228, p<0.001). Yet assessments do not reliably trigger mitigation, a means-ends decoupling [@bromley2012] where documentation artifacts function independently of operational action, consistent with the governance theater pattern.

### Contextual Calibration: Sector-Specific Harm Fingerprints

AI Incident Database (AIID) incident analysis reveals that AI harms are sector-structured rather than autonomy-driven: finance incidents cluster around economic harm, healthcare around physical harm, and government deployments around civil rights harm ($\chi^2$=12.97, p=0.0003). Across 15 experiments the hypothesis "higher autonomy → more physical harm" was repeatedly contradicted, reinforcing the argument that trust readiness must be sector-calibrated rather than applied uniformly from generic threat models.

![Figure 4. Sector-Failure Heatmap: Technical Failure Type x Sector of Deployment (AIID, n=69)](figures/fig3_sector_harm_heatmap.png){width=75%}

Biometrics incidents show a disproportionate civil-rights association (EXP_168, p<0.01), and federal deployment sectors do not mirror incident concentration (EXP_108; +0.171), suggesting that governance programs derived from adversarial threat research may misallocate attention relative to incident reality.

These arguments lead us to four testable hypotheses:

H1: Trust readiness surface compliance (TR-surface) is positively associated with operational deployment.

H2: Trust readiness substantive safeguards (TR-substantive) are negatively associated with operational deployment in cross-sectional reporting.

H3: Integration readiness (IR) is positively associated with operational deployment.

H4: Vendor procurement is negatively associated with safeguards that require deep system access (e.g., impact assessment), but less associated with safeguards performable externally (e.g., independent evaluation).

---

## Propositions

The four hypotheses above were tested through the pathway model; Table 2 reports results. Based on the triangulated evidence, we now advance three propositions and one extension that synthesize and extend the empirical findings (Table 3).

**Table 3.** Propositions and primary evidence anchors

| ID | Proposition | Primary Evidence Anchor |
|----|-------------|------------------------|
| P1 | TR and IR are potential strategic complements, but complementarity is contingent on governance maturity: only when TR moves beyond surface compliance does complementarity become possible. Current data show a suppression effect: TR-surface facilitates deployment while TR-substantive dampens it. | TR-surface OR=1.39, p<0.01; TR-substantive OR=0.92, p<0.05; IR OR=1.25, p<0.001; high-IR systems 9$\times$ more likely to show bundled *deep* safeguards |
| P2 | Under heightened regulatory pressure, risk-tiering does not reliably produce higher deep safeguards; organizations exhibit governance theater (53.9% of non-flagged systems, rising to 63.0% of rights/safety systems). | Risk-tiering null across experiments; theater rate *increases* under classification |
| P3 | Commercially procured AI reduces governance implementability via evaluability constraints, specifically limits on control rights and system access, that cascade into weaker substantive safeguard bundles. | Vendor OR=0.43 for impact assessment (n=1,107); effect robust to agency FE (OR=0.47) |
| E1 | AI harms exhibit sector-specific fingerprints that governance investment does not match; organizations need dynamic sensing to recalibrate priorities. | $\chi^2$=12.97, p=0.0003; autonomy hypothesis contradicted across 15 experiments |

---

## Discussion

**TR/IR complementarity: aspiration versus reality.** Table 2 (M4) reveals a suppression effect: TR-surface and TR-substantive pull in opposite directions, explaining why the composite TR index shows no net effect in M3. Surface compliance removes administrative barriers while substantive safeguards introduce friction from genuine scrutiny. IR remains the dominant predictor (OR=1.25, p<0.001), consistent with dynamic capabilities theory [@teece2007] and the complementarity logic of [@milgrom1990]. Complementarity characterizes the *target state* (deep governance paired with deep architecture) rather than the *current state*. With TR-substantive at only 5–9% prevalence, the preconditions for productive TR×IR interaction do not yet exist at population level. However, high-IR systems already show higher bundled safeguard prevalence (14.9% vs. 1.6%).

**Governance theater as capability failure.** As defined in the Theoretical Background, governance theater is the systematic decoupling of formal AI governance structures from the operational routines needed to enact them---an AI-specific instantiation of institutional decoupling [@meyer1977; @bromley2012]. Three reinforcing mechanisms sustain it. First, *evaluability constraints* from commercial procurement block access to model artifacts needed for substantive safeguards. Second, *missing evaluation infrastructure* leaves the highest-demand mitigations dependent on monitoring pipelines that only 5-9% of systems report. Third, *capability bundling thresholds* mean that governance requires coordinated investment across complete safeguard clusters. Partial investment yields no functional governance, echoing dynamic capabilities logic [@teece2007]. Governance theater therefore signals *capability deficit*, not merely motivational deficit.

**Evaluability constraints as a structural barrier.** Our most novel finding is that procurement model acts as a boundary condition on governance capability. Among systems with identified development method, vendor-developed systems are roughly half as likely to report impact assessment (OR=0.43, p=0.002), revealing that trust readiness includes a *structural* dimension: the ability to access the artifacts required to execute governance processes [@ali2023]. Conceptually, this deficit can be understood through the lens of AI boundary resources [@hanelt2025]: when vendors do not provide governance-relevant interfaces (documentation, logging, evaluation endpoints), clients cannot enact deep safeguards even when policies demand them. Vendor boundaries thus block auditability, contestability, and independent evaluation, core trustworthy AI obligations across NIST, EU, and international AI management standards [e.g., @iso42001; @iso23894]. This also explains why risk-tiering fails: if high-impact systems are disproportionately vendor-procured, governance requirements cannot be implemented because the underlying artifacts are inaccessible.

**Contradictions as evidence.** The 67.7% contradiction rate strengthens the contribution: contradictions cluster around core framework assumptions (risk-tiering → proportional safeguards; autonomy → physical harm), showing that contemporary governance frameworks encode aspirational models not yet routinized. Contradictions thus become productive empirical objects for IS theory-building [@gregor2006; @papagiannidis2025], and our pipeline pinpoints precisely where divergence is greatest.

---

## Implications, Limitations, and Conclusion

### Research Implications

This study provides a replicable secondary-data framework for AI governance gap analysis, connecting "what can go wrong" (ATLAS), "what has gone wrong" (AIID), and "what is being done" (EO 13960) without requiring proprietary organizational access. The split-TR finding provides a quantitative signature of governance theater: surface compliance facilitates deployment while substantive safeguards dampen it. This suggests that TR$\times$IR complementarity may emerge only beyond a maturity threshold where substantive safeguards become prevalent. More broadly, the work positions systematic contradictions as productive empirical objects in IS theory-building.

### Practice Implications

For CIOs, the central implication is that governance must shift from checkbox compliance to bundle-based capability building. Organizations should implement safeguard clusters as standard architecture patterns: a verification and validation bundle (assessment → testing → evaluation) and an accountability bundle (assessment → notice → appeal). Procurement must become a first-class governance lever, embedding audit rights, documentation delivery, model transparency, and evaluation access requirements into AI vendor contracts. Finally, governance should be sector-calibrated rather than autonomy-calibrated, aligning safeguard priorities to empirically observed sector-specific harm fingerprints rather than generic threat models.

### Limitations

The governance practice data is federal-only and self-reported. Vendor analyses exclude 650 use cases (37%) with unspecified development method and near-zero governance reporting; their inclusion reverses the bivariate vendor direction, underscoring the sensitivity of procurement findings to sample composition. Pathway model variables are proxies rather than validated scales: the orientation measure captures agency-level portfolio scope, not executive strategic intent directly. Future work should replace proxies with validated instruments, for example organizational AI maturity scales or sector-specific governance metrics. AIID structured taxonomies cover a subset of the full corpus, and ATLAS comprises 52 case studies, limiting fine-grained subgroup analysis. The exploratory experiments should be validated with confirmatory designs, primary organizational data, and outcome measures beyond deployment stage.

### Conclusion

Triangulating adversarial threat knowledge, real-world AI failures, and reported governance practices, this paper reveals a persistent governance readiness gap in a large, policy-salient deployment portfolio. While 61% of federal AI systems report internal review, fewer than 9% report substantive safeguards. Integration readiness is the dominant predictor of operational deployment (OR=1.25). Splitting trust readiness reveals that surface compliance facilitates deployment while substantive safeguards dampen it, a suppression effect that constitutes the quantitative signature of governance theater. Commercial procurement introduces evaluability constraints that undermine substantive governance (OR=0.43 for impact assessment). By triangulating threats, incidents, and governance practice, we offer a replicable method and a reconciled proposition set to guide IS research on how organizational AI portfolio scope can be converted into safe, scalable AI deployment.

---

## References

::: {#refs}
:::
