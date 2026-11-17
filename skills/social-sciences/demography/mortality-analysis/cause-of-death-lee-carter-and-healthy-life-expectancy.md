---
id: social-sciences.demography.mortality-analysis.cause-of-death-lee-carter-and-healthy-life-expectancy
name: cause-of-death-lee-carter-and-healthy-life-expectancy
category: social-sciences
field: demography
product: mortality-analysis
tags: [mortality-analysis, mortality, demography, cause-of-death, icd-10, icd-11, garbage-codes, ill-defined-causes, redistribution, cause-deleted-life-table, competing-risks, survival-analysis, cox-model, gompertz, hazard, lee-carter, mortality-forecasting, stmomo, demography-r-package, coherent-forecasting, excess-mortality, healthy-life-expectancy, hle, dfle, sullivan-method, hale, avoidable-mortality, mortality-improvement]
level: advanced
status: draft
description: "Analyse mortality: clean cause-of-death data (ICD, garbage codes), fit survival models, forecast with Lee-Carter, and compute healthy life expectancy with Sullivan's method."
sources:
  - https://cran.r-project.org/web/packages/demography/refman/demography.html
  - https://cran.r-project.org/web/packages/StMoMo/index.html
  - https://doi.org/10.2307/2290201
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cause-of-death analysis, Lee–Carter forecasting and healthy life expectancy

**Goal:** go beyond overall life expectancy: what people die of, how mortality will
evolve, and how many years are lived in good health.

## 1. Cause-of-death data
- Coded to ICD-10 (ICD-11 adoption is under way at different speeds by country —
  check which revision your series uses). Revision changes create breaks; use bridge-
  coding studies or comparability ratios across revisions.
- **Underlying cause** (the one that started the chain) is what standard tabulations
  use; multiple-cause data capture contributing conditions (important for diabetes, dementia).
- **Garbage codes** — ill-defined or impossible underlying causes (e.g. R00–R99 symptoms,
  heart failure unspecified, septicaemia as underlying) — can be 10–30%+ of deaths in some
  systems. Redistribute proportionally or with GBD-style algorithms, and report the share.
- Age-standardise cause-specific rates for comparisons (see
  social-sciences.demography.demographic-rates-life-tables).

## 2. Cause-related life-table tools
- **Cause-deleted life table:** e0 if a cause were eliminated, assuming independence of
  competing risks (a strong assumption — removed deaths would partly occur from other causes).
- **Decomposition** of e0 gaps by age and cause (Arriaga extended).
- **Competing-risks** methods (cumulative incidence functions, Fine–Gray) for individual data.

## 3. Individual-level survival
Cox proportional hazards or parametric (Gompertz for adult ages: hazard rises roughly
exponentially, doubling every ln2/b years; slope b of 0.085-0.10 per year gives 7-8 years) models on linked
cohort/register data. Check proportional hazards (Schoenfeld residuals); use age as
the time scale for mortality studies of adults.

## 4. Lee–Carter forecasting
Model: log m(x,t) = a(x) + b(x)·k(t) + ε.
- a(x): average age pattern; k(t): mortality index over time; b(x): age sensitivity to k.
- Fit by SVD on centred log rates, constrain Σb = 1 and Σk = 0, re-estimate k(t) so
  fitted deaths match observed (second-stage).
- Forecast k(t) as a random walk with drift; intervals from the drift uncertainty and
  innovation variance.
- R: `demography::lca()` then `forecast()` (`forecast.lca`), or `StMoMo` (also Cairns–Blake–Dowd,
  age-period-cohort models).
- Choose the fitting period with care — a structural break (e.g. 1950s vs post-1980
  improvement) changes the drift. Lee–Miller variant uses a later fitting window.
- **Coherent forecasts** (Li–Lee) for sexes/subpopulations avoid diverging projections.
- Known limitation: b(x) fixed over time → age pattern of improvement can't shift.

## 5. Excess mortality
Observed minus expected deaths, with expected from a baseline model (e.g. weekly deaths
from recent years with trend and seasonality, or projected rates × current population).
Baseline choice drives results — report it and test alternatives.

## 6. Healthy life expectancy (Sullivan method)
1. Take the period life table's nLx.
2. Get age-specific prevalence of health/disability π(x) from a survey (e.g. "limited
   in activities" GALI for EU HLY, self-rated health).
3. Healthy years in each interval = nLx · (1 − π(x)); sum from age x upward and divide
   by lx → HLE at age x.
Prevalence must refer to the same population and period; institutionalised people
(often excluded from surveys) have higher disability — adjust if possible. Different
health measures (disability-free vs good self-rated health) give very different HLE.
WHO HALE uses a more complex severity-weighted approach.

## Gotchas
- Small-area cause-specific rates are unstable — use Bayesian smoothing or pool years.
- Lee–Carter intervals are often too narrow (they ignore model and parameter uncertainty).
- Uncertain: garbage-code shares vary hugely by country; the range above is indicative only.

## Verify
- [ ] ICD revision and coding changes handled; garbage share reported and redistributed.
- [ ] Competing-risk assumptions stated for cause-deleted results.
- [ ] Lee–Carter fitting period justified; residuals show no strong cohort pattern left.
- [ ] Excess-mortality baseline documented with sensitivity check.
- [ ] HLE prevalence measure, survey and population coverage stated.
