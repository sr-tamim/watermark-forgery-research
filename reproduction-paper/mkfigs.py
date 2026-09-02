import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np, pandas as pd, json

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"],
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8.5,
    "legend.fontsize": 7, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 400, "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
})
U = "/mnt/user-data/uploads/"
df = pd.read_csv(U+"phase0_scores.csv"); df["c"] = df.lambd - df.x
TAU = 0.0261008646426459
COL = {"clean": "#8c8c8c", "forged": "#c8632a", "genuine": "#2f6f4e"}
ORD = ["clean", "forged", "genuine"]

# ---------- Fig 1: attack pipeline ----------
fig, ax = plt.subplots(figsize=(7.0, 2.5))
ax.set_xlim(0, 100); ax.set_ylim(-1, 33); ax.axis("off")

def box(x, y, w, h, txt, fc, ec, fs=7.2, bold=False):
    ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.35,rounding_size=0.8",
                                   fc=fc, ec=ec, lw=0.9))
    ax.text(x+w/2, y+h/2, txt, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", linespacing=1.4)

def arrow(x1, y1, x2, y2, txt=None, dy=1.0, ha="center"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#333", shrinkA=0, shrinkB=0))
    if txt:
        ax.text((x1+x2)/2, (y1+y2)/2+dy, txt, ha=ha, va="bottom", fontsize=6.5, color="#333")

ax.text(0, 31.5, "Defender  (holds key $k$)", fontsize=7.2, style="italic", color="#2f6f4e")
box(0,  20, 18, 8, "watermarked\nlatent $z_T^{(w)}$", "#eaf3ee", "#2f6f4e")
box(27, 20, 15, 8, "target $u_T$\nSDXL", "#eaf3ee", "#2f6f4e")
box(51, 20, 16, 8, "reference\nimage $x^{(g)}$", "#eaf3ee", "#2f6f4e")
arrow(18, 24, 27, 24)
arrow(42, 24, 51, 24, "generate")

ax.text(22, 10.6, "Attacker  (no key, no target weights)", fontsize=7.2, style="italic", color="#c8632a")
box(0,  1, 18, 8, "proxy $u_A$\nSD 2.1", "#fbeee6", "#c8632a")
box(27, 1, 15, 8, "recovered\n$\\hat{z}_T^{(w)}$", "#fbeee6", "#c8632a")
box(51, 1, 16, 8, "forged\nimage $x^{(f)}$", "#fbeee6", "#c8632a")
arrow(18, 5, 27, 5)
arrow(42, 5, 51, 5, "reprompt $q_A$")

# reference image feeds the attacker's inversion
ax.annotate("", xy=(9, 9.6), xytext=(56, 20),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#333",
                            connectionstyle="arc3,rad=0.16", shrinkA=0, shrinkB=0))
ax.text(40, 16.4, "invert in the proxy model", fontsize=6.5, color="#333",
        ha="center", style="italic")

box(80, 10.5, 19, 9, "detector\n$\\mathcal{D}(\\cdot\\,;k)$", "#f2f2f2", "#444", bold=True)
ax.annotate("", xy=(89.5, 19.5), xytext=(67, 24),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#2f6f4e", shrinkA=0, shrinkB=0))
ax.annotate("", xy=(89.5, 10.5), xytext=(67, 5),
            arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#c8632a", shrinkA=0, shrinkB=0))
ax.text(78, 23.6, "accepted", fontsize=6.5, color="#2f6f4e", ha="right")
ax.text(78, 8.4, "also accepted", fontsize=6.5, color="#c8632a", ha="right")
plt.savefig("figures/fig1_pipeline.png")
plt.close()

# ---------- Fig 2: G1 memory ----------
g1 = json.load(open(U+"gate1.json"))
fig, ax = plt.subplots(figsize=(3.3, 2.0))
labs = ["SD 2.1\nfp32", "SDXL\nfp16", "SDXL\nfp32"]
vals = [g1["attacker_fp32"]["peak_gb"], g1["target_fp16"]["peak_gb"], g1["target_fp32"]["peak_gb"]]
cols = ["#c8632a", "#2f6f4e", "#8c8c8c"]
b = ax.bar(labs, vals, color=cols, width=0.58, zorder=3)
ax.axhline(14.6, color="#b00", lw=1.0, ls="--", zorder=4)
ax.text(2.42, 14.9, "T4 capacity 14.6 GB", fontsize=6.6, color="#b00", ha="right")
for r, v in zip(b, vals):
    ax.text(r.get_x()+r.get_width()/2, v+0.3, f"{v:.2f}", ha="center", fontsize=7)
ax.set_ylabel("peak allocated (GB)"); ax.set_ylim(0, 17)
ax.grid(axis="y", lw=0.4, color="#ddd", zorder=0)
plt.savefig("figures/fig2_memory.png"); plt.close()

# ---------- Fig 3: per-arm statistic ----------
fig, ax = plt.subplots(figsize=(3.3, 2.3))
rng = np.random.default_rng(0)
for i, h in enumerate(ORD):
    s = df[df.hypothesis == h]
    ax.scatter(np.full(len(s), i) + rng.uniform(-.09, .09, len(s)), s.x,
               s=26, color=COL[h], alpha=.85, zorder=3, edgecolor="white", lw=.5)
    ax.hlines(s.x.mean(), i-.26, i+.26, color=COL[h], lw=1.6, zorder=4)
miss = df[(df.hypothesis == "forged") & (~df.detected)]
ax.scatter(miss.index*0+1, miss.x, s=90, facecolor="none", edgecolor="#b00", lw=1.1, zorder=5)
ax.annotate("undetected\nforgery", xy=(1.1, float(miss.x.iloc[0])), xytext=(1.42, 1690),
            fontsize=6.4, color="#b00", ha="center",
            arrowprops=dict(arrowstyle="-", lw=.7, color="#b00"))
ax.set_xticks(range(3)); ax.set_xticklabels(ORD)
ax.set_ylabel("$x$  (lower $=$ closer to key)")
ax.grid(axis="y", lw=.4, color="#eee", zorder=0)
plt.savefig("figures/fig3_statistic.png"); plt.close()

# ---------- Fig 4: ROC for the two scores ----------
def roc(pos, neg):
    th = np.sort(np.unique(np.concatenate([pos, neg])))[::-1]
    tpr = [np.mean(pos >= t) for t in th]; fpr = [np.mean(neg >= t) for t in th]
    return [0]+fpr+[1], [0]+tpr+[1]
def auc(p, n):
    p, n = np.asarray(p), np.asarray(n)
    return ((p[:, None] > n[None, :]).sum() + .5*(p[:, None] == n[None, :]).sum())/(len(p)*len(n))

nul = df[df.hypothesis == "clean"]; fo = df[df.hypothesis == "forged"]
fig, ax = plt.subplots(figsize=(3.3, 2.3))
for score, lab, c, ls in ((-df.x, r"$-x$", "#8c8c8c", "--"), (df.c, r"$\lambda-x$", "#c8632a", "-")):
    p = score[df.hypothesis == "forged"].to_numpy(); n = score[df.hypothesis == "clean"].to_numpy()
    f, t = roc(p, n)
    ax.plot(f, t, ls, color=c, lw=1.5, label=f"{lab}   AUC {auc(p,n):.3f}")
ax.plot([0, 1], [0, 1], lw=.7, color="#ccc")
ax.set_xlabel("false positive rate"); ax.set_ylabel("true positive rate")
ax.set_title("forged vs. clean", fontsize=8)
ax.legend(loc="lower right", frameon=False)
plt.savefig("figures/fig4_roc.png"); plt.close()

# ---------- Fig 5: p-values on log scale ----------
fig, ax = plt.subplots(figsize=(3.3, 2.3))
for i, h in enumerate(ORD):
    s = df[df.hypothesis == h]
    ax.scatter(np.full(len(s), i) + rng.uniform(-.09, .09, len(s)), s.p_value,
               s=26, color=COL[h], alpha=.85, zorder=3, edgecolor="white", lw=.5)
ax.axhline(TAU, color="#b00", lw=1.0, ls="--", zorder=4)
ax.text(2.45, TAU*2.2, r"$\tau = 0.0261$", fontsize=6.6, color="#b00", ha="right")
ax.set_yscale("log"); ax.set_ylim(1e-40, 20)
ax.set_xticks(range(3)); ax.set_xticklabels(ORD)
ax.set_ylabel("detector $p$-value")
ax.grid(axis="y", lw=.4, color="#eee", zorder=0)
plt.savefig("figures/fig5_pvalues.png"); plt.close()
print("figures written")
