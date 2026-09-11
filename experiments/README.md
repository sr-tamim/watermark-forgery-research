# Experiment sessions

Each folder holds one end-to-end execution of the reproduction notebook, run
from a clean environment build on Kaggle (2× Tesla T4). Artifact file names
match those cited in the paper.

| Session | `session_meta.json` timestamp | Fork commit | Lock SHA-256 | Reprompt wall-clock |
|---|---|---|---|---|
| [`2026-08-28_session1`](2026-08-28_session1) | 2026-08-28 05:28 | `7f9e7ad` | `5592c786…` | 332.0 s |
| [`2026-09-08_session2`](2026-09-08_session2) | 2026-09-08 10:16 | `7f9e7ad` | `5592c786…` | 324.8 s |

**Session 1 is the one quoted in the paper.** Session 2 is an independent
re-execution of the same notebook code. Its `gate3.json`, `gate4.json`,
`phase0_scores.csv`, `precision_probe.json` and dependency locks are
byte-identical to session 1. The only differences are timing fields
(`timings.json`, `gate1.json`, `phase0_verdict.json`) and re-rendered PNGs.

## Artifacts

| File | Contents |
|---|---|
| `tree_ring_reprompt_reproduction.ipynb` | The executed notebook, with outputs |
| `session_meta.json` | Fork and upstream commits, model IDs, dtypes, devices, library versions, lock SHA-256, timestamp |
| `requirements.lock.txt` | `pip freeze` after applying the version pins |
| `repo_deps.installed` | `pip freeze` after installing the attack repo's remaining requirements |
| `gate1.json` | **G1**: peak allocated GPU memory, plus time to load and run one 20-step generation, for attacker fp32, target fp16 and target fp32 |
| `timings.json` | **G2**: wall-clock time, exit code and output tail of the released `run_reprompting.py` |
| `precision_probe.json` | Non-finite checks and detection *p*-value under fp16 vs fp32 VAE |
| `gate3.json` | **G3**: range of the recovered statistic *x*, *p*-value censoring check, cross-check against the released detector |
| `phase0_scores.csv` | One row per observation (6 trials × genuine/clean/forged): `x`, `lambd`, `df`, `sigma`, `p_value`, `log_p`, `detected`, `evidence` |
| `gate4.json` | **G4**: AUC of genuine and forged vs clean |
| `gate4_separation.png` | The notebook's diagnostic separation plot |
| `phase0_verdict.json` | All gate results and environment summary in one file |
| `fig6_distributions.png` | Fig. 6 (session 1 copy is the one in the paper) |

Session 1 additionally contains:

| File | Contents |
|---|---|
| `stat_analysis.py` | Post-hoc statistics: Wilson intervals, bootstrap AUC CIs, Mann-Whitney tests, Cohen's *d*; also draws Fig. 6 |
| `stats_report.txt` | Output of `stat_analysis.py`, quoted in the paper's uncertainty analysis |

To regenerate `stats_report.txt` and `fig6_distributions.png`:

```bash
cd 2026-08-28_session1
python stat_analysis.py
```
