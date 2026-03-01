# AMCIS 2026 ↔ Template Comparison & Backport Report

**Generated**: 2026-02-28  
**AMCIS workspace**: `AMCIS 2026/`  
**Template repo**: `carlosdenner/paper-research-template` (master branch)

---

## Executive Summary

The AMCIS 2026 project has **massively evolved** beyond the template across every dimension — domain-specific content, pipeline sophistication, data richness, and output quality. The template is a proper skeleton with `# TODO` placeholders and `CUSTOMIZE` comments; the AMCIS version is a fully-realised, production-quality research pipeline.

**Key finding**: Almost every AMCIS agent file contains substantial improvements that are **generalizable** and should be backported. The template can absorb most of these improvements while keeping them domain-agnostic via configuration/placeholders.

---

## 1. File-by-File Agent Comparison (`scripts/agents/`)

### 1.1 `__init__.py`

| Aspect | Template | AMCIS |
|--------|----------|-------|
| Content | Empty | `# AMCIS 2026 — Agentic Analysis Pipeline` |
| **Verdict** | Identical (effectively) | No meaningful difference |

**Backport**: None needed.

---

### 1.2 `config.py`

| Aspect | Template | AMCIS |
|--------|----------|-------|
| Lines | ~75 | 199 |
| **`dotenv` support** | ✅ `from dotenv import load_dotenv` | ❌ Missing |
| **Env var prefix** | `PAPER_EXTRACTION_MODEL` | `AMCIS_EXTRACTION_MODEL` |
| **`DATA_DIR` / `RAW_DIR` paths** | ✅ Defined | ❌ Missing (has `ATLAS_DIR` instead) |
| **Retry config** | `MAX_RETRIES=3`, `RETRY_DELAY=5` | `MAX_RETRIES=6`, `RETRY_DELAY=15` |
| **`LITERATURE_FILES`** | Empty dict with commented examples | 34 fully populated entries |
| **`SOURCE_TYPES`** | Empty dict | 34 entries with academic/standard/practitioner |
| **Construct source groups** | Placeholder comments | `TRUST_SOURCES`, `INTEGRATION_SOURCES`, `ORIENTATION_SOURCES`, `REGULATORY_SOURCES` — fully populated |

**AMCIS improvements to backport**:
1. **Higher retry defaults** (`MAX_RETRIES=6`, `RETRY_DELAY=15`) — more robust for production runs
2. **Construct source groups pattern** — the actual grouping variables are AMCIS-specific, but the template should show a clearer pattern with typed lists
3. **`ATLAS_DIR` / `ATLAS_DIST`** — AMCIS-specific, don't backport

**Template has and AMCIS doesn't**:
1. ⚠️ **`from dotenv import load_dotenv; load_dotenv()`** — AMCIS should add this
2. ⚠️ **`DATA_DIR` / `RAW_DIR` path constants** — AMCIS should add these generic paths
3. **Generic env var prefix** `PAPER_*` is better than `AMCIS_*` for template

---

### 1.3 `literature_loader.py`

| Aspect | Template | AMCIS |
|--------|----------|-------|
| Lines | ~120 | 244 |
| **BS4 import** | Graceful fallback (`HAS_BS4`) | Hard import (no fallback) |
| **`load_sources()`** | Prints skip reason for failed loads | Silent skip |
| **`prepare_source_context()`** | Simple — concat docs to max chars | **Sophisticated**: quality-aware allocation, `max_source_pct` cap, min/max per-source budgets, quality-tier sorting, quality label in headers |
| **`chunk_text()`** | Overlap-based sliding window | Paragraph-boundary-respecting chunking |
| **`_extract_html()`** | BS4 → `get_text()` (flat) | BS4 → structured extraction with h1-h6 → `##`, `li` → `- `, preserves semantic structure |
| **`_clean_markdown()`** | Strips HTML tags | Strips HTML tags + collapses whitespace |
| **`_extract_pdf()`** | Basic `page.get_text()` | **Enhanced**: page-number tracking `[Page N]`, artifact cleanup (page numbers, form-feeds, hyphenated line breaks), skips near-empty pages |
| **`_assess_quality()`** | 3 tiers: full/partial/stub | 4 tiers: full/partial/stub/**unusable** |
| **Quality thresholds** | Same constants | Same + `MIN_USEFUL_CHARS` warning |
| **`load_all_readable()`** | Loads everything | Skips PDFs when fitz unavailable |

**AMCIS improvements to backport** (ALL of these are generic/reusable):
1. ✅ **Quality-aware source context allocation** (`prepare_source_context`) — prevents a single 200K-char HTML from drowning out 20 other sources. This is the single most impactful improvement.
2. ✅ **Paragraph-boundary chunking** — much better than mid-sentence overlap cuts.
3. ✅ **Structured HTML extraction** — preserves headings/lists instead of flat text dump. Huge quality improvement for LLM prompts.
4. ✅ **Enhanced PDF extraction** — page tracking, artifact cleanup, hyphen fix.
5. ✅ **4-tier quality assessment** with `unusable` tier and warning message.

**Template has and AMCIS doesn't**:
1. ⚠️ **`HAS_BS4` graceful fallback** — good defensive coding, AMCIS should adopt.
2. ⚠️ **Skip-reason logging** in `load_sources()` — helpful for debugging.

---

### 1.4 `llm.py`

| Aspect | Template | AMCIS |
|--------|----------|-------|
| Lines | ~90 | ~100 |
| **`print_usage_summary()`** | Compact 1-line format | Detailed multi-line box with `=` borders |
| **Cost estimate** | `prompt * 0.4 + completion * 1.6` / 1M | `prompt * 1.0 + completion * 4.0` / 1M (blended for gpt-4.1 mix) |

**Verdict**: Nearly identical. Both have the same core functions: `get_client()`, `chat()`, `chat_json()`, `extract_json_from_text()`, `get_token_usage()`, `print_usage_summary()`.

**AMCIS improvements to backport**:
1. ✅ **More detailed `print_usage_summary()`** — the boxed format with separate lines is more readable in long pipeline runs.
2. The blended cost estimate is AMCIS-specific (depends on extraction vs synthesis model mix). Template version works fine.

---

### 1.5 `run_agents.py`

| Aspect | Template | AMCIS |
|--------|----------|-------|
| Lines | ~95 | ~125 |
| **Title** | Generic `"AGENTIC ANALYSIS PIPELINE"` | `"AMCIS 2026 — AGENTIC ANALYSIS PIPELINE v2"` |
| **Summary format** | `f"  {status:>6}  {name:<40}  ({dt:.1f}s)"` | Similar but with `[status]` brackets |
| **Enriched file listing** | ❌ None | ✅ Lists all output files with byte sizes at the end |

**AMCIS improvements to backport**:
1. ✅ **Enriched file listing at end** — useful to confirm all outputs were generated.

---

### 1.6 `step1_extract.py`

| Aspect | Template | AMCIS |
|--------|----------|-------|
| Lines | ~95 (skeleton) | **495** (fully implemented) |
| **`SYSTEM_PROMPT`** | Generic 6-line prompt | **60+ lines**: theoretical spine (DMC, Role Theory, Governance-as-Capability), McKinsey scaling constraints, evidence strength rubric with examples, discriminant validity guidance |
| **Extraction prompt** | Single simple prompt | **Two-phase approach**: (1) Extract evidence per construct, (2) Enrich definitions from evidence |
| **Construct definitions** | Placeholder `["Construct A", "Construct B", "Construct C"]` | 3 fully defined constructs with working definitions, dimensions, discriminant notes, relevant source lists |
| **Output formats** | Single JSON file | **3 outputs**: Markdown (human-readable), CSV (sub-competencies), JSON (evidence for downstream steps) |
| **Evidence rubric** | 3 strength levels mentioned | 3 levels with **detailed examples** and DISCARD guidance |
| **Negative evidence** | Not tracked | ✅ Explicitly required in prompt — sources with no findings must explain why |
| **Triangulation** | Not tracked | ✅ Source type classification passed to enrichment prompt |
| **Observable practices** | Not requested | ✅ Each sub-dimension requires 1-3 observable practices + candidate metrics |

**AMCIS improvements to backport** (generalizable):
1. ✅ **Two-phase extraction → enrichment pattern** — this is a much better architecture than single-shot. Phase 1 extracts raw evidence, Phase 2 synthesizes definitions. Domain-agnostic.
2. ✅ **Evidence strength rubric with examples** — the rubric is generic; only examples need updating.
3. ✅ **Negative evidence tracking** — forces the LLM to explain gaps, not just produce positive findings.
4. ✅ **Discriminant validity prompting** — preventing construct overlap.
5. ✅ **Triple output format** (MD + CSV + JSON) — the template should produce all three.
6. ✅ **Observable practices + candidate metrics** — great for operationalizability.
7. ✅ **Chain-of-thought in extraction prompt** — explicit step-by-step instructions.

**Template advantages**:
1. ✅ Clean `CUSTOMIZE` comments and placeholder pattern — easier onboarding.

---

### 1.7 `step2_crosswalk.py`

| Aspect | Template | AMCIS |
|--------|----------|-------|
| Lines | ~65 (skeleton) | **321** (fully implemented) |
| **Purpose** | Generic "cross-taxonomy mapping" | Full governance-requirement → architecture-control crosswalk with 42 requirements and 18 controls |
| **System prompt** | 3 generic rules | Detailed bundle classification criteria (Trust vs Integration), decision rules, confidence scoring guidelines |
| **Data structures** | None | `GOVERNANCE_REQUIREMENTS` (42 from NIST/EU/OWASP), `ARCH_CONTROLS` (18) |
| **Batching** | None — single call | Batched processing (10 reqs per call) to stay within token limits |
| **Output** | Single JSON | **3 outputs**: crosswalk matrix CSV, competency statements CSV, evidence JSON |
| **Competency statements** | Not generated | ✅ Natural academic prose statements with citation guidance and anti-template instructions |

**AMCIS improvements to backport** (generalizable):
1. ✅ **Batched processing pattern** — any crosswalk with many items needs this.
2. ✅ **Triple output format** (matrix CSV + statements CSV + evidence JSON).
3. ✅ **Bundle classification criteria in prompt** — the concept of classifying requirements into capability bundles is generic.
4. ✅ **Confidence scoring rubric** for mappings.
5. ✅ **Varied-prose guidance** in competency statement prompt ("Bad: ... Good: ...").

**AMCIS-specific** (don't backport):
- The 42 governance requirements are AMCIS-domain-specific
- The 18 architecture controls are AMCIS-domain-specific
- The Trust/Integration bundle split is research-specific

---

### 1.8 `step3_enrich.py`

| Aspect | Template | AMCIS |
|--------|----------|-------|
| Lines | ~45 (skeleton, does nothing) | **535** (MITRE ATLAS incident coding) |
| **Status** | Prints "not configured" | Full implementation: loads YAML adversarial incident data, codes by harm type, maps to sub-competencies, generates coverage maps |
| **LLM enrichment** | None | Batch-processed incident enrichment with detailed failure-mode rubric |
| **Output** | Empty JSON | **5 outputs**: incident coding CSV, tactic frequency CSV, mitigation gaps CSV, coverage map CSV + MD, enrichments JSON |

**AMCIS improvements to backport** (generalizable patterns):
1. ✅ **Batch-by-5 enrichment pattern** — smaller batches = better per-item reasoning.
2. ✅ **Detailed classification rubric in prompt** — the harm-type and failure-mode rubrics are excellent prompt engineering templates.
3. ✅ **Coverage map pattern** — validating that a framework covers real-world cases is generic.
4. ✅ **Merge-LLM-enrichments-into-rows pattern** — useful for any tabular enrichment task.
5. ✅ **Multiple output formats** for the same analysis.

**AMCIS-specific** (don't backport):
- MITRE ATLAS data loading, tactic/technique mappings, specific harm types

---

### 1.9 `step4_synthesize.py`

| Aspect | Template | AMCIS |
|--------|----------|-------|
| Lines | ~65 (skeleton) | **620** (fully implemented) |
| **Propositions** | None defined | 5 detailed proposition shells with theoretical lenses, mechanisms, roles |
| **Evidence integration** | Single prompt dumps all steps' output | **Computed statistics** from Steps 2/3 fed into per-proposition prompts |
| **Devil's advocate** | Not included | ✅ Required: counter-argument, weakest evidence, alternative explanation, boundary conditions |
| **Falsifiability** | Mentioned in output schema | ✅ Full falsifiability note required per proposition |
| **Fallback loading** | None | ✅ Can load from cached enriched files or original CSVs if step results not passed |
| **Output** | Single JSON | **3 outputs**: Markdown with ASCII conceptual model, CSV evidence table, JSON |

**AMCIS improvements to backport** (generalizable):
1. ✅ **Devil's advocate section** in proposition grounding — forces intellectual honesty.
2. ✅ **Computed statistics integration** — pulling real numbers from upstream steps instead of hoping the LLM remembers.
3. ✅ **Fallback data loading pattern** — `_load_step_data()` tries passed data → enriched file → original CSV.
4. ✅ **Per-proposition prompting** (not batch) — better quality per proposition.
5. ✅ **Citation discipline rules** — explicit "do NOT fabricate author/year" instructions.
6. ✅ **ASCII conceptual model in Markdown** output.

---

### 1.10 `step5_validate.py`

| Aspect | Template | AMCIS |
|--------|----------|-------|
| Lines | ~85 (skeleton) | **445** (fully implemented) |
| **Architecture** | Single LLM call | **3-phase**: automated citation check → LLM adversarial review → cross-step consistency |
| **Automated checks** | None | ✅ Regex-based citation validation (`[#XX]` matches valid source IDs) |
| **Cross-step checks** | None | ✅ Verifies that claimed requirement/incident counts match actual Step 2/3 data |
| **Deduplication** | None | ✅ Deduplicates issues by (proposition, category, description[:80]) |
| **Output** | Single JSON | **3 outputs**: Markdown report, issues CSV, full JSON |

**AMCIS improvements to backport** (ALL generalizable):
1. ✅ **3-phase validation architecture** — automated → LLM → consistency. This is excellent and fully generic.
2. ✅ **Automated citation regex checker** — any paper with corpus references benefits.
3. ✅ **Cross-step consistency checking** — verifying numbers match upstream data.
4. ✅ **Issue deduplication** — avoids repetitive findings.
5. ✅ **Severity/category classification** with counting.

---

### 1.11 `step6_writing_quality.py`

| Aspect | Template | AMCIS |
|--------|----------|-------|
| Lines | ~260 | ~400 |
| **Core readability functions** | Identical | Identical |
| **SYSTEM_PROMPT** | Generic IS conferences | Identical but slightly more detailed |
| **REVIEW_PROMPT** | Same structure, slightly shorter | Adds more guidance text |
| **OVERALL_PROMPT** | Same structure | AMCIS version uses `amcis_fit_assessment` vs template's `venue_fit_assessment` |
| **CUSTOMIZATION comments** | ✅ Present | ❌ Removed |

**Verdict**: Very similar. The template version is actually slightly better structured with CUSTOMIZE comments. AMCIS version adds minor elaborations.

**AMCIS improvements to backport**: Minimal. The template already captured this well.

---

### 1.12 `step7_ref_check.py`

| Aspect | Template | AMCIS |
|--------|----------|-------|
| Lines | ~140 (compact) | ~270 (expanded) |
| **Core logic** | Same | Same |
| **BibTeX entry types** | 4 types | 6 types (adds `online`, `techreport`, `report`) |
| **Invalid year check** | Not present | ✅ Regex check for valid year format |
| **Context check prompt** | Shorter, same structure | Longer, more detailed guidance |
| **Output fields** | Slightly different keys | More detailed summary dict keys |

**AMCIS improvements to backport**:
1. ✅ **Extra BibTeX entry types** (`online`, `techreport`, `report`) — very common.
2. ✅ **Year validation regex** — catches bad years like "forthcoming" or "n.d."

---

### 1.13 `step8_peer_review.py`

| Aspect | Template | AMCIS |
|--------|----------|-------|
| Lines | ~130 (compact) | ~260 (expanded) |
| **Reviewer personas** | 3 terse personas (~2 lines each) | 3 **detailed** personas (~15 lines each) with specific review priorities, publication record, personality |
| **META_REVIEW_PROMPT** | Same structure | Adds `risks_if_not_addressed` field |
| **Review prompt** | Same structure | Same |

**AMCIS improvements to backport**:
1. ✅ **Richer reviewer personas** — more detailed personas produce better simulated reviews. The template should include fuller personas even if generic.
2. ✅ **`risks_if_not_addressed` field** in meta-review.

---

## 2. Top-Level Scripts Comparison (`scripts/`)

### Template has (3 scripts):
| Script | Content |
|--------|---------|
| `00_profile_sources.py` | Skeleton — lists files in `data/raw/` |
| `01_prepare_datasets.py` | Skeleton — empty TODO |
| `02_generate_figures.py` | Skeleton with matplotlib defaults — empty TODO |

### AMCIS has (18 scripts + utility):
| Script | Purpose | Generalizable? |
|--------|---------|---------------|
| `00_profile_sources.py` | Profile literature sources | Likely customized |
| `01_cross_taxonomy_mapping.py` | Cross-taxonomy mapping | Domain-specific |
| `02_prepare_datasets.py` | Dataset preparation | Domain-specific |
| `03_generate_figures.py` | General figure generation | Partially |
| `04_profile_eo13960.py` | EO 13960 profiling | AMCIS-specific |
| `05_prepare_astalabs_discovery.py` | AstaLabs data prep | AMCIS-specific |
| `06_fetch_astalabs_experiments.py` | Fetch AstaLabs experiments | AMCIS-specific |
| `07_archive_astalabs_experiments.py` | Archive experiments | AMCIS-specific |
| `08_generate_paper_figures.py` | Publication figures | Domain-specific |
| `09_pathway_model.py` | Pathway analysis | AMCIS-specific |
| `10_ir_analysis.py` | Integration readiness analysis | AMCIS-specific |
| `11_mapping_sensitivity.py` | **Sensitivity analysis** | ✅ Partially generic |
| `12_procurement_confounding.py` | **Confounding check** | ✅ Pattern is generic |
| `13_aiid_coverage_robustness.py` | **Coverage robustness** | ✅ Pattern is generic |
| `14_atlas_threat_characterization.py` | ATLAS analysis | AMCIS-specific |
| `15_elaine_review_analyses.py` | Review response analyses | AMCIS-specific |
| `16_vendor_divergence_diagnostic.py` | Vendor diagnostic | AMCIS-specific |
| `17_table2_split_tr.py` | Table generation | AMCIS-specific |
| `local_readability_audit.py` | **Offline readability audit** | ✅ **FULLY generic** |
| `test_api.py` | API connectivity test | ✅ Likely generic |

**Scripts to backport to template**:
1. ✅ **`local_readability_audit.py`** — This is a zero-cost (no LLM) readability tool that reuses Step 6 functions. Identifies longest sentences, most jargon-dense sentences, per-section metrics. **Highly valuable for any paper project.**
2. ✅ **`test_api.py`** — utility script to test OpenAI connectivity.
3. Consider creating template versions of sensitivity analysis / robustness check patterns (scripts 11-13), even as skeletons.

---

## 3. `paper/` Folder Comparison

### Template:
```
paper/
├── apa.csl
├── header.tex          ← generic LaTeX preamble
├── paper.md            ← template with section placeholders
├── references.bib      ← empty
└── figures/
    └── .gitkeep
```

### AMCIS:
```
paper/
├── amcis-header.tex    ← AMCIS-specific LaTeX header
├── apa.csl
├── paper.md            ← full manuscript
├── paper_review.md     ← review response document
├── references.bib      ← populated bibliography
├── amcis.pdf           ← compiled output
├── paper v2.pdf, v3.pdf, v4.pdf  ← version history
├── paper-review.docx/pdf         ← review artifacts
├── figures/
└── master-copy/
```

**Observations**:
- Template uses `header.tex`; AMCIS uses `amcis-header.tex` — the template naming is more generic, which is correct.
- AMCIS has `paper_review.md` — a review response document pattern that could be templated.
- AMCIS has `master-copy/` — for archiving submitted versions.

**Backport recommendations**:
1. ✅ Add a `paper_review.md` template (empty review-response scaffold).
2. Consider adding a `master-copy/` directory with `.gitkeep`.

---

## 4. `requirements.txt` Comparison

### Template:
```
pandas>=2.1
pyyaml>=6.0
numpy>=1.24
matplotlib>=3.7
seaborn>=0.13
statsmodels>=0.14
scipy>=1.11
beautifulsoup4>=4.12
pymupdf>=1.23
openai>=1.0
langchain-openai>=0.3
python-dotenv>=1.0
```

### AMCIS:
```
pandas>=2.1
pyyaml>=6.0
numpy>=1.24
matplotlib>=3.7
statsmodels>=0.14
openai>=1.0
langchain-openai>=0.3
```

**Differences**:
| Package | Template | AMCIS | Note |
|---------|----------|-------|------|
| `seaborn>=0.13` | ✅ | ❌ | Template has it |
| `scipy>=1.11` | ✅ | ❌ | Template has it |
| `beautifulsoup4>=4.12` | ✅ | ❌ | AMCIS uses it but doesn't list it! |
| `pymupdf>=1.23` | ✅ | ❌ | AMCIS uses it but doesn't list it! |
| `python-dotenv>=1.0` | ✅ | ❌ | Template loads .env; AMCIS doesn't |

**Issues**:
1. ⚠️ **AMCIS is missing `beautifulsoup4` and `pymupdf`** from requirements.txt despite importing them in `literature_loader.py`.
2. ⚠️ **AMCIS is missing `python-dotenv`** — should either add it or add `load_dotenv()` to config.py.
3. Template requirements.txt is **more complete** — this is correct.

---

## 5. `.env.example` and `illustrator/`

### `.env.example`
- **Template**: ✅ Has `.env.example` with `OPENAI_API_KEY`, optional `GOOGLE_API_KEY`, `ANTHROPIC_API_KEY`, model overrides.
- **AMCIS**: ❌ Has no `.env.example`. Config.py uses `os.environ.get()` directly.

**Backport**: AMCIS should adopt `.env.example` + `python-dotenv` pattern from template.

### `illustrator/`
- **Template**: ✅ Full `illustrator/` directory with PaperBanana-based multi-agent figure generation (planner → visualizer → critic loop). Supports OpenAI, Claude, Gemini. Has Streamlit demo.
- **AMCIS**: Has `PaperBanana/` at root level (appears to be the source fork), but does NOT have the cleaned-up `illustrator/` integration that the template provides.

**Analysis**: The template's `illustrator/` is a cleaned-up, documented integration of PaperBanana. AMCIS has the raw PaperBanana fork. No backport needed — the template already has the better version.

### `chatgpt_package/`
- **Template**: `PROMPT.md` + `HANDOFF.md` — clean LLM handoff package.
- **AMCIS**: `optionA_paper_package/` with `PROMPT_FOR_CHATGPT.md` + `README_PACKAGE.md` — similar concept, different naming.

**Backport**: Template naming is cleaner. No content to backport.

---

## 6. Priority Backport Recommendations

### P0 — Critical (backport immediately)

| # | Item | Source File | Impact |
|---|------|-------------|--------|
| 1 | **Quality-aware source context allocation** | `literature_loader.py` → `prepare_source_context()` | Prevents large docs from drowning out small ones. Affects ALL pipeline quality. |
| 2 | **Two-phase extract→enrich architecture** | `step1_extract.py` | Fundamental improvement to evidence extraction quality. |
| 3 | **3-phase validation** (auto + LLM + consistency) | `step5_validate.py` | Much more robust than single-LLM-call validation. |
| 4 | **`local_readability_audit.py`** | New file | Zero-cost offline tool. Immediately useful for any paper. |

### P1 — High Priority

| # | Item | Source File | Impact |
|---|------|-------------|--------|
| 5 | **Structured HTML extraction** (headings/lists) | `literature_loader.py` → `_extract_html()` | Huge quality improvement for LLM context windows. |
| 6 | **Enhanced PDF extraction** with page tracking | `literature_loader.py` → `_extract_pdf()` | Better citation traceability. |
| 7 | **Paragraph-boundary chunking** | `literature_loader.py` → `chunk_text()` | Better than mid-sentence cuts. |
| 8 | **Devil's advocate in propositions** | `step4_synthesize.py` | Forces intellectual honesty. Generic pattern. |
| 9 | **Automated citation regex checker** | `step5_validate.py` → `_automated_citation_check()` | Generic — works for any `[#XX]` citation scheme. |
| 10 | **Cross-step consistency checks** | `step5_validate.py` → `_cross_step_consistency()` | Generic pattern for multi-step pipelines. |
| 11 | **Batched processing pattern** | `step2_crosswalk.py`, `step3_enrich.py` | Needed for any pipeline with many items. |

### P2 — Medium Priority

| # | Item | Source File | Impact |
|---|------|-------------|--------|
| 12 | **Triple output format** (MD + CSV + JSON) | All step files | Better usability for different consumers. |
| 13 | **Negative evidence tracking** | `step1_extract.py` | Better prompt engineering pattern. |
| 14 | **Richer reviewer personas** | `step8_peer_review.py` | Better-quality simulated reviews. |
| 15 | **Extra BibTeX types + year validation** | `step7_ref_check.py` | Small but useful improvements. |
| 16 | **Coverage map pattern** | `step3_enrich.py` → `_write_coverage_map()` | Useful framework validation approach. |
| 17 | **Fallback data loading** (`_load_step_data`) | `step4_synthesize.py`, `step5_validate.py` | Robust loading from file when step results not passed. |

### P3 — Nice to Have

| # | Item | Source File | Impact |
|---|------|-------------|--------|
| 18 | **Enriched file listing** in run_agents.py | `run_agents.py` | Convenience. |
| 19 | **`paper_review.md` template** | `paper/` | Review response scaffold. |
| 20 | **`HAS_BS4` graceful fallback** | Back-port from template to AMCIS | Defensive coding. |

---

## 7. AMCIS Project — Missing from Template (unique value)

These AMCIS-only files don't exist in the template and represent unique research value:

| File | Unique Value |
|------|-------------|
| `scripts/09_pathway_model.py` | Pathway/process model analysis |
| `scripts/10_ir_analysis.py` | Integration readiness analysis |
| `scripts/11_mapping_sensitivity.py` | Sensitivity analysis for taxonomy mappings |
| `scripts/12_procurement_confounding.py` | Confounding variable analysis |
| `scripts/13_aiid_coverage_robustness.py` | Coverage robustness checking |
| `scripts/14_atlas_threat_characterization.py` | MITRE ATLAS threat characterization |
| `scripts/15_elaine_review_analyses.py` | Reviewer response analyses |
| `scripts/16_vendor_divergence_diagnostic.py` | Vendor divergence checking |
| `scripts/17_table2_split_tr.py` | Table generation for split Trust/Integration |
| `data/astalabs*/` | AstaLabs experimental data |
| `data/raw/atlas/` | MITRE ATLAS YAML dataset |
| `literature/` (34 files) | Full literature corpus |

The **robustness/sensitivity scripts (11-13)** contain patterns that could be generalized into template skeletons for any quantitative IS paper.

---

## 8. Summary Statistics

| Metric | Template | AMCIS | Ratio |
|--------|----------|-------|-------|
| Agent files total LOC | ~1,050 | ~4,300 | 4.1× |
| Top-level scripts | 3 (skeletons) | 18 + 2 utilities | 6.7× |
| Literature sources configured | 0 | 34 | — |
| Governance requirements | 0 | 42 | — |
| Output formats per step | JSON only | MD + CSV + JSON | 3× |
| requirements.txt packages | 11 | 7 (incomplete!) | — |

**Bottom line**: The template is a well-structured skeleton. The AMCIS project is a fully-realized research pipeline with ~4× the code. The majority of AMCIS improvements are in **prompt engineering quality**, **multi-phase architectures**, and **multi-format outputs** — all of which are generalizable and should be backported.
