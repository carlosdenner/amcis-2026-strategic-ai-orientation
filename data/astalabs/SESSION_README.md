# AstaLabs AutoDiscovery – Session Setup Guide

## Discovery session name
```
AMCIS2026 – AI Orientation Trust-Integration Readiness
```

## Dataset context
```
This dataset consolidates three public secondary-data sources used in a
design-science / framework-synthesis study targeting AMCIS 2026.

Sources:
1. AIID – AI Incident Database (1,366 real-world AI failure incidents
   classified by harm domain, tangible harm, sector, autonomy level,
   AI technology, and technical failure type).
2. MITRE ATLAS – Adversarial Threat Landscape for AI Systems (84
   adversarial case studies coded with tactics, techniques, and
   mitigations; cross-mapped to McKinsey AI-scaling constraints C1–C8).
3. EO 13960 – U.S. Federal AI Use-Case Inventory (3,658 government AI
   deployments scored for governance readiness across two tiers: basic
   controls and deep governance safeguards including impact assessments,
   bias mitigation, and independent evaluation).

Analytical layers built on top of these three sources include:
- A crosswalk matrix linking 42 governance requirements from NIST AI RMF,
  EU AI Act, ISO 42001, and OWASP Top-10 LLM to 18 architecture controls.
- 16 sub-competencies in two bundles: Trust Readiness (TR-1…TR-8) and
  Integration Readiness (IR-1…IR-8).
- Incident-coding of ATLAS cases mapping tactics to competency gaps.
- Five testable propositions (P1–P5) with falsifiability criteria.

The CSV concatenates ALL tables (sparse — use the `source_table` column
to segment by data source). Supplementary .md and .json files provide
construct definitions, proposition narratives, and validation reports.

Known limitation: EO 13960 data skews toward U.S. federal agencies;
AIID coverage varies by year; ATLAS cases are curated (not exhaustive).
```

## Domain of datasets
```
Information Systems / AI Governance / Enterprise Architecture
```

## Files to upload
| # | File | Type | Purpose |
|---|------|------|---------|
| 1 | `astalabs_discovery_all_data.csv` | CSV | All 6,705 rows across 14 tables |
| 2 | `context_construct_definitions.md` | MD | Trust & Integration Readiness construct definitions |
| 3 | `context_propositions.md` | MD | Five propositions (P1–P5) with evidence |
| 4 | `context_validation_report.md` | MD | Step-5 validation findings |
| 5 | `context_crosswalk_evidence.json` | JSON | Crosswalk evidence details |
| 6 | `context_propositions.json` | JSON | Proposition evidence details |
| 7 | `context_step1_evidence.json` | JSON | Construct-building evidence |
