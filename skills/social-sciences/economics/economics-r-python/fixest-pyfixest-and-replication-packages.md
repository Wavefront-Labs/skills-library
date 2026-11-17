---
id: social-sciences.economics.economics-r-python.fixest-pyfixest-and-replication-packages
name: fixest-pyfixest-and-replication-packages
category: social-sciences
field: economics
product: economics-r-python
tags: [economics-r-python, r, python, fixest, feols, fepois, feglm, etable, modelsummary, pyfixest, linearmodels, statsmodels, pandas, polars, data-table, tidyverse, dplyr, did-package, rdrobust, synthdid, marginaleffects, renv, uv, conda, targets, quarto, jupyter, replication-package, reproducibility, fred-api, wbgapi, pandas-datareader, computational-economics, numpy, scipy, quantecon]
level: practitioner
status: gated
description: "Empirical economics in R or Python: fixest/pyfixest with fixed effects and clustering, data wrangling at scale, pinned environments, and a replication package that runs end to end."
sources: ["fixest documentation (lrberge.github.io/fixest)", "pyfixest documentation (py-econometrics.github.io/pyfixest)", "linearmodels documentation", "QuantEcon lectures (quantecon.org)", "AEA Data Editor replication template"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# R and Python for economics — estimation, data, reproducibility

**Goal:** empirical results in R or Python that match what a Stata-trained referee expects
(same estimators, same clustering), produced by a pipeline anyone can rerun.

## 1. Estimation with fixed effects
**R — fixest** (fast, multi-way FE, the de facto standard):
```r
library(fixest)
m1 <- feols(y ~ x + ctrl | firm + year, data = df, cluster = ~firm)
m2 <- feols(y ~ ctrl | firm + year | x ~ z, data = df, cluster = ~firm)  # IV
m3 <- fepois(count ~ x | firm + year, data = df)                          # Poisson PML
etable(m1, m2, m3, tex = TRUE, file = "output/tables/main.tex")
```
(gated: unconfirmed, source is paywalled or blocked) The R fixest block and the options below were not run here (R unavailable); the Python pyfixest block was run on simulated data (`feols` with `vcov={"CRV1": ...}`, IV via `| x ~ z`, `fepois`, `etable` all work in pyfixest 0.60).
- Multiple outcomes/specifications in one call: `feols(c(y1, y2) ~ x | sw0(year, firm), df)`.
- Event study: `feols(y ~ i(rel_time, treated, ref = -1) | id + year, df)`; staggered:
  `sunab(cohort, year)`; plot with `iplot()`.
- Marginal effects for nonlinear models: `marginaleffects::avg_slopes()`.
- Tables: `etable` or `modelsummary` (Word, HTML, LaTeX).

**Python — pyfixest** mirrors the fixest syntax:
```python
import pyfixest as pf
fit = pf.feols("y ~ x + ctrl | firm + year", data=df, vcov={"CRV1": "firm"})
pf.etable([fit])
```
Alternatives: `linearmodels` (`PanelOLS`, `IV2SLS`, absorbing regressions) and
`statsmodels` (general GLMs; formula API).

**Matching Stata:** small-sample corrections differ by package. fixest sets them with
`ssc()` (documented defaults `K.adj=TRUE`, `K.fixef="nonnested"`, `G.adj=TRUE`; the docs do not claim they match `reghdfe`); if a referee compares numbers, set `ssc()` options explicitly and
document them. Check on one model that SEs match the Stata output to 3 decimals.

## 2. Data work at scale
- R: `data.table` or `dplyr` (with `dtplyr`/`arrow` for big data); `haven` for `.dta`.
- Python: `pandas` for most; `polars` for speed on large files; `pd.read_stata()` turns value labels into categoricals by default (`convert_categoricals`).
- Store intermediate data as **Parquet** (types preserved, fast), not CSV.
- Merges: assert the key is unique first (`stopifnot(!anyDuplicated(df[c("id","year")]))`;
  pandas `merge(..., validate="one_to_one", indicator=True)`).
- Pull public data reproducibly: FRED (`fredr`, `fredapi`), World Bank (`WDI`, `wbgapi`),
  saving the raw pull with the download date.

## 3. Computational economics
- Python: `numpy`/`scipy` (optimisation, root finding), `numba` for loops, `jax` for
  autodiff; QuantEcon libraries and lectures for dynamic programming, Markov chains, and
  heterogeneous-agent models.
- R is weaker here; Julia is common for heavy models. Dynare (MATLAB/Octave) for DSGE — see
  social-sciences.economics.macroeconomic-modelling.solving-and-simulating-dsge-models-with-dynare.
- Validate numerical solutions: Euler-equation errors, grid refinement, alternative starting values.

## 4. Environments and pipelines
- R: **renv** (`renv::init()`, `renv::snapshot()`; replicators run `renv::restore()`).
  Optional `targets` for a dependency-aware pipeline that only rebuilds what changed.
- Python: `uv` or `conda` with a lock file (`uv.lock`, `environment.yml` with pinned versions).
- One entry point: `run_all.R` / `main.py` / a Makefile. Notebooks are fine for exploration;
  the replication path should run headless (`quarto render`, `jupyter nbconvert --execute`).
- Set seeds (`set.seed()`, `np.random.default_rng(seed)`).

## 5. Replication package
README with data availability statement, software versions, package lock file, expected
runtime and hardware, and a table mapping each figure/table to the script that makes it.
Run it in a clean container or fresh machine before submission.

## Gotchas
- Silent NA drops: fixest reports removed observations — check `nobs()` against expectations.
- pandas `groupby` drops NaN keys by default (`dropna=False` to keep).
- Floating IDs read from CSV lose leading zeros; specify `dtype`/`col_types`.
- Different default clustering adjustments between R, Python and Stata.

## Verify
- [ ] Key models replicated against a second implementation (or Stata) on one spec.
- [ ] Lock file committed; fresh environment restores and runs.
- [ ] One command regenerates all outputs from raw data.
- [ ] Merge validations and observation counts logged.
- [ ] README maps outputs to scripts.

*Checked: pandas defaults (`convert_categoricals=True`, `groupby` drops NaN keys, `merge(validate=...)` raises MergeError) run in pandas; pyfixest run. Pin versions; APIs evolve.*
