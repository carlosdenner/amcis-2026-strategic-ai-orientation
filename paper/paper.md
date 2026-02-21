# Strategic AI Orientation Enabled by Trust and Integration Readiness: A Secondary-Data Analysis of Governance Gaps in AI Deployment

## Abstract

Organizations are scaling artificial intelligence (AI) with unprecedented ambition, yet most struggle to convert strategic intent into production-level value. Drawing on dynamic managerial capabilities theory and governance-as-capability perspectives, we investigate how *trust readiness* (governance capability) and *integration readiness* (architecture capability) mediate the link between a CIO-driven AI orientation and realized AI value. We triangulate three publicly available secondary data sources — the MITRE ATLAS adversarial threat matrix (52 case studies), the AI Incident Database (1,362 incidents), and the U.S. Executive Order 13960 Federal AI Use Case Inventory (1,757 use cases across 38 agencies) — through a cross-taxonomy mapping anchored to McKinsey's empirically derived constraints to AI scaling. Our analysis reveals a striking governance gap: while 63% of federal AI deployments hold basic authorization-to-operate, fewer than 9% report substantive safeguards such as impact assessments, bias mitigation, or independent evaluation. Even among the 227 rights-and-safety-impacting use cases where deep governance is mandatory, only 16–23% report these controls. We develop five theoretically grounded propositions linking CIO centrality, trust readiness, integration readiness, their complementarity, and regulatory pressure to AI value realization. The findings contribute to IS research by (1) operationalizing trust and integration readiness as distinct, measurable capability bundles, (2) providing triangulated empirical evidence from threat, incident, and practice data, and (3) offering a replicable analytical framework for governance gap analysis. Implications for CIOs and boards center on the insufficiency of compliance-oriented governance and the need for architectural co-investment to realize strategic AI ambitions.

**Keywords:** AI governance, CIO competencies, trust readiness, integration readiness, MITRE ATLAS, AI Incident Database, secondary data analysis

---

## Introduction

Artificial intelligence has moved from boardroom aspiration to organizational imperative. McKinsey's 2026 survey of global CIOs finds that 92% of organizations are actively deploying generative AI, yet only 1% report full-scale deployment across business functions (McKinsey, 2026). The gap between AI ambition and AI realization is widening, not narrowing. BCG (2025) reports that over 50% of firms cite legacy IT architectures as the primary barrier to AI scaling, while 74% of AI-leading companies — but far fewer laggards — continuously monitor responsible AI (RAI) framework compliance. Deloitte's Tech Trends 2026 argues that agentic AI value comes not from model selection alone but from redesigning operations and building agent-compatible architectures.

These practitioner findings converge on a fundamental tension that IS scholarship has only begun to address: *strategic AI orientation* — the degree to which a firm's leadership commits to AI as a strategic direction — is necessary but insufficient for AI value creation. Realization depends on enabling capabilities that span both governance and architecture.

We frame this tension through the lens of the CIO's evolving role. Upper echelons theory (Hambrick & Mason, 1984) establishes that executive cognition and attention shape strategic choices. Recent IS research extends this to AI contexts, showing that CIO centrality and board AI awareness significantly influence a firm's AI orientation (MISQ, 2021). Yet orientation alone does not produce outcomes. Drawing on the dynamic managerial capabilities framework (Adner & Helfat, 2003; Hossain et al., 2025), we argue that CIOs must develop two distinct capability bundles to convert orientation into value:

1. **Trust readiness** — the governance capability bundle encompassing risk management, compliance, adversarial threat modeling, incident response, and stakeholder accountability. This is grounded in normative frameworks including NIST AI RMF 1.0 (NIST, 2023), the EU AI Act (Regulation 2024/1689), OWASP Top 10 for LLM Applications (OWASP, 2025), and the MITRE ATLAS adversarial threat taxonomy.

2. **Integration readiness** — the architecture capability bundle encompassing agentic design patterns, orchestration controls, data pipeline governance, GenAIOps lifecycle management, and modular deployment infrastructure. This is grounded in practitioner guidance from Microsoft Azure Well-Architected AI, Google Cloud agentic design patterns, and GenAIOps/LLMOps practices.

The central claim of this paper is that these two readiness bundles are *strategic complements*: weak architecture undermines governance effectiveness (policies without enforcement hooks are unverifiable), and weak governance constrains safe architecture deployment (orchestration without access boundaries creates excessive agency risk). Neither bundle alone suffices; their joint presence enables the conversion of AI orientation into realized value.

To ground this argument empirically, we triangulate three publicly available secondary data sources that have not previously been connected in IS research:

- **MITRE ATLAS** (Adversarial Threat Landscape for AI Systems): 52 adversarial case studies, 16 tactics, 155 techniques, and 35 mitigations representing what *can* go wrong with AI systems.
- **AI Incident Database (AIID)**: 1,362 documented incidents and 6,681 media reports representing what *has* gone wrong in real-world AI deployments.
- **EO 13960 Federal AI Use Case Inventory**: 1,757 government AI deployments across 38 agencies with 62 governance and integration variables, representing what organizations *are actually doing*.

By mapping these three sources through a cross-taxonomy bridging table anchored to McKinsey's empirically derived "constraints to AI scaling" (8 barriers reported by CIOs, ranging from talent gaps at 31% to change management resistance at 16%), we construct a triangulated evidence base that links threat landscapes, incident patterns, and governance practice gaps to specific CIO capability requirements.

Our analysis reveals a governance gap that is both striking and consequential. In the EO 13960 inventory, 62.7% of AI use cases report holding an Authorization to Operate (ATO) and 60.7% report internal review approval — suggesting reasonable surface-level compliance. However, when we examine substantive governance safeguards — impact assessments, post-deployment monitoring, bias mitigation, independent evaluation, stakeholder consultation — completion rates plummet to 5.9–8.9%. Even among the 227 use cases explicitly flagged as impacting rights or safety, where deep governance is mandatory by executive order, only 16–23% report these safeguards. This 63%→7% compliance drop-off provides empirical evidence of a *governance theater* phenomenon: organizations check compliance boxes while largely foregoing the substantive governance work that frameworks like NIST AI RMF, the EU AI Act, and MITRE ATLAS require.

This paper makes three contributions. First, we *operationalize* trust and integration readiness as distinct, measurable capability bundles with specific sub-competencies derived from normative standards and practitioner guidance. Second, we provide *triangulated empirical grounding* from threat, incident, and practice data — connecting what can go wrong, what has gone wrong, and what organizations are doing about it. Third, we offer a *replicable analytical framework* (cross-taxonomy mapping methodology, analysis-ready datasets, and reproducible scripts) that other researchers can extend, audit, and build upon. We develop five propositions linking CIO centrality, trust readiness, integration readiness, their complementarity, and regulatory pressure to AI value realization, establishing a testable foundation for future empirical work.

The remainder of this paper is organized as follows. We review related work on CIO roles, AI governance, and capability-based perspectives. We then describe our methodology in detail, emphasizing reproducibility. We present findings from the cross-taxonomy mapping and governance gap analysis. We develop propositions grounded in the triangulated evidence. We conclude with implications for research and practice.

---

## Theoretical Background

### CIO Role and AI Orientation

Upper echelons theory posits that organizational outcomes are partially predicted by the characteristics, experiences, and attention patterns of top management team members (Hambrick & Mason, 1984). The CIO's role has evolved from a technology steward to a strategic partner (Springer, 2023), with digital transformation requiring CIOs to operate simultaneously across technical, business, and institutional domains. In AI contexts, this multidimensionality becomes critical: AI orientation — a firm's strategic commitment to AI as a source of competitive advantage — is shaped by CIO centrality (board access, reporting structure, agenda ownership) and board AI awareness (MISQ, 2021).

McKinsey (2026) frames the contemporary CIO mandate around three imperatives: strategy, speed, and scaled intelligence. BCG (2025) provides empirical backing: at 86% of AI-leading companies, IT leads or co-leads generative AI initiatives, compared to only 54% at AI-stagnating firms. Gartner (2026) identifies agility and risk mastery as the defining items on the CIO agenda, both requiring strategic-level AI orientation. These converging practitioner findings support the theoretical claim that CIO centrality is a necessary antecedent of organizational AI orientation.

### Dynamic Managerial Capabilities and Governance-as-Capability

While upper echelons theory explains *why* CIO attention matters for AI orientation, it does not explain *how* orientation converts into realized value. For this, we draw on the dynamic managerial capabilities (DMC) framework (Adner & Helfat, 2003), which identifies managerial human capital, managerial social capital, and managerial cognition as the micro-foundations of capability building. Hossain et al. (2025) extend DMC to digital leadership contexts, arguing that digital-era executives must develop capabilities that span both technical and institutional domains.

We complement DMC with a governance-as-capability perspective. Rather than treating governance as a static compliance constraint, we conceptualize it as a dynamic organizational capability — a bundle of routines, skills, and processes that enables the firm to sense governance requirements, seize governance opportunities (e.g., building trust as competitive advantage), and reconfigure governance structures as regulatory and technological landscapes evolve (Teece, 2007). This framing aligns with ISACA's COBIT for AI (2024), which defines governance not as overhead but as a set of objectives that organizations must actively build competency in.

### Trust Readiness

Trust readiness is the governance capability bundle that enables an organization to deploy AI systems that are secure, compliant, accountable, and trustworthy. We operationalize trust readiness through four sub-competency domains derived from normative standards:

- **Risk governance and lifecycle management** (NIST AI RMF GOVERN/MAP/MEASURE/MANAGE functions)
- **Adversarial threat modeling and mitigation** (MITRE ATLAS tactics, techniques, and mitigations)
- **Vulnerability management** (OWASP Top 10 for LLM Applications)
- **Regulatory compliance** (EU AI Act Art. 9–15, ISO/IEC 42001, ISO/IEC 23894)

Trust readiness is not binary. The EO 13960 data reveal a continuum from basic compliance (ATO authorization) through intermediate controls (impact assessment) to advanced governance (independent evaluation, bias mitigation). Our analysis quantifies where organizations fall on this continuum and where the most significant gaps lie.

### Integration Readiness

Integration readiness is the architecture capability bundle that enables an organization to deploy AI systems that are scalable, reusable, interoperable, and operationally sustainable. We operationalize integration readiness through sub-competency domains derived from practitioner guidance:

- **Agentic orchestration patterns** (single-agent, multi-agent, human-in-the-loop)
- **Tool-use boundaries and access controls** (agent-to-tool authorization)
- **Nondeterminism management** (evaluation frameworks, output validation)
- **GenAIOps / LLMOps lifecycle governance** (CI/CD for AI, model versioning, drift monitoring)
- **Data pipeline and RAG architecture** (retrieval-augmented generation, embedding management)
- **Modular, composable AI infrastructure** (API-first design, service mesh, observability)

BCG (2025) finds that over 50% of firms identify legacy IT architecture as the primary barrier to AI scaling, underscoring the strategic importance of integration readiness as a capability rather than a fixed asset.

### Complementarity of Trust and Integration Readiness

We theorize that trust readiness and integration readiness are strategic complements (Milgrom & Roberts, 1990): the marginal value of each capability bundle increases when the other is also present. This complementarity arises because:

1. Governance controls require architectural hooks to be *enforceable* — audit logging requires telemetry infrastructure, human override requires architectural approval gates, and model risk assessment requires evaluation pipelines.
2. Architectural patterns require governance boundaries to be *safe* — multi-agent orchestration without access governance creates excessive agency risk (OWASP LLM06); RAG without data governance creates embedding vulnerabilities (OWASP LLM08).

NIST AI RMF explicitly treats GOVERN, MAP, MEASURE, and MANAGE as interdependent functions: governance without measurement infrastructure is unverifiable, and measurement without governance is ungoverned. MITRE ATLAS case studies confirm that incidents typically involve failures across both domains simultaneously.

---

## Methodology

This study employs a secondary-data triangulation approach using three publicly available data sources. The methodology is designed to be fully replicable: all data sources are publicly accessible, all analysis scripts are version-controlled and published in the companion repository, and all intermediate outputs are preserved for audit.

### Research Design

We follow a *convergent triangulation* design (Creswell & Plano Clark, 2018) adapted for secondary data. Three data streams are independently collected, profiled, and coded, then merged through a cross-taxonomy mapping that bridges their distinct classification schemes. The triangulation logic connects:

- **Threat data** (MITRE ATLAS) — what adversarial attacks *can* exploit in AI systems
- **Incident data** (AIID) — what harms *have* occurred in deployed AI systems
- **Practice data** (EO 13960) — what governance and integration controls organizations *actually report*

By connecting these three perspectives, we can identify governance gaps (where practice lags behind threat reality) and capability requirements (what CIOs must build to close the gaps).

### Data Sources

Table 1 summarizes the three data sources.

| Source | Records | Variables | Licence | Snapshot Date |
|--------|--------:|----------:|---------|---------------|
| MITRE ATLAS v4.x | 52 case studies; 16 tactics; 155 techniques; 35 mitigations | Tactic, technique, procedure, mitigation, case narrative | Apache 2.0 | Feb 2026 |
| AI Incident Database (AIID) | 1,362 incidents; 6,681 reports | Incident ID, title, date, description, CSET taxonomy (214 classified), GMF taxonomy (326 classified) | CC BY-SA 4.0 | Feb 2026 |
| EO 13960 Federal AI Use Case Inventory | 1,757 use cases | 62 variables incl. agency, dev stage, purpose, PII handling, ATO status, 12+ safeguard indicators | Public domain | 2024 consolidated |

**MITRE ATLAS** is the Adversarial Threat Landscape for AI Systems, maintained by the MITRE Corporation. It provides a structured taxonomy of adversarial tactics, techniques, and procedures (TTPs) targeting machine learning systems, modeled after the MITRE ATT&CK framework for cybersecurity. Each case study documents a real or demonstrated adversarial scenario, the attack chain (sequence of tactics and techniques), and applicable mitigations. We use the open-source ATLAS data repository (https://github.com/mitre-atlas/atlas-data), which provides machine-readable YAML files for tactics, techniques, mitigations, and case studies.

**AI Incident Database (AIID)** is a systematically curated repository of real-world AI incidents, maintained by the Responsible AI Collaborative. Each incident aggregates one or more media reports and may include structured classifications from two expert taxonomies: the Center for Security and Emerging Technology (CSET) taxonomy, which classifies 214 incidents by AI technique, harm type, and sector; and the Goals, Methods, and Failures (GMF) taxonomy, which classifies 326 incidents by known technical failures, near-miss status, and potential failure categories. We use the full MongoDB snapshot (https://incidentdatabase.ai/research/snapshots/).

**EO 13960 Federal AI Use Case Inventory** is a government-mandated inventory of all AI use cases across U.S. federal agencies, created under Executive Order 13960 (December 2020) and consolidated in the 2024 release. Each use case record includes 62 variables covering agency, system name, development stage, purpose description, AI techniques used, PII handling, infrastructure, review status, and a comprehensive set of governance safeguard indicators (impact assessment, risk identification, monitoring, bias mitigation, stakeholder consultation, appeal processes, etc.). We use the consolidated CSV from the Office of Management and Budget (https://github.com/ombegov/2024-Federal-AI-Use-Case-Inventory).

### Data Profiling and Quality Assessment

Before analysis, we profile each data source to assess completeness, coverage, and quality (`scripts/00_profile_sources.py`, `scripts/04_profile_eo13960.py`). Key profiling steps include:

- **ATLAS**: Count of tactics, techniques, mitigations, and case studies; distribution of case studies across tactics; identification of most-referenced mitigations.
- **AIID**: Count of incidents, reports, and classified incidents per taxonomy; distribution of harm types and sectors; assessment of CSET and GMF coverage overlap.
- **EO 13960**: Completeness analysis across all 62 variables; identification of Tier-1 (basic) vs. Tier-2 (deep) governance safeguards; subsetting of rights-and-safety-impacting use cases (n=227); distribution across agencies and development stages.

### Cross-Taxonomy Mapping

The three data sources use distinct classification schemes that do not share a common ontology. To enable triangulation, we construct a *cross-taxonomy bridging table* that maps elements from each source to a common set of organizing constructs (`scripts/01_cross_taxonomy_mapping.py`).

We anchor the bridging table to McKinsey's empirically derived "constraints to AI scaling" (McKinsey, 2026, Exhibit 5), which reports eight barriers cited by CIOs in a global survey:

| ID | Constraint | CIOs Citing (%) |
|----|-----------|---:|
| C1 | Talent and capability gaps | 31 |
| C2 | Integration complexity | 29 |
| C3 | Security, reliability, and hallucinations | 26 |
| C4 | Regulatory, privacy, and compliance | 24 |
| C5 | Lack of modern data foundations | 21 |
| C6 | Lack of clear business use cases | 18 |
| C7 | Difficulty measuring ROI and value | 17 |
| C8 | Internal resistance and change management | 16 |

We chose these constraints as the organizing anchor because they (a) are empirically derived from CIO surveys, (b) span governance and integration concerns, (c) are practitioner-legible, and (d) provide a natural bridge to the CIO capability framing of our conceptual model.

The mapping procedure proceeds as follows:

1. **ATLAS → Constraints**: Each ATLAS tactic (n=16) is mapped to one or more McKinsey constraints based on the nature of the adversarial threat. For example, *Reconnaissance* (AML.TA0002) maps to C1 (talent gap — insufficient red-teaming capability) and C3 (security); *Exfiltration* (AML.TA0010) maps to C4 (privacy/compliance); *Resource Development* (AML.TA0003) maps to C2 (integration — supply chain and resource acquisition failures).

2. **AIID → Constraints**: AIID incident categories from the CSET and GMF taxonomies are mapped to McKinsey constraints based on the type of harm or failure. For example, *bias/discrimination* incidents map to C4 (compliance) and C3 (reliability); *misinformation/hallucination* incidents map to C3; *privacy/surveillance* incidents map to C4.

3. **EO 13960 → Constraints**: EO 13960 governance safeguard variables are mapped to McKinsey constraints based on the governance function they represent. For example, *impact assessment* maps to C4 (regulatory compliance) and C7 (ROI measurement); *post-deployment monitoring* maps to C7 and C3 (reliability); *stakeholder consultation* maps to C8 (change management).

Each mapping link records the source element, target constraint, link type (threatens, addresses, evidences, or measures), and rationale. The resulting bridging table contains links spanning all three sources and all eight constraints.

### Analysis-Ready Dataset Preparation

We transform the raw cross-taxonomy map into four analysis-ready datasets (`scripts/02_prepare_datasets.py`):

1. **ATLAS cases enriched** (`atlas_cases_enriched.csv`): Each ATLAS case study is tagged with its associated tactics, techniques, and mitigations, then linked to McKinsey constraints via the bridging table.

2. **AIID incidents classified** (`aiid_incidents_classified.csv`): AIID incidents with CSET and/or GMF classifications are merged, and each incident is tagged with applicable McKinsey constraints based on its failure type and sector.

3. **EO 13960 scored** (`eo13960_scored.csv`): Each federal AI use case receives a governance readiness score computed from the ratio of reported safeguards to applicable safeguards, yielding a continuous 0–1 governance completeness index.

4. **Unified evidence base** (`unified_evidence_base.csv`): A long-format stacked dataset combining all three sources, with common fields for source, element, constraint, link type, and evidence strength indicators.

### Figure Generation

Publication-ready figures are generated programmatically (`scripts/03_generate_figures.py`) to ensure reproducibility. Five figures are produced:

1. **Governance gap bar chart**: Side-by-side comparison of Tier-1 (basic) vs. Tier-2 (deep) safeguard completion rates in the EO 13960 data.
2. **AIID failure–sector heatmap**: Cross-tabulation of the top 8 technical failure types by the top 8 deployment sectors, showing incident concentration patterns.
3. **ATLAS tactic frequency chart**: Distribution of adversarial cases across the 16 ATLAS tactics, highlighting which attack categories are most prevalent.
4. **Constraint coverage radar**: Coverage of each McKinsey constraint across the three data sources, showing triangulation breadth.
5. **Governance readiness distribution**: Histogram of the governance completeness index across all 1,757 EO 13960 use cases.

### Reproducibility

All analysis code, data paths, and intermediate outputs are organized in a public GitHub repository (https://github.com/carlosdenner/amcis-2026-strategic-ai-orientation.git). The repository follows a separation-of-concerns structure:

```
data/raw/         ← Immutable source data (not edited after acquisition)
data/processed/   ← Regenerable analysis outputs
scripts/          ← Numbered pipeline scripts (00–04)
paper/figures/    ← Publication-ready PNGs (regenerated by scripts/03)
```

To reproduce all results from raw data:

```bash
python scripts/01_cross_taxonomy_mapping.py   # → cross_taxonomy_map.csv
python scripts/02_prepare_datasets.py         # → 4 analysis CSVs
python scripts/03_generate_figures.py         # → 5 publication PNGs
```

Dependencies are specified in `requirements.txt` (pandas, PyYAML, matplotlib, numpy). No API keys are required for the core analysis pipeline; the optional LLM-based enrichment pipeline (`scripts/agents/`) requires an OpenAI API key but is not needed to reproduce the reported findings.

---

## Findings

*(To be completed after co-author review of research angle selection and cross-taxonomy mapping results.)*

---

## Propositions

Based on the triangulated evidence from the cross-taxonomy mapping and governance gap analysis, we develop five testable propositions.

**Proposition 1 (CIO Centrality → AI Orientation):** *The greater the CIO's centrality in strategic decision-making (reflected in reporting structure, board access, and AI agenda ownership), the stronger the firm's AI orientation.*

This proposition is grounded in upper echelons theory and supported by BCG's finding that at 86% of AI-leading companies, IT leads or co-leads GenAI initiatives versus 54% at laggards.

**Proposition 2 (Trust Readiness → Value Conversion):** *Higher trust readiness strengthens the conversion of AI orientation into production-scale value by reducing incident risk, enabling auditability, and satisfying regulatory license-to-operate requirements.*

ATLAS incident analysis confirms the cost of trust readiness gaps: Impact (47 cases), Defense Evasion (34), and Model Access (24) are the dominant failure modes — all preventable through monitoring, threat modeling, and access governance. The most commonly missing control across incidents is AI Telemetry Logging (33 incidents).

**Proposition 3 (Integration Readiness → Value Conversion):** *Higher integration readiness strengthens the conversion of AI orientation into production-scale value by enabling reusable architectures, operational lifecycle management, and scalable deployment.*

ATLAS tactic frequency analysis shows that Resource Development (77 instances) and Initial Access (41 instances) — both integration-domain failures — are the most prevalent attack enablers.

**Proposition 4 (Complementarity):** *Trust readiness and integration readiness are strategic complements: the marginal value of each increases when the other is also present.*

ATLAS case studies show that the dominant failure pattern combines integration weaknesses (Resource Development 77×, Initial Access 41×) with trust gaps (missing telemetry 33×, missing access controls 20×) — consistent with co-occurring failures across both bundles.

**Proposition 5 (Regulatory Pressure):** *External regulatory pressure increases the strategic salience of trust readiness, elevating governance capability-building onto the CIO and board AI orientation agenda.*

The EU AI Act creates binding obligations for high-risk AI (Art. 9–15) and GPAI models with systemic risk (Art. 53–55). EO 13960 data show that even mandatory governance requirements are underimplemented (16–23% among rights-impacting cases), suggesting that regulatory pressure has not yet translated into governance capability — precisely the gap our framework addresses.

---

## Discussion

*(To be completed after findings section.)*

---

## Implications for Research and Practice

*(To be completed.)*

---

## Limitations and Future Research

*(To be completed.)*

---

## Conclusion

*(To be completed.)*

---

## References

*(To be formatted per AMCIS 2026 style — APA 7th edition.)*
