#!/usr/bin/env python3
"""
stat_analysis.py - post-hoc statistical analysis of Phase 0 scores

Reads phase0_scores.csv and computes:
  - bootstrap 95% CIs for AUC (forged vs clean, genuine vs clean)
  - Mann-Whitney U tests between each pair of arms
  - Cohen's d effect sizes
  - Wilson score intervals for detection proportions
  - the numbers quoted in the paper's "Hypothesis tests" paragraph

Run from the experiments/28Aug2026_run1/ directory:
    python stat_analysis.py

Output: stats_report.txt (printed to stdout), fig6_distributions.png

Taslimul Hasan Toufique, 2026
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
import json, sys


def bootstrap_auc(pos, neg, n_boot=5000, seed=42):
    """
    bootstrap CI for Mann-Whitney AUC (same as rank-biserial).
    returns (point estimate, lo, hi) for 95% CI.
    """
    rng = np.random.default_rng(seed)
    pos, neg = np.asarray(pos), np.asarray(neg)
    def _auc(p, n):
        return float(((p[:, None] > n[None, :]).sum()
                      + 0.5 * (p[:, None] == n[None, :]).sum()) / (len(p) * len(n)))
    point = _auc(pos, neg)
    boots = np.empty(n_boot)
    for b in range(n_boot):
        bp = rng.choice(pos, len(pos), replace=True)
        bn = rng.choice(neg, len(neg), replace=True)
        boots[b] = _auc(bp, bn)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return point, lo, hi


def wilson_ci(k, n, z=1.96):
    """Wilson score interval for a proportion k/n at 95%."""
    phat = k / n
    denom = 1 + z**2 / n
    centre = (phat + z**2 / (2*n)) / denom
    margin = z * np.sqrt((phat*(1-phat) + z**2/(4*n)) / n) / denom
    return centre - margin, centre + margin


def cohens_d(a, b):
    """pooled Cohen's d, positive means a > b."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = len(a), len(b)
    var_a, var_b = a.var(ddof=1), b.var(ddof=1)
    pooled = np.sqrt(((na-1)*var_a + (nb-1)*var_b) / (na+nb-2))
    if pooled == 0:
        return 0.0
    return (a.mean() - b.mean()) / pooled

def main():
    csv_path = "phase0_scores.csv"
    df = pd.read_csv(csv_path)
    df["neg_x"] = -df["x"]       # lower x = stronger watermark evidence
    df["lam_x"] = df["lambd"] - df["x"]  # adjusted score

    genuine = df[df.hypothesis == "genuine"]
    clean   = df[df.hypothesis == "clean"]
    forged  = df[df.hypothesis == "forged"]
    n = len(df)

    out_lines = []
    def pr(s=""):
        out_lines.append(s)

    pr("=" * 62)
    pr("  Phase 0 Statistical Analysis")
    pr("  Forging Tree-Ring reproduction study")
    pr("=" * 62)
    pr()

    # --- detection proportions + Wilson CI ---
    pr("Detection proportions (Wilson 95% CI)")
    pr("-" * 48)
    for name, sub in [("genuine", genuine), ("clean", clean), ("forged", forged)]:
        k = sub["detected"].sum()
        nn = len(sub)
        lo, hi = wilson_ci(k, nn)
        pr(f"  {name:<10}  {k}/{nn} = {k/nn:.4f}   "
           f"CI [{lo:.4f}, {hi:.4f}]")
    pr()

    # --- bootstrap AUC ---
    pr("Bootstrap AUC (forged vs clean), 5000 resamples, 95% CI")
    pr("-" * 48)
    for score_name, col in [("-x (raw)", "neg_x"), ("lambda-x (adjusted)", "lam_x")]:
        auc_pt, lo, hi = bootstrap_auc(forged[col], clean[col])
        pr(f"  {score_name:<24}  AUC = {auc_pt:.4f}   CI [{lo:.4f}, {hi:.4f}]")

    pr()
    pr("Bootstrap AUC (genuine vs clean), 5000 resamples, 95% CI")
    pr("-" * 48)
    for score_name, col in [("-x (raw)", "neg_x"), ("lambda-x (adjusted)", "lam_x")]:
        auc_pt, lo, hi = bootstrap_auc(genuine[col], clean[col])
        pr(f"  {score_name:<24}  AUC = {auc_pt:.4f}   CI [{lo:.4f}, {hi:.4f}]")
    pr()

    # --- Mann-Whitney U tests ---
    pr("Mann-Whitney U tests (two-sided)")
    pr("-" * 48)
    pairs = [("genuine", genuine, "clean", clean),
             ("genuine", genuine, "forged", forged),
             ("forged", forged, "clean", clean)]
    for n1, s1, n2, s2 in pairs:
        u, pval = stats.mannwhitneyu(s1["neg_x"], s2["neg_x"], alternative="two-sided")
        d = cohens_d(s1["x"], s2["x"])
        pr(f"  {n1} vs {n2}  (raw -x):  U = {u:.1f},  p = {pval:.4e},  d = {d:.3f}")
    pr()

    # --- descriptive stats per arm (mirrors the paper's per-arm table) ---
    pr("Per-arm descriptive statistics")
    pr("-" * 48)
    pr(f"  {'Arm':<10} {'mean x':>10} {'median x':>10} {'sd x':>10} "
       f"{'mean p':>12} {'median p':>12}")
    for name, sub in [("genuine", genuine), ("clean", clean), ("forged", forged)]:
        pr(f"  {name:<10} {sub['x'].mean():>10.1f} {sub['x'].median():>10.1f} "
           f"{sub['x'].std():>10.2f} {sub['p_value'].mean():>12.2e} "
           f"{sub['p_value'].median():>12.2e}")
    pr()

    # --- missed forgery detail ---
    missed = forged[~forged["detected"]]
    if len(missed) > 0:
        pr("Missed forgery (inside clean range)")
        pr("-" * 48)
        cr_lo, cr_hi = clean["x"].min(), clean["x"].max()
        for _, row in missed.iterrows():
            pr(f"  trial {int(row['trial'])}: x = {row['x']:.1f}, "
               f"p = {row['p_value']:.4e}")
            pr(f"  clean range: [{cr_lo:.1f}, {cr_hi:.1f}]")
            pr(f"  position within clean range: "
               f"{(row['x'] - cr_lo) / (cr_hi - cr_lo) * 100:.1f}%")
    pr()

    # --- write report ---
    report = "\n".join(out_lines)
    print(report)
    with open("stats_report.txt", "w") as f:
        f.write(report)
    print(f"\n[written to stats_report.txt]")

    # --- generate Figure 6: box + strip plots ---
    make_boxplot(df)


def make_boxplot(df):
    """
    Box + strip plots of the raw statistic x and adjusted score lambda-x,
    split by arm. This is Fig 6 in the paper.
    """
    plt.rcParams.update({
        "font.family": "serif", "font.serif": ["DejaVu Serif"],
        "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8.5,
        "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "figure.dpi": 400, "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
    })

    COL = {"clean": "#8c8c8c", "forged": "#c8632a", "genuine": "#2f6f4e"}
    ORD = ["clean", "forged", "genuine"]

    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.6))

    for ax, col, label in zip(axes,
                               ["x", "lambd"],
                               [r"$x$  (raw statistic)",
                                r"$\lambda - x$  (adjusted)"]):
        data = [df[df.hypothesis == h][col].values for h in ORD]

        # boxplot
        bp = ax.boxplot(data, widths=0.45, patch_artist=True,
                        medianprops=dict(color="black", lw=1.2),
                        whiskerprops=dict(lw=0.8), capprops=dict(lw=0.8),
                        flierprops=dict(marker="none"))

        for patch, h in zip(bp["boxes"], ORD):
            patch.set_facecolor(COL[h])
            patch.set_alpha(0.35)
            patch.set_edgecolor(COL[h])

        # strip (jitter) on top
        rng = np.random.default_rng(7)
        for i, h in enumerate(ORD):
            vals = df[df.hypothesis == h][col].values
            jit = rng.uniform(-0.08, 0.08, len(vals))
            ax.scatter(np.full(len(vals), i+1) + jit, vals,
                       s=24, color=COL[h], alpha=0.85, zorder=3,
                       edgecolor="white", linewidth=0.5)

        ax.set_xticks(range(1, 4))
        ax.set_xticklabels(ORD)
        ax.set_ylabel(label)
        ax.grid(axis="y", lw=0.4, color="#eee", zorder=0)

    plt.tight_layout()
    plt.savefig("fig6_distributions.png", dpi=400)
    plt.close()
    print("[saved fig6_distributions.png]")


if __name__ == "__main__":
    main()
