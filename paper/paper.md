---
bibliography: references.bib
csl: apa.csl
link-citations: true
---

# Governance Readiness Gaps in Organizational AI Deployment: A Triangulated Analysis of Threats, Incidents, and Practice

*Indicate Submission Type: Full Paper*

<!-- AMCIS PCS fields, abstract, keywords, and authors entered in the submission system, not in this file.

**Abstract.** Organizations are scaling artificial intelligence (AI) with unprecedented ambition, yet governance readiness lags far behind deployment pace. Drawing on dynamic managerial capabilities theory and institutional decoupling, we investigate how *trust readiness* (governance capability) and *integration readiness* (architecture capability) shape the link between organizational AI orientation and realized AI value. Triangulating MITRE ATLAS, the AI Incident Database, and the U.S. EO 13960 Federal AI Use Case Inventory (1,757 deployments), our analysis reveals governance theater: while 61% of federal AI deployments report internal review approval, fewer than 9% report substantive safeguards such as impact assessments, bias mitigation, or independent evaluation, and risk-tiering does not rescue governance depth. A use-case-level logistic regression shows that integration readiness is the dominant predictor of operational deployment (OR=1.40, p<0.001), whereas trust readiness shows no independent effect, indicating that architecture, not governance, currently binds AI value realization. Across 14 convergent experiments, commercial procurement emerges as the strongest structural barrier: vendor-supplied systems are 71% less likely to report impact assessment after controls (OR=0.29, p<0.001). We contribute by empirically documenting governance theater and identifying procurement opacity as a structural antecedent of governance failure.

**Keywords:** AI governance, governance theater, trust readiness, integration readiness, secondary data triangulation
-->

---

## Introduction

Artificial intelligence has shifted from boardroom aspiration to organizational imperative. McKinsey's latest global survey reports that 88% of organizations now use AI in at least one business function, yet the majority remain in piloting stages and only about one-third have begun scaling [@mckinseyai2025]. Over 50% of firms cite legacy IT architectures as the primary barrier [@bcg2025]. The gap between AI ambition and AI realization is widening, not narrowing.

We investigate this gap through a governance lens. Using the U.S. Federal AI Use Case Inventory (1,757 deployments across 38 agencies), we find that 61% of AI systems report internal review approval, but fewer than 9% report substantive safeguards such as impact assessments, bias mitigation, or independent evaluation. This steep "surface-to-substance" drop-off is not merely organizational immaturity; it constitutes *governance theater*, a form of institutional decoupling [@meyer1977] in which organizations adopt formal governance structures while the operational routines needed to enact them remain absent.

Documenting governance theater raises a harder question: *why does it persist?* Despite proliferating governance frameworks, from NIST AI Risk Management Framework (RMF) [@nist2023] to the EU AI Act [@euaiact2024] and beyond, substantive safeguards remain rare even under federal mandate. Recent IS syntheses of responsible AI governance propose integrative frameworks yet emphasize that empirical work connecting governance designs to enacted routines and outcomes remains underdeveloped [@papagiannidis2025], precisely the gap we address. We argue that the explanation lies not in awareness deficits but in *capability constraints*. Governance demands architectural hooks to be enforceable, and commercial procurement introduces opacity barriers that block access to those hooks. If governance theater persists even where mandates and classification requirements both exist, the constraint must lie deeper than regulatory design.

We frame this argument through two theoretical lenses. Upper echelons theory [@hambrick1984] establishes that CIO centrality shapes strategic AI orientation [@misq2021; @mckinsey2026], but orientation alone does not produce value. Drawing on dynamic managerial capabilities (DMC) [@adner2003; @hossain2025], we argue that converting orientation into realized value requires two capability bundles: *trust readiness* (TR), governance capabilities spanning risk management, compliance, and accountability, and *integration readiness* (IR), architecture capabilities spanning data pipelines, evaluation infrastructure, and deployment controls. These bundles should function as strategic complements [@milgrom1990], yet our evidence suggests they are currently decoupled. Governance safeguards show no relationship to deployment outcomes, and commercial procurement creates transparency barriers that prevent organizations from executing substantive safeguards even when policies demand them.

To ground this argument empirically, we triangulate three publicly available secondary data sources not previously connected in IS research: MITRE ATLAS (52 adversarial case studies representing what *can* go wrong), the AI Incident Database (1,362 incidents representing what *has* gone wrong), and the Executive Order (EO) 13960 Federal AI Use Case Inventory (1,757 deployments representing what organizations *are actually doing*). Through this triangulated analysis, we demonstrate that risk-tiered AI governance frequently functions as governance theater, identify procurement opacity and missing architectural enforceability as binding constraints, and provide a replicable analytical framework that other researchers can extend with public data.

---

## Theoretical Background

Upper echelons theory posits that organizational outcomes reflect the cognitive orientations and attention patterns of top executives [@hambrick1984]. In AI contexts, the Chief Information Officer (CIO) role has evolved from technology steward to strategic partner [@chawla2023], and CIO centrality, including board access, reporting structure, and agenda ownership, together with board AI awareness significantly influence a firm's strategic AI orientation [@misq2021]. Practitioner surveys confirm that strategy, speed, and risk mastery now define the CIO agenda [@mckinsey2026; @bcg2025; @gartner2026]. We therefore take CIO-driven strategic AI orientation as a contextual assumption; our propositions focus on the downstream capability mechanisms, trust readiness and integration readiness, that convert orientation into realized AI value.

Strategic orientation, however, is necessary but insufficient. The dynamic managerial capabilities framework [@adner2003; @hossain2025] identifies managerial human capital, social capital, and cognition as micro-foundations of capability building, yet does not specify *which* capabilities matter for AI value realization. At the individual level, @pinski2023 operationalize AI literacy as a measurable human competency spanning technical, evaluative, and practical dimensions. This is precisely the kind of micro-foundation that enables managers to sense governance requirements and evaluate AI system behaviors. We complement DMC with a governance-as-capability perspective [@teece2007], conceptualizing governance not as a static compliance constraint but as a dynamic organizational capability: a bundle of routines enabling the firm to sense governance requirements, seize governance opportunities (e.g., building trust as competitive advantage), and reconfigure governance structures as regulatory and technological landscapes evolve.

We operationalize this framework through two capability bundles. **Trust readiness** (TR) encompasses risk management, compliance, adversarial threat modeling, incident response, and stakeholder accountability, grounded in normative frameworks including NIST AI RMF [@nist2023], the EU AI Act [@euaiact2024], and the MITRE ATLAS adversarial threat taxonomy. TR spans a continuum from surface compliance (internal review boards, authorization to operate) to substantive safeguards (impact assessment, independent evaluation, bias mitigation) that demand deep technical access, cross-functional coordination, and sustained investment. Our composite TR index (0–9) aggregates both tiers. Theoretically, however, the complementarity mechanism is driven by the *substantive* tier: surface approvals alone cannot interact productively with architecture because they impose no operational demands on the system. The distribution of federal AI systems across this continuum serves as the paper's core empirical anchor.

**Integration readiness** (IR) is the architecture capability bundle encompassing data pipeline governance, evaluation infrastructure, deployment controls, and code/model accessibility. Concretely, IR includes data catalogs, documentation practices, provisioned infrastructure, source-code access, and component reuse, the organizational and technical conditions for deploying and sustaining AI systems at scale. Critically, IR supplies the *enforcement hooks* that make governance actionable: without telemetry infrastructure, audit logging is impossible; without evaluation pipelines, bias testing cannot be conducted; without code access, independent review is foreclosed. We term the resulting boundary condition *governance implementability*: the degree to which an organization possesses the control rights and technical access needed to execute governance routines. Implementability depends on access to model artifacts, telemetry, and evaluation interfaces; when procurement or outsourcing restricts these rights, it collapses and decoupling persists even under mandate. @bcg2025 find that over 50% of firms identify legacy IT architecture as the primary barrier to AI scaling, underscoring IR's strategic importance as a dynamic capability rather than a fixed asset.

Institutional theory shows that organizations routinely adopt formal structures to signal conformity while decoupling those structures from day-to-day operations [@meyer1977; @bromley2012]. @ali2023 document how this dynamic extends to AI ethics, where organizational structures create barriers between stated commitments and operational practice. We adopt the term *governance theater* to describe this pattern in AI governance: the systematic adoption of authorization artifacts without the operational safeguards needed to make authorization meaningful. Our empirical analysis tests whether a large-scale federal AI inventory exhibits governance theater and identifies the structural mechanisms that sustain it.

We theorize that trust readiness and integration readiness are strategic complements [@milgrom1990]: the marginal return to each increases when the other is present. Governance controls require architectural hooks to be *enforceable*: for example, bias testing is impossible without evaluation pipelines, and independent review is foreclosed without code access. Conversely, architectural patterns require governance boundaries to be *safe*. Crucially, we predict that this complementarity is *conditional on governance maturity*: when TR remains theatrical, surface compliance without operational substance, it cannot interact productively with IR. We therefore expect integration readiness to be the binding constraint in current deployments, with complementarity emerging only as governance deepens.

---

## Methodology

We follow a convergent triangulation design [@creswell2018] using three publicly available data sources. Table 1 summarizes each source.

**Table 1.** Data sources

| Source | Records | Coverage | Licence |
|--------|--------:|----------|---------|
| MITRE ATLAS v4.x | 52 case studies; 16 tactics; 155 techniques; 35 mitigations | Adversarial AI threats | Apache 2.0 |
| AI Incident Database (AIID) | 1,362 incidents; 6,681 reports | Real-world AI harms (CSET: 201 classified; GMF: 278 classified) | CC BY-SA 4.0 |
| EO 13960 Federal AI Use Case Inventory | 1,757 use cases; 38 agencies; 62 variables | Governance and integration practice | Public domain |

We use ATLAS for adversarial threat coverage, AIID for realized harms and their structured taxonomies (Center for Security and Emerging Technology [CSET] for harm types/sectors; Goals, Methods, and Failures [GMF] taxonomy for technical failure modes), and EO 13960 for reported governance and integration practice across 62 variables per use case.

**Cross-taxonomy mapping.** Because the three data sources use distinct classification schemes, we construct a bridging table that maps elements from each source to a common set of organizing constructs, anchored to CIO-reported constraints to AI scaling [@mckinsey2026]. The mapping links 126 elements across all three sources via rule-based assignments with explicit rationale. Monte Carlo sensitivity analysis (1,000 iterations at 10–20% perturbation) confirms mapping stability (mean $\rho$=0.95). Importantly, the paper's core findings, namely governance drop-off, IR dominance, and procurement opacity, are computed directly from EO 13960 variables and are not mediated by the cross-taxonomy map.

**Pathway model.** To provide a preliminary test of the theorized Orientation $\rightarrow$ TR $\times$ IR $\rightarrow$ Value pathway, we estimate nested logistic regressions at the use-case level (n=1,757) predicting operational deployment status. Trust readiness (TR, 0–9) counts nine governance safeguard indicators: ATO, internal review, impact assessment, real-world testing, independent evaluation, post-deployment monitoring, AI notice, disparity mitigation, and appeal process. Integration readiness (IR, 0–7) counts seven architecture indicators: data catalog, documentation, custom code, source-code access, provisioned infrastructure, timely resources, and code/data reuse. Orientation is an agency-level composite of portfolio size and domain breadth. Controls include development method and rights/safety classification. We estimate four nested models: (M1) controls only; (M2) + orientation; (M3) + TR + IR; (M4) + TR $\times$ IR interaction.

**Exploratory analysis.** We employ a Bayesian-surprise-based exploratory analysis engine that programmatically generates and tests hypotheses from the data schema. Across 400 experiments (Session 1: 100; Session 2: 300), 67.7% of hypotheses were contradicted, a result we treat as substantive evidence of governance gaps rather than methodological failure. We report only findings supported by convergent multi-experiment evidence or independently confirmed through standard statistical tests. All analysis code and data are available in the companion repository.

---

## Findings

Our findings are exploratory, not confirmatory. We emphasize patterns supported by convergent evidence across multiple independent experiments or confirmed through standard statistical tests.

### Governance Theater: Depth Collapse and Tiering Failure

Federal AI deployments exhibit high surface compliance but strikingly low substantive safeguards. Across 1,757 EO 13960 use cases, internal review is reported by 60.7% and Authorization to Operate (ATO) by 37.2%, yet substantive safeguards, including impact assessment, independent evaluation, bias mitigation, and the like, cluster in the 5–9% range. This ~55 percentage-point gap between internal review and the substantive safeguard floor shows that review processes exist but the operational governance work that frameworks prescribe remains rare.

![The Governance Drop-off: Surface Compliance vs. Substantive Safeguards (EO 13960)](figures/fig1_governance_dropoff.png)

This gap persists precisely where governance should intensify. Among the 227 use cases flagged as rights- or safety-impacting, deep safeguards rise but remain limited: impact assessment reaches 22.5%, independent evaluation 18.1%, and bias mitigation 16.3%. Even in this mandatory subset, the gap is attenuated rather than eliminated.

Risk-tiering, the foundational design principle of contemporary AI governance, fails to rescue governance depth. High-impact systems are no more likely to report independent evaluation (EXP_146, n=1,718, p<0.0001; contradicted), nor are rights-impacting systems more likely to report impact assessment (EXP_207, n=1,757; contradicted). Multiple experiments replicate this null. In institutional-theory terms, this constitutes policy-practice decoupling [@meyer1977; @bromley2012]: adopted classification policies do not translate into differentiated operational practice.

A preliminary pathway test reinforces this interpretation. Table 2 reports nested logistic regressions predicting operational deployment (52.4% of use cases). Integration readiness is the dominant predictor (M4: OR=1.40, 95% CI [1.33, 1.48], p<0.001), while trust readiness shows no independent effect (p=0.287) and the TR$\times$IR interaction is marginally negative (p=0.052), suggesting weak substitution rather than the theorized complementarity.

**Table 2.** Nested logistic regression: DV = Operational deployment (0/1)

| Variable | M1 | M2 | M3 | M4 |
|:---------|:--:|:--:|:--:|:--:|
| Constant | -0.357\*\*\* (0.063) | -0.387\*\*\* (0.064) | -1.200\*\*\* (0.093) | -1.242\*\*\* (0.096) |
| Vendor | 1.109\*\*\* (0.119) | 1.171\*\*\* (0.121) | 0.813\*\*\* (0.130) | 0.732\*\*\* (0.137) |
| Mixed dev. | 0.955\*\*\* (0.166) | 0.960\*\*\* (0.167) | 0.436\* (0.178) | 0.367\* (0.181) |
| Rights/safety | 0.487\*\* (0.158) | 0.588\*\*\* (0.161) | 0.928\*\*\* (0.175) | 0.910\*\*\* (0.175) |
| Orientation | | -0.195\*\*\* (0.059) | -0.273\*\*\* (0.065) | -0.279\*\*\* (0.066) |
| TR | | | -0.054 (0.033) | 0.085 (0.080) |
| IR | | | 0.316\*\*\* (0.025) | 0.339\*\*\* (0.028) |
| TR x IR | | | | -0.028+ (0.014) |
| *N* | 1,757 | 1,757 | 1,757 | 1,757 |
| Pseudo R2 | 0.055 | 0.059 | 0.147 | 0.148 |
| AIC | 2,306.7 | 2,297.6 | 2,089.4 | 2,087.7 |

+p<0.10; \*p<0.05; \*\*p<0.01; \*\*\*p<0.001. Standard errors in parentheses.

### Binding Constraints: Procurement Opacity and Architectural Enforceability

Commercial procurement is the strongest and most consistently supported predictor of governance under-implementation. It is not merely a correlate of low governance but a structural opacity barrier that prevents organizations from translating governance commitments into implementable safeguards.

Across 14 convergent experiments, vendor-supplied systems report lower transparency (code access, documentation) and weaker governance. The pattern is most pronounced for impact assessment, where vendor systems trail in-house systems (6.4% vs. 10.3%).

![Commercial Opacity as a Governance Barrier: Vendor-Supplied vs. In-House AI Systems (EO 13960)](figures/fig2_commercial_opacity.png)

Multivariate logistic regressions (n=1,107) controlling for impact classification, public-facing status, operational stage, and agency fixed effects confirm these bivariate results. Impact assessment, the safeguard requiring the deepest vendor cooperation, shows the strongest effect: vendor-developed systems are 71% less likely to report it (OR=0.29, 95% CI [0.15, 0.56], p<0.001). This effect *strengthens* with controls, indicating genuine procurement opacity rather than confounding. By contrast, independent evaluation, performable by external parties, shows no vendor effect ($\text{OR} \approx 1.0$), confirming that the barrier is specific to activities requiring internal system access. Transparency deficits cascade into accountability: code access strongly predicts appeal processes (OR=7.52, p<0.001) and independent evaluation (OR=19.48, p<0.001).

Integration readiness provides the architectural context for these patterns. The IR index (mean=3.15, median=3) substantially outpaces the TR index (mean=1.49, median=1), and operational deployment rates differ sharply by IR level: 33% for low-IR (0–2), 57% for mid-IR (3–4), and 73% for high-IR (5–7). Where governance *is* present, it appears as coherent capability bundles rather than isolated controls. Impact assessment predicts real-world testing (surprise +0.581), and high-IR systems are nine times more likely to exhibit bundled deep safeguards (14.9% vs. 1.6%, $\chi^2$=87.3, p<0.001; Spearman $\rho$=0.228, p<0.001). Yet assessments do not reliably trigger mitigation, a means-ends decoupling [@bromley2012] where documentation artifacts function independently of operational action, consistent with the governance theater pattern.

### Contextual Calibration: Sector-Specific Harm Fingerprints

AIID incident analysis reveals that AI harms are sector-structured rather than autonomy-driven: finance incidents cluster around economic harm, healthcare around physical harm, and government deployments around civil rights harm ($\chi^2$=12.97, p=0.0003). Across 15 experiments the hypothesis "higher autonomy $\rightarrow$ more physical harm" was repeatedly contradicted, reinforcing the argument that trust readiness must be sector-calibrated rather than applied uniformly from generic threat models.

![Sector-Failure Heatmap: Technical Failure Type x Sector of Deployment (AIID, n=69)](figures/fig3_sector_harm_heatmap.png){width=75%}

Biometrics incidents show a disproportionate civil-rights association (EXP_168, p<0.01), and federal deployment sectors do not mirror incident concentration (EXP_108; +0.171), suggesting that governance programs derived from adversarial threat research may misallocate attention relative to incident reality.

---

## Propositions

Based on the triangulated evidence, we advance three propositions and one extension (Table 3).

**Table 3.** Propositions and primary evidence anchors

| ID | Proposition | Primary Evidence Anchor |
|----|-------------|------------------------|
| P1 | TR and IR are strategic complements, but complementarity is contingent on governance maturity: only when TR moves beyond surface compliance does the TR $\times$ IR interaction become positive. | IR OR=1.40, p<0.001; TR null (composite mixes surface + deep); high-IR systems 9$\times$ more likely to show bundled *deep* safeguards |
| P2 | Under heightened regulatory pressure, risk-tiering does not reliably produce higher deep safeguards; organizations exhibit governance theater. | Risk-tiering null across experiments; mandatory-subset safeguards flat |
| P3 | Commercially procured AI reduces governance implementability via a transparency deficit that cascades into weaker safeguard bundles. | Vendor OR=0.29 for impact assessment; 14 convergent experiments |
| E1 | AI harms exhibit sector-specific fingerprints that governance investment does not match; organizations need dynamic sensing to recalibrate priorities. | $\chi^2$=12.97, p=0.0003; autonomy hypothesis contradicted across 15 experiments |

---

## Discussion

**TR/IR complementarity: aspiration versus reality.** Table 2 shows IR dominates deployment prediction (OR=1.40) while TR shows no effect and the interaction is marginally negative. We interpret this as a maturity threshold: with mean TR at 1.49 out of 9, governance is too thin to interact meaningfully with architecture. Complementarity characterizes the *target state* (deep governance paired with deep architecture) rather than the *current state* (theatrical governance alongside functional architecture). High-IR systems show significantly higher bundled safeguard prevalence (14.9% vs. 1.6%), indicating that preconditions for complementarity exist in the high-IR tail but remain too rare to generate a population-level interaction.

**Governance theater as capability failure.** We characterize governance theater as the systematic decoupling of formal AI governance structures from the operational routines needed to enact them, an AI-specific instantiation of institutional decoupling [@meyer1977; @bromley2012]. Three reinforcing mechanisms sustain it: (i) *procurement opacity* blocks access to model artifacts needed for substantive safeguards; (ii) *missing evaluation infrastructure* leaves the highest-demand mitigations dependent on monitoring pipelines that only 5–9% of systems report; and (iii) *capability bundling thresholds* mean that governance requires coordinated investment across complete safeguard clusters: partial investment yields no functional governance, echoing DMC logic [@teece2007]. Governance theater therefore signals *microfoundation deficit*, not merely motivational deficit.

**Procurement opacity as a structural barrier.** The most novel empirical contribution is identifying procurement model as a boundary condition on governance capability. Vendor-developed systems are 71% less likely to report impact assessment (OR=0.29, p<0.001), revealing that trust readiness includes a *structural* dimension: the ability to access the artifacts required to execute governance processes [@ali2023]. Conceptually, this deficit can be understood through the lens of AI boundary resources [@hanelt2025]: when vendors do not provide governance-relevant interfaces (documentation, logging, evaluation endpoints), clients cannot enact deep safeguards even when policies demand them. Vendor boundaries thus block auditability, contestability, and independent evaluation, core trustworthy AI obligations across NIST, EU, and international AI management standards [e.g., @iso42001; @iso23894]. This also explains why risk-tiering fails: if high-impact systems are disproportionately vendor-procured, governance requirements cannot be implemented because the underlying artifacts are inaccessible.

**Contradictions as evidence.** The 67.7% contradiction rate strengthens the contribution: contradictions cluster around core framework assumptions (risk-tiering $\rightarrow$ proportional safeguards; autonomy $\rightarrow$ physical harm), showing that contemporary governance frameworks encode aspirational models not yet routinized. Contradictions thus become productive empirical objects for theory-building, and our pipeline pinpoints precisely where divergence is greatest.

---

## Implications, Limitations, and Conclusion

### Research Implications

This study provides a replicable secondary-data framework for AI governance gap analysis, connecting "what can go wrong" (ATLAS), "what has gone wrong" (AIID), and "what is being done" (EO 13960) without requiring proprietary organizational access. The finding that IR dominates while TR shows no effect suggests that TR$\times$IR complementarity may emerge beyond a governance maturity threshold. More broadly, the work positions systematic contradictions as productive empirical objects in IS theory-building.

### Practice Implications

For CIOs, the central implication is that governance must shift from checkbox compliance to bundle-based capability building. Organizations should implement safeguard clusters as standard architecture patterns: a verification and validation bundle (assessment $\rightarrow$ testing $\rightarrow$ evaluation) and an accountability bundle (assessment $\rightarrow$ notice $\rightarrow$ appeal). Procurement must become a first-class governance lever, embedding audit rights, documentation delivery, model transparency, and evaluation access requirements into AI vendor contracts. Finally, governance should be sector-calibrated rather than autonomy-calibrated, aligning safeguard priorities to empirically observed sector-specific harm fingerprints rather than generic threat models.

### Limitations

The governance practice data is federal-only and self-reported. An alternative explanation for the null TR$\times$IR interaction is organizational siloing: governance and architecture may be implemented by separate units, producing independent investment patterns. Pathway model variables are proxies rather than validated scales; future work should replace them with validated instruments such as top management team (TMT) AI literacy measures [@pinski2024] or CIO attention constructs [@bendig2023]. AIID structured taxonomies cover a subset of the full corpus, and ATLAS comprises 52 case studies, limiting fine-grained subgroup analysis. The exploratory experiments should be validated with confirmatory designs, primary organizational data, and outcome measures beyond deployment stage.

### Conclusion

Triangulating adversarial threat knowledge, real-world AI failures, and reported governance practices, this paper reveals a persistent governance readiness gap in a large, policy-salient deployment portfolio. While 61% of federal AI systems report internal review, fewer than 9% report substantive safeguards, and integration readiness, not trust readiness, is the dominant predictor of operational deployment (OR=1.40). Commercial procurement emerges as a structural opacity barrier that undermines implementable governance (OR=0.29 for impact assessment). By triangulating threats, incidents, and governance practice, we offer a replicable method and a reconciled proposition set to guide IS research on how CIO-driven AI orientation can be converted into safe, scalable AI value.

---

## References

::: {#refs}
:::
