# Forging Tree-Ring: Reproducing and Instrumenting Black-Box Semantic Watermark Forgery

[![arXiv](https://img.shields.io/badge/arXiv-ARXIV__ID-b31b1b.svg)](https://arxiv.org/abs/ARXIV_ID)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Paper & data: CC BY 4.0](https://img.shields.io/badge/paper%20%26%20data-CC%20BY%204.0-lightgrey.svg)](LICENSE-CC-BY-4.0)

**Saifur Rahman Tamim, Md Taslimul Hasan Toufique, A.M. Tayeful Islam**
Department of Computer Science and Engineering, Northern University Bangladesh

This repository contains the paper source, reproduction notebook, measurement
artifacts and analysis scripts for our reproduction of the *Reprompt* semantic
watermark forgery attack of Müller et al.
([CVPR 2025](https://arxiv.org/abs/2412.03283)) against Tree-Ring on Stable
Diffusion XL. We ran it on free-tier dual NVIDIA T4 GPUs (14.6 GB each).

The git tag
[`arxiv-v1`](https://github.com/sr-tamim/watermark-forgery-research/tree/arxiv-v1)
marks the state described in the
arXiv paper.

## Summary

| Arm     | Detected | Mean *x* | Mean *λ − x* | Original rate |
|---------|:--------:|---------:|-------------:|:-------------:|
| genuine | 6/6      | 1096.5   | +220.0       | 1.00          |
| clean   | 0/6      | 1623.9   | −626.3       | 0.01          |
| forged  | 5/6      | 1391.2   | −371.3       | 0.97          |

- **The attack reproduces**, at 325–332 s per attack on a T4.
- **The detector discards its own statistic.** The released Tree-Ring detector
  computes a non-central χ² statistic and returns only its CDF. We recover the
  statistic exactly (maximum difference 0 across all 18 observations). Two
  natural scores built from it separate forged from clean at AUC 0.861 (−*x*)
  and 0.972 (*λ − x*).
- **SDXL runs in fp16** once the pipeline's direct VAE calls are upcast. A
  controlled probe shows the patched path leaves the detector output unchanged.
- **Determinism:** the full pipeline was run in two independent sessions
  (28 Aug and 8 Sep 2026). Every statistic matched; only wall-clock time
  differed.

See the paper for the gate protocol, limitations (notably the single watermark
key and *n* = 18), and discussion.

## Repository layout

```
.
├── paper/                          LaTeX source of the arXiv paper
│   ├── main.tex, refs.bib          paper source (as submitted)
│   ├── main.pdf                    compiled paper
│   ├── mkfigs.py                   regenerates Figs. 1–5
│   └── figures/                    Figs. 1–6
│
└── experiments/                    one folder per notebook session
    ├── 2026-08-28_session1/        the session quoted in the paper
    │   ├── tree_ring_reprompt_reproduction.ipynb   executed notebook
    │   ├── gate1.json … session_meta.json         measurement artifacts
    │   ├── stat_analysis.py        post-hoc statistics + Fig. 6
    │   └── stats_report.txt        output of stat_analysis.py
    └── 2026-09-08_session2/        independent re-execution
```

[`experiments/README.md`](experiments/README.md) describes every artifact
file. [`paper/README.md`](paper/README.md) covers building the paper and where
each figure comes from.

## Reproducing

### 1. Rerun the experiment (GPU)

The notebook targets a Kaggle notebook with the **GPU T4 ×2** accelerator
(the P100 is not supported by PyTorch 2.10). Open
`experiments/2026-08-28_session1/tree_ring_reprompt_reproduction.ipynb`, run
it top to bottom, and restart the kernel when the pinning cell asks you to.
Outputs are written to `/kaggle/working/phase0_out`.

The notebook clones our fork of the released attack code and hard-resets it
to the exact commit used for every run in the paper:

| | Repository | Commit |
|---|---|---|
| Fork (used) | [sr-tamim/semantic-forgery](https://github.com/sr-tamim/semantic-forgery) | `7f9e7ad` |
| Upstream base | [and-mill/semantic-forgery](https://github.com/and-mill/semantic-forgery) | `ca68950` |

Models: `stabilityai/stable-diffusion-xl-base-1.0` (target, fp16) and
`Manojb/stable-diffusion-2-1-base` (attacker, fp32; a mirror of the withdrawn
SD 2.1 base weights). `session_meta.json` records library versions, dtypes,
devices and the SHA-256 of the resolved dependency lock.

### 2. Recompute the statistics and figures (CPU)

Both steps need only `numpy pandas scipy matplotlib`.

```bash
# post-hoc statistics (stats_report.txt) and Fig. 6
cd experiments/2026-08-28_session1
python stat_analysis.py

# Figs. 1–5, written to paper/figures/
cd ../../paper
python mkfigs.py
```

## Citation

```bibtex
@article{tamim2026forging,
  title   = {Forging Tree-Ring: Reproducing and Instrumenting Black-Box
             Semantic Watermark Forgery},
  author  = {Tamim, Saifur Rahman and Toufique, Md Taslimul Hasan and
             Islam, A.M. Tayeful},
  journal = {arXiv preprint arXiv:ARXIV_ID},
  year    = {2026}
}
```

Please also cite the original attack:

```bibtex
@inproceedings{muller2025semantic,
  title     = {Black-Box Forgery Attacks on Semantic Watermarks for Diffusion Models},
  author    = {M{\"u}ller, Andreas and Lukovnikov, Denis and Thietke, Jonas and
               Fischer, Asja and Quiring, Erwin},
  booktitle = {IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year      = {2025}
}
```

## License

- **Code** (notebooks, `*.py`): [MIT](LICENSE)
- **Paper source, figures and measurement data** (`paper/`, experiment
  artifacts): [CC BY 4.0](LICENSE-CC-BY-4.0)

The attack implementation itself is not in this repository. It lives in the
fork linked above and remains under its original authors' terms.

## Acknowledgements

This paper is the final project report for CSE 4383: Image Processing and
Computer Vision Lab Work, Northern University Bangladesh. We thank Müller et
al. for releasing their code.
