---
id: mathematics.statistics.survey-sampling.survey-weighting-and-design-effects
name: survey-weighting-and-design-effects
category: mathematics
field: statistics
product: survey-sampling
tags: [statistics, survey-sampling, survey, sampling, stratified-sampling, cluster-sampling, probability-sampling, design-weights, survey-weights, post-stratification, raking, calibration, nonresponse, nonresponse-adjustment, design-effect, deff, effective-sample-size, kish, margin-of-error, horvitz-thompson, survey-package, svydesign, finite-population-correction]
level: practitioner
status: gated
description: "Estimate population quantities from a survey: build design weights, adjust for nonresponse, rake to known totals, and compute design effects and honest margins of error."
sources: ["https://search.r-project.org/CRAN/refmans/survey/html/svydesign.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Survey weighting and design effects

**Goal:** turn responses from a sample into population estimates with standard
errors that reflect how the sample was actually drawn.

## 1. Know the design before touching the data
Record for every respondent: **stratum**, **cluster (PSU)**, **selection probability**.
- **Stratified** sampling (sample within groups) usually *reduces* variance.
- **Cluster** sampling (sample schools, then pupils) usually *increases* it, because
  people in a cluster are alike (intra-class correlation, ρ).
- Unequal selection probabilities (oversampling a minority) need weights or estimates are biased.

## 2. Build weights in three stages
1. **Design (base) weight** = 1 / selection probability. A person sampled with
   probability 1/500 represents 500 people. Sum of base weights ≈ population size.
2. **Nonresponse adjustment** — within cells that predict response (age × region, say),
   multiply respondents' weights by (sum of weights of eligible sampled units) /
   (sum of weights of respondents). This assumes nonresponse is random *within* cells;
   choose cells on variables related to both response and outcome.
3. **Calibration / raking** — adjust weights so weighted totals match known population
   margins (census age, sex, region). Raking (iterative proportional fitting) cycles
   through margins until all match, (iteration counts vary; stop on a convergence tolerance). Post-stratification
   is the one-variable-cross case.
Then **trim** extreme weights (caps such as a multiple of the median weight or a fixed percentile are agency conventions; no single standard cap confirmed, gated: unconfirmed, source is paywalled or blocked)
and re-rake. Extreme weights blow up variance.

## 3. Design effect and effective sample size
- **Kish's weighting design effect**: deff_w = n·Σw² / (Σw)² = 1 + CV²(weights).
- **Clustering design effect**: deff_c ≈ 1 + (m − 1)·ρ, where m = average cluster size.
  With 20 pupils per school and ρ = 0.05: 1 + 19 × 0.05 = 1.95 — your sample is worth
  about half its nominal size.
- **Effective n** = n / deff. Margin of error for a proportion at 95%:
  MOE ≈ 1.96·√(p(1−p)/n_eff). With n = 1,000, p = 0.5 and deff 1.5:
  n_eff ≈ 667, MOE ≈ ±3.8 points, not the naïve ±3.1 (recomputed: 3.80 and 3.10).

## 4. Analyse with design-aware software
Ordinary `lm()` or `mean()` with weights gives right point estimates but wrong SEs.
- R: `library(survey)` (svydesign signature confirmed in the CRAN reference manual: `ids, probs, strata, variables, fpc, data, nest, weights`; set `nest = TRUE` when PSU ids repeat across strata); `d <- svydesign(ids = ~psu, strata = ~stratum, weights = ~w,
  data = df, nest = TRUE); svymean(~y, d); svyglm(y ~ x, d)`. Raking: `rake()`
  or `calibrate()`.
- Python: `samplics` (exists on PyPI, 0.6.1 fetched); Stata: `svyset` then `svy:` prefix; SAS: `PROC SURVEYMEANS/SURVEYREG`.
- Replicate weights (jackknife, BRR, bootstrap) supplied by agencies are used instead
  of strata/PSU — declare them as provided.
- **Subpopulations:** use `subset()` on the design object (domain estimation), never
  filter the data frame first — that discards design information and understates SEs.
- **Finite population correction** (1 − n/N) matters when the sampling fraction is non-trivial (a common rule of thumb is above about 5%, not a hard threshold; gated: unconfirmed, source is paywalled or blocked).

## 5. Nonprobability (opt-in, panel) samples
Weighting can correct only for variables you weight on. Raking an online opt-in panel
to census margins doesn't make it a probability sample; report it as "modelled" and be
cautious with margins of error. Uncertain: practice here is evolving (MRP, propensity
pseudo-weights); treat any single method as provisional.

## Gotchas
- Weighting on a variable unrelated to the outcome adds variance and no bias reduction.
- Raking to margins that are themselves out of date (old census) imports error.
- Response rates alone don't measure bias; compare respondents to known benchmarks.
- Reporting unweighted n alongside weighted percentages is fine — but compute MOE from n_eff.

## Verify
- [ ] Strata, PSU and selection probability recorded for each case.
- [ ] Base weights sum to roughly the population size.
- [ ] Nonresponse cells chosen on predictors of response and outcome.
- [ ] Weighted margins match the calibration targets; extreme weights trimmed.
- [ ] deff and n_eff reported; MOE uses n_eff.
- [ ] Estimates and SEs come from design-aware routines; domains via subset of the design.
