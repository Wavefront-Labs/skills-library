---
id: social-sciences.economics.econometrics.ols-panel-iv-and-robust-inference
name: ols-panel-iv-and-robust-inference
category: social-sciences
field: economics
product: econometrics
tags: [econometrics, ols, regression, omitted-variable-bias, heteroskedasticity, robust-standard-errors, clustered-standard-errors, wild-cluster-bootstrap, panel-data, fixed-effects, random-effects, hausman-test, first-differences, two-way-fixed-effects, instrumental-variables, iv, 2sls, weak-instruments, first-stage-f, effective-f, anderson-rubin, exclusion-restriction, overidentification, time-series, stationarity, unit-root, adf-test, cointegration, newey-west, hac, specification-tests]
level: advanced
status: gated
description: "Choose and diagnose the core econometric estimator: OLS with the right standard errors, panel fixed effects, IV/2SLS with weak-instrument checks, and time-series basics like unit roots and HAC SEs."
sources: ["Wooldridge, Econometric Analysis of Cross Section and Panel Data (2nd ed., MIT 2010)", "Angrist & Pischke, Mostly Harmless Econometrics (Princeton 2009)", "Cameron & Miller (2015), Journal of Human Resources 50(2)", "Andrews, Stock & Sun (2019), Annual Review of Economics 11"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Econometrics core — estimator, assumptions, inference

**Goal:** for any empirical question, pick an estimator whose identifying assumption you
can state and defend, and report standard errors that respect how the data were generated.
Design-based causal methods (DiD, RDD, synthetic control) are in
social-sciences.economics.causal-inference-economics.staggered-did-rdd-and-synthetic-control.

## 1. OLS — what it needs
Unbiasedness hinges on **E[u | X] = 0**. The **omitted variable bias** formula: if the true
model has `z` and you omit it, bias on `x` = β_z × (coefficient from regressing z on x).
Use it to *sign* likely bias in your discussion.
- Report **heteroskedasticity-robust** SEs by default (Stata `vce(robust)`; R `fixest`
  `vcov = "hetero"` (gated: unconfirmed, source is paywalled or blocked); Python `statsmodels` `cov_type="HC1"`; in `linearmodels` use `cov_type="robust"`, since `"HC1"` raises UnknownOptionError).
- **Cluster** at the level of treatment assignment or where errors plausibly correlate
  (state, firm, school). With few clusters, conventional cluster SEs over-reject (Cameron & Miller 2015 survey the rules of thumb);
  use the **wild cluster bootstrap** (`boottest` in Stata (gated: unconfirmed, source is paywalled or blocked); `fwildclusterboot` in R was archived from CRAN on 2024-05-29, install from its GitHub repo).
- "Bad controls": do not condition on variables affected by the treatment.

## 2. Panel data
| Estimator | Identifying variation | Assumption |
|---|---|---|
| Pooled OLS | All | No unobserved unit effect correlated with X |
| Random effects | Weighted within + between | Unit effect uncorrelated with X |
| **Fixed effects (within)** | Within unit over time | Strict exogeneity given unit effect |
| First differences | Changes | Similar; better with serially correlated (random-walk) errors |
- Hausman test compares FE and RE, but the classic version is invalid with clustered errors;
  use the Mundlak (correlated random effects) approach or simply default to FE in economics.
- FE removes time-invariant regressors and absorbs a lot of variance — report within-R² and
  how much identifying variation remains.
- Fast multi-way FE: `reghdfe` (Stata), `fixest::feols(y ~ x | id + year)` (R), `pyfixest` (Python).
- Two-way FE with staggered treatment timing is **not** a clean DiD — see the causal skill.

## 3. Instrumental variables
Need **relevance** (instrument moves X) and **exclusion** (affects Y only through X). Only
relevance is testable.
- Report the first stage, the reduced form, and 2SLS. If the reduced form is zero, so is the effect.
- **Weak instruments:** the old rule "first-stage F > 10" is a minimum; with
  heteroskedastic/clustered errors use the **effective F** (Montiel Olea–Pflueger) and
  report **Anderson–Rubin** confidence intervals, which are valid even when instruments are weak.
  Lee, McCrary, Moreira & Porter (AER 2022; arXiv 2010.05058) report that a true 5% t-test needs a first-stage F above 104.7 (one instrument).
- Overidentification tests (Hansen J) only test instruments against each other; passing
  them does not validate exclusion.
- IV estimates a **LATE** — the effect for compliers — not the average effect; describe who
  the compliers are.

## 4. Time series essentials
- Check stationarity (ADF, KPSS, plot first). Regressing one trending series on another
  gives **spurious regression** with high R².
- Nonstationary but cointegrated series: error-correction models; otherwise difference.
- Serial correlation: **Newey–West/HAC** SEs; choose lag length by a rule of thumb or
  data-driven selection (state the rule you used).
- VARs for dynamic interactions; identification of structural shocks needs explicit
  restrictions (recursive, sign, external instruments).

## 5. Specification diagnostics
Residual plots, influential observations (leverage, Cook's distance), functional form
(add squares/splines, RESET), and stability across subsamples. Log transformations: with
zeros, `log(1+y)` and inverse hyperbolic sine results depend on units — consider Poisson
pseudo-ML (`ppmlhdfe`, `fepois`) instead.

## Gotchas
- Clustering at too fine a level understates uncertainty; at too coarse a level with few
  clusters, use the bootstrap.
- Significance tests on many outcomes: adjust (Romano–Wolf, sharpened q-values) or pre-specify.
- Including lagged dependent variable with FE in short panels → Nickell bias.

## Verify
- [ ] Identifying assumption stated in one sentence for the main estimate.
- [ ] SEs clustered at the assignment level; few-cluster correction if needed.
- [ ] Panel: FE choice justified; staggered-timing issues addressed.
- [ ] IV: first stage, reduced form, effective F, AR intervals reported.
- [ ] Time series: stationarity checked; HAC SEs where needed.
- [ ] Robustness to functional form and influential observations shown.

*Checked: linearmodels cov_type names run in linearmodels; pyfixest syntax run; F threshold from arXiv abstract.*
