# Forging Tree-Ring — single-file source

Three files total:
```
main.tex                      <- everything: preamble + all 10 sections
refs.bib                      <- 13 references
figures/gate4_separation.png  <- Figure 1 (your real plot)
```

## Build
```
latexmk -pdf main.tex
```
On Overleaf: upload all three (keep `figures/` as a folder), set the compiler to
pdfLaTeX. 8 pages, 0 undefined references.

Packages used, all standard in TeX Live and Overleaf: geometry, times, microtype,
booktabs, multirow, graphicx, xcolor, amsmath, listings, algorithm, algpseudocode,
natbib, caption, balance, hyperref, url, titlesec.

## Layout of main.tex
| lines | what |
|---|---|
| 1–70 | preamble: layout, listing style, macros |
| ~72–100 | title and author block |
| ~102 onward | Abstract, then Sections 1–9, then bibliography |

Sections in order: Introduction · Background and Related Work · Reproduction
Setup · Environment Reconstruction · Detector Instrumentation · Evaluation ·
Discussion · Limitations · Conclusion (+ Division of Work, Availability).

## Remaining red markers — 3
`\NUM{}` renders in red. Search for `NUM{` in main.tex:
- Toufique's contribution (Division of Work)
- Hafiz's contribution (Division of Work)
- repository URL (Availability)

## Switching to IEEEtran
Replace line 1 with `\documentclass[conference]{IEEEtran}` and comment out the
`geometry`, `titlesec` and `times` lines in the preamble. The `\author{}` block
uses plain superscript numbering (department house style) and carries over as-is.

## Numbers
All from your run artifacts. G1 5.57 / 7.36 / 13.68 GB · G2 338.3 s · G3 n=18,
x in [889.1, 1802.2], df=634, p_zero 0/18, p_min 5.45e-49, crosscheck 0.0 ·
G4 AUC genuine 1.000, forged 0.861 (-x) / 0.972 (lambda-x), detection 6/6, 0/6,
5/6 · clean mean p 0.480 vs 0.472 original · precision probe both dtypes
p = 1.6648e-36.
