# Governance Readiness Gaps in Organizational AI Deployment

**A Triangulated Analysis of Threats, Incidents, and Practice**

AMCIS 2026 Full Paper · Carlos Denner dos Santos & Elaine Mosconi · Université de Sherbrooke

📄 Paper: [`paper/AMCIS2026_Santos&Mosconi_GovernanceReadiness.pdf`](paper/AMCIS2026_Santos&Mosconi_GovernanceReadiness.pdf)
📘 Replication details: [REPLICATION.md](REPLICATION.md)

---

## Summary

We triangulate three public datasets — MITRE ATLAS (52 adversarial case studies), the AI Incident Database (1,362 incidents), and the EO 13960 Federal AI Use Case Inventory (1,757 deployments × 38 agencies) — to characterize the gap between formal AI governance adoption and substantive implementation. Two capability bundles (Trust Readiness and Integration Readiness) are operationalized from the EO 13960 fields and used to test a pathway model of operational deployment.

**Key findings**

- **Governance theater**: 60.7% of federal AI systems report internal review, but substantive safeguards (impact assessment, independent evaluation, bias mitigation) cluster at 5–9%.
- **Risk-tiering does not rescue depth**: theater rates *rise* from 53.9% (non-flagged) to 63.0% (rights/safety-impacting).
- **Suppression effect**: TR-surface facilitates deployment (OR=1.39, p<0.01) while TR-substantive dampens it (OR=0.92, p<0.05); IR is the dominant predictor (OR=1.25, p<0.001).
- **Evaluability constraints**: vendor-supplied systems are roughly half as likely to report impact assessment (OR=0.43, p=0.002, robust to agency fixed effects).

## Reproducing the Analysis

```bash
git clone https://github.com/<your-fork>/governance-readiness
cd governance-readiness
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

All three raw datasets are bundled under `data/raw/` (MITRE ATLAS, AIID snapshot, EO 13960 inventory). To refresh from upstream sources, run `python scripts/download_data.py`.

Then run, in order:

```bash
python scripts/01_cross_taxonomy_mapping.py     # cross-taxonomy bridging table
python scripts/02_prepare_datasets.py           # analysis-ready CSVs
python scripts/09_pathway_model.py              # nested logistic regressions (Table 2)
python scripts/17_table2_split_tr.py            # split-TR suppression model
python scripts/18_tr_weighting_robustness.py    # TR weighting robustness (PCA, inv-prevalence)
python scripts/12_procurement_confounding.py    # vendor / evaluability analyses
python scripts/13_aiid_coverage_robustness.py   # sector-harm fingerprints
python scripts/03_generate_figures.py           # figures 2–4
```

See [REPLICATION.md](REPLICATION.md) for the full script catalog, construct operationalization, robustness checks, and the Bayesian exploratory protocol.

## Repository Layout

```
README.md                  # this file
REPLICATION.md             # full replication documentation
requirements.txt
data/
  raw/                     # immutable source data (do not edit)
  processed/               # regenerable analysis artefacts
scripts/                   # numbered, runnable analysis pipeline
paper/
  AMCIS2026_Santos&Mosconi_GovernanceReadiness.pdf
```

## Citation

```bibtex
@inproceedings{santos2026governance,
  author    = {Santos, Carlos Denner and Mosconi, Elaine},
  title     = {Governance Readiness Gaps in Organizational {AI} Deployment:
               A Triangulated Analysis of Threats, Incidents, and Practice},
  booktitle = {Proceedings of the Americas Conference on Information Systems (AMCIS 2026)},
  year      = {2026}
}
```

## License

Code: MIT (see `LICENSE`). Data: governed by the licences of the original sources (MITRE ATLAS — Apache 2.0; AIID — CC BY-SA 4.0; EO 13960 — public domain).
