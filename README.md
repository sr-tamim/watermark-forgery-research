# Forging Tree-Ring — paper source

```
main.tex                   everything: preamble + all sections
refs.bib                   21 entries, all 21 cited in the text
mkfigs.py                  regenerates all five figures
figures/fig1_pipeline.png  attack flow diagram
figures/fig2_memory.png    G1 peak memory
figures/fig3_statistic.png per-arm x, missed forgery circled
figures/fig4_roc.png       ROC, -x vs lambda-x
figures/fig5_pvalues.png   p-values vs threshold
main.pdf                   compiled output, 9 pages
```

## Where the figures come from
Nothing is copied, traced, or downloaded. `mkfigs.py` draws all five with
matplotlib and writes them as PNG; `main.tex` pulls them in with
`\includegraphics` from `figures/`.

- Fig. 1 is drawn from scratch using matplotlib boxes and arrows. No external
  image, no template, not adapted from Muller et al.
- Figs. 2-5 are plotted directly from your run artifacts: `gate1.json` for the
  memory bars, `phase0_scores.csv` for the statistic, ROC and p-value plots.

Edit the numbers in the artifacts, rerun `python3 mkfigs.py`, and the figures
update. The paths at the top of `mkfigs.py` point at `/mnt/user-data/uploads/`;
change `U = ...` to wherever your JSON and CSV live.

Build: `latexmk -pdf main.tex`. 9 pages, 0 undefined references.
Overleaf: upload all, keep `figures/` a folder, compiler pdfLaTeX.

## Run used
Session `2026-08-28T05:28:33`, repo commit `7f9e7ad`, upstream base `ca68950`,
lock SHA `5592c786`. Artifacts: `gate1.json`, `gate3.json`, `gate4.json`,
`gate4` figures, `timings.json`, `precision_probe.json`, `phase0_scores.csv`,
`phase0_verdict.json`. Notebook: `research2-reproduction-paper.ipynb`.
Reprompt wall-clock is 332.0 s.

## Remaining red markers — 2
Toufique's contribution, Hafiz's contribution (Division of Work).
The repository URL marker is also still there if you want a link instead of
"on request". Check: `grep -c 'NUM{' main.tex`

## Verified numbers
G1 5.57 / 7.36 / 13.68 GB, capacity 14.6 · G2 332.0 s · G3 n=18, x 889.1–1802.2,
df=634, p_zero 0/18, p_min 5.45e-49, crosscheck exactly 0.0 · G4 AUC genuine 1.000,
forged 0.861 (-x) / 0.972 (lambda-x), detection 6/6, 0/6, 5/6 · clean mean p 0.480
vs 0.472 original · missed forgery x=1558.3, clean range 1483.7–1802.2 ·
seeds 123–128, w_seed fixed at 999999 · sigma 31.75–42.59, lambda 856.6–1541.4


## Reference audit
Every entry in `refs.bib` is cited somewhere in `main.tex`. BibTeX only prints
entries that are cited, so an uncited entry would silently vanish from the PDF
rather than pad it. Check with:

```
grep -o 'cite{[^}]*}' main.tex | tr -d 'cite{}' | tr ',' '\n' | sort -u
```

Verified against arXiv / proceedings pages rather than recalled: Muller (CVPR
2025), Wen Tree-Ring (NeurIPS 2023), Yang Gaussian Shading (CVPR 2024, pp.
12162-12171), Ci RingID (ECCV 2024, pp. 338-354), Gunn (ICLR 2025), Zhao
(NeurIPS 2024), Zhou MetaSeal (TMLR 2026), Zhu PnP (arXiv 2506.06018), Fernandez
Stable Signature (ICCV 2023), Zhu HiDDeN (ECCV 2018), An WAVES (ICML 2024),
Hwang (arXiv 2412.12511), Olszewski (CCS 2023), Arp (USENIX Sec 2022).
