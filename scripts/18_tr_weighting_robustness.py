"""
18_tr_weighting_robustness.py
Robustness check requested by AMCIS reviewers (Minitrack Chair / R1, "Construct Measurement"):
re-estimate the M3 and M4 logistic-regression specifications using alternative
weighting schemes for the TR index, and confirm the suppression-effect signature
(TR-surface positive, TR-substantive negative) is preserved.

Schemes:
    (a) Equal weights              -- baseline reported in the paper
    (b) PCA-1 weights              -- loadings on the first principal component
                                       of the 9 TR items (separately for surface/subst.)
    (c) Inverse-prevalence weights -- rare safeguards weighted higher

Output: console summary + sign/significance comparison vs. baseline.
"""
from __future__ import annotations
import importlib.util, pathlib, warnings
import numpy as np, pandas as pd, statsmodels.api as sm
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
BASE = pathlib.Path(__file__).resolve().parent

# Reuse the dataset builder from 17_table2_split_tr.py
spec = importlib.util.spec_from_file_location("split_tr", BASE/"17_table2_split_tr.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

TR_SURF = ["tr_ato","tr_internal_rev"]
TR_SUBST = ["tr_impact_assess","tr_rw_testing","tr_indep_eval","tr_postdeploy",
            "tr_notice","tr_disparity","tr_appeal"]
TR_ALL = TR_SURF + TR_SUBST

def pca_weights(df, items):
    X = StandardScaler().fit_transform(df[items].astype(float).values)
    pca = PCA(n_components=1).fit(X)
    w = np.abs(pca.components_[0])
    w = w / w.sum() * len(items)            # rescale so equal-weights == 1 each
    return dict(zip(items, w)), pca.explained_variance_ratio_[0]

def inv_prev_weights(df, items):
    p = df[items].mean()
    w = 1.0 / p.replace(0, np.nan)
    w = (w / w.sum() * len(items)).fillna(0)
    return w.to_dict()

def weighted_sum(df, items, weights):
    return sum(df[i].astype(float) * weights[i] for i in items)

def fit(df, cols, label):
    y = df["deployed"]
    X = sm.add_constant(df[cols].astype(float))
    m = sm.Logit(y, X).fit(disp=0, maxiter=200)
    print(f"\n--- {label} | N={len(y)} | Pseudo R²={m.prsquared:.3f} | AIC={m.aic:.1f} ---")
    for v in cols:
        b, se, p = m.params[v], m.bse[v], m.pvalues[v]
        stars = "***" if p<0.001 else "**" if p<0.01 else "*" if p<0.05 else "+" if p<0.1 else " "
        print(f"  {v:<18s} b={b:+.3f}  SE={se:.3f}  p={p:.4f}{stars}  OR={np.exp(b):.3f}")
    return m

def main():
    df = mod.build()

    # Baseline weights
    eq_all = {i:1.0 for i in TR_ALL}
    eq_surf = {i:1.0 for i in TR_SURF}
    eq_subst = {i:1.0 for i in TR_SUBST}

    # PCA weights
    w_pca_all, evr_all = pca_weights(df, TR_ALL)
    w_pca_surf, evr_surf = pca_weights(df, TR_SURF)
    w_pca_subst, evr_subst = pca_weights(df, TR_SUBST)
    print(f"\nPCA-1 explained variance: TR_all={evr_all:.2f}, TR_surface={evr_surf:.2f}, TR_substantive={evr_subst:.2f}")
    print("PCA weights (TR-all):")
    for k,v in w_pca_all.items(): print(f"  {k:<18s} {v:.3f}")

    # Inverse-prevalence weights
    w_inv_all  = inv_prev_weights(df, TR_ALL)
    w_inv_surf = inv_prev_weights(df, TR_SURF)
    w_inv_subst= inv_prev_weights(df, TR_SUBST)

    schemes = {
        "equal (baseline)":   (eq_all,  eq_surf,  eq_subst),
        "PCA-1":              (w_pca_all, w_pca_surf, w_pca_subst),
        "inverse-prevalence": (w_inv_all, w_inv_surf, w_inv_subst),
    }

    base_cols = ["vendor","mixed_dev","rights_safety","orientation"]
    print("\n" + "="*72)
    print("M3 (composite TR) under alternative weighting schemes")
    print("="*72)
    for name,(wa,_,_) in schemes.items():
        df["TR_w"] = weighted_sum(df, TR_ALL, wa)
        fit(df, base_cols+["TR_w","IR"], f"M3 / {name}")

    print("\n" + "="*72)
    print("M4 (split TR) under alternative weighting schemes")
    print("="*72)
    for name,(_,ws,wb) in schemes.items():
        df["TR_surf_w"] = weighted_sum(df, TR_SURF, ws)
        df["TR_subst_w"] = weighted_sum(df, TR_SUBST, wb)
        fit(df, base_cols+["TR_surf_w","TR_subst_w","IR"], f"M4 / {name}")

    print("\nDone. Compare signs/significance of TR_surf_w (>0) and TR_subst_w (<0) across schemes.")

if __name__ == "__main__":
    main()
