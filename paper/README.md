# Paper source

`main.tex` and `refs.bib` are the source as submitted to arXiv. The tag
`arxiv-v1` marks that version.

```
main.tex                        preamble + all sections, single file
refs.bib                        23 entries, all cited in the text
main.pdf                        compiled output, 11 pages
mkfigs.py                       regenerates Figs. 1–5
figures/fig1_pipeline.png       attack flow diagram
figures/fig2_memory.png         G1 peak memory
figures/fig3_statistic.png      per-arm x, missed forgery circled
figures/fig4_roc.png            ROC, -x vs lambda-x
figures/fig5_pvalues.png        p-values vs threshold
figures/fig6_distributions.png  box + strip by arm, both scores
```

## Building

```bash
latexmk -pdf main.tex
```

On Overleaf, upload everything with `figures/` kept as a folder and use the
pdfLaTeX compiler.

## Where the figures come from

All figures are drawn with matplotlib. None is copied, traced or adapted
from another source.

| Figure | Script | Input |
|---|---|---|
| Fig. 1 (pipeline) | `mkfigs.py` | none, drawn from boxes and arrows |
| Fig. 2 (memory) | `mkfigs.py` | `gate1.json` |
| Figs. 3–5 | `mkfigs.py` | `phase0_scores.csv` |
| Fig. 6 (distributions) | `../experiments/2026-08-28_session1/stat_analysis.py` | `phase0_scores.csv` |

All inputs are read from `../experiments/2026-08-28_session1/`, the session
the paper quotes. Run `python mkfigs.py` from this directory; it overwrites the
PNGs in `figures/`. Rerunning with a different matplotlib version can shift
image sizes by a few pixels, but the plotted content is unchanged.

## Reference audit

Every entry in `refs.bib` is cited in `main.tex`. BibTeX prints only cited
entries, so an uncited entry would silently drop out of the PDF. To check:

```bash
grep -o 'cite{[^}]*}' main.tex | sed 's/cite{//;s/}//' | tr ',' '\n' | sort -u
```
