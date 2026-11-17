---
id: social-sciences.economics.causal-inference-economics.staggered-did-rdd-and-synthetic-control
name: staggered-did-rdd-and-synthetic-control
category: social-sciences
field: economics
product: causal-inference-economics
tags: [causal-inference-economics, causal-inference, policy-evaluation, difference-in-differences, did, staggered-adoption, two-way-fixed-effects, twfe, callaway-santanna, sun-abraham, de-chaisemartin-dhaultfoeuille, borusyak-jaravel-spiess, event-study, parallel-trends, pre-trends, honestdid, regression-discontinuity, rdd, sharp-rdd, fuzzy-rdd, rdrobust, bandwidth, mccrary-test, density-test, synthetic-control, synthetic-did, placebo-tests, matching, propensity-score, rct-analysis, potential-outcomes]
level: advanced
status: gated
description: "Estimate causal policy effects from economic data: modern staggered DiD and event studies, sharp and fuzzy RDD with rdrobust, synthetic control with placebo inference, plus the checks referees expect."
sources: ["Roth, Sant'Anna, Bilinski & Poe (2023), Journal of Econometrics 235(2)", "Callaway & Sant'Anna (2021), Journal of Econometrics 225(2)", "Cattaneo, Idrobo & Titiunik, A Practical Introduction to Regression Discontinuity Designs (Cambridge Elements 2020)", "Abadie (2021), Journal of Economic Literature 59(2)", "Cunningham, Causal Inference: The Mixtape (Yale 2021)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Causal inference for policy evaluation — DiD, RDD, synthetic control

**Goal:** a credible estimate of what a policy did, with the design's key assumption
made visible and stress-tested. General estimator and inference issues are in
social-sciences.economics.econometrics.ols-panel-iv-and-robust-inference.

## 1. Choose the design from how treatment was assigned
| Assignment | Design |
|---|---|
| Random (lottery, RCT) | Compare means; ITT, then LATE via IV for compliance |
| Score crosses a known cutoff | **Regression discontinuity** |
| Some units adopt at different times; others never/later | **Difference-in-differences / event study** |
| One or a few treated aggregate units (a state, a country) | **Synthetic control** / synthetic DiD |
| Selection on observables only | Matching/weighting — weakest; needs a strong argument and sensitivity analysis |
Write the estimand (ATT, LATE at cutoff, effect for the treated unit) before estimating.

## 2. Difference-in-differences
- **Canonical 2×2** (two groups, two periods): TWFE is fine.
- **Staggered adoption:** TWFE uses already-treated units as controls and can produce
  wrong-sign estimates when effects vary over time. Use heterogeneity-robust estimators:
  Callaway–Sant'Anna (`did` in R (CRAN), `csdid` in Stata and on PyPI), Sun–Abraham (`fixest::sunab()`),
  Borusyak–Jaravel–Spiess imputation (`did_imputation`), de Chaisemartin–D'Haultfœuille
  (`did_multiplegt_dyn`). Show the Goodman-Bacon decomposition to explain any gap with TWFE.
- **Event study plot:** leads and lags relative to adoption with the period before as reference.
  Flat pre-period coefficients are supportive, not proof — pre-tests have low power.
  Report sensitivity with **HonestDiD** (Rambachan–Roth) bounds for violations of parallel trends.
- Choose controls: never-treated vs not-yet-treated, and say why.
- Covariates only if parallel trends plausibly holds conditionally; use doubly robust versions.
- Cluster at the level of policy variation.

## 3. Regression discontinuity
- **Sharp:** treatment switches on at the cutoff. **Fuzzy:** probability jumps → IV with the
  cutoff as instrument.
- Use local linear regression with **data-driven bandwidth** and robust bias-corrected
  inference: `rdrobust y x, c(0)` (Stata/R/Python; `rdrobust`, `rddensity` and `HonestDiD` are on CRAN, `rdrobust`/`rddensity` on PyPI). Avoid global high-order polynomials
  (Gelman–Imbens 2019).
- Plot binned means with `rdplot`.
- **Manipulation:** density test at the cutoff (`rddensity`; successor to McCrary). Bunching
  just above a threshold kills the design.
- **Covariate balance** at the cutoff: run the RD on pre-determined covariates — they should
  not jump. Show robustness to bandwidth (half, double) and donut-hole specifications.
- The estimate is local to the cutoff; be explicit about external validity.

## 4. Synthetic control
- Build a weighted combination of donor units matching the treated unit's pre-period
  outcome path (and predictors). Weights non-negative and sum to one.
- Good pre-period fit is required; poor fit → do not interpret.
- Exclude donors exposed to similar policies or spillovers.
- **Inference by placebo:** reassign treatment to each donor, compute the post/pre RMSPE
  ratio, and report the treated unit's rank (permutation p-value).
- Robustness: leave-one-out donors, in-time placebos (fake earlier date).
- **Synthetic DiD** (Arkhangelsky et al.; `synthdid` package) blends unit and time weights;
  useful with several treated units.
- Tools: `Synth` (CRAN); `synthdid` and `augsynth` are GitHub-only (not on CRAN; github.com/synth-inference/synthdid, github.com/ebenmichael/augsynth); `synth`, `sdid` (Stata) (gated: unconfirmed, source is paywalled or blocked).

## 5. RCT analysis
Pre-registered primary outcome, ITT with baseline covariates and strata fixed effects,
attrition bounds (Lee bounds) if differential, multiple-testing corrections across outcome families.

## Gotchas
- Anticipation effects contaminate the "pre" period; shift the reference period if adoption was announced.
- Composition changes in repeated cross-sections can masquerade as effects.
- Reporting the one bandwidth or donor pool that works.

## Verify
- [ ] Estimand and assignment mechanism stated; design matches it.
- [ ] Staggered DiD uses a heterogeneity-robust estimator; event-study plot shown.
- [ ] Parallel-trends sensitivity (HonestDiD or similar) reported.
- [ ] RDD: rdrobust, density test, covariate balance, bandwidth robustness.
- [ ] SCM: pre-fit shown, placebo distribution and rank reported.
- [ ] Clustering and multiple-testing handled.

*Checked: package availability on CRAN/PyPI/GitHub (2026-10-19). Estimator behaviour and the Gelman-Imbens, Rambachan-Roth, Arkhangelsky citations were not re-read (gated: unconfirmed, source is paywalled or blocked); this literature moves fast.*
