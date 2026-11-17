---
id: social-sciences.sociology.stratification-demography-analysis.mobility-tables-log-linear-models-and-inequality-measures
name: mobility-tables-log-linear-models-and-inequality-measures
category: social-sciences
field: sociology
product: stratification-demography-analysis
tags: [stratification-demography-analysis, social-stratification, social-mobility, sociology, inequality, mobility-table, origin-destination, absolute-mobility, relative-mobility, odds-ratio, log-linear-models, unidiff, uniform-difference, core-model, quasi-independence, egp, esec, ns-sec, isei, occupational-class, intergenerational-elasticity, ige, rank-rank-slope, gini, theil-index, decomposition, income-inequality, glm-poisson, gnm-package]
level: advanced
status: gated
description: "Analyse class mobility and inequality: build origin-destination tables, separate absolute from relative mobility with log-linear models, and decompose Gini or Theil."
sources:
  - https://cran.r-project.org/web/packages/gnm/index.html
  - https://github.com/hturner/gnm/blob/master/man/yaish.Rd
  - https://www.statsmodels.org/stable/glm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mobility tables, log-linear models and inequality measures

**Goal:** measure how strongly origins shape destinations, distinguishing changes in
the occupational structure from changes in "social fluidity", and describe inequality
with measures whose properties you understand.

## 1. Build the mobility table
- **Origin:** parent's class (usually father's — increasingly the dominance or joint
  approach using both parents) when respondent was ~14. **Destination:** respondent's
  current or main class.
- Use a standard class schema: EGP / ESeC (European), NS-SEC (UK), or occupational status
  scores (ISEI) for continuous analysis. Code from ISCO occupation with employment
  status and supervisory duties. Collapse to 5–7 classes so cells aren't sparse.
- Restrict ages (e.g. 25–64 or 30+) to avoid "occupational immaturity".

## 2. Absolute mobility
Straight from the table: total mobility rate (off-diagonal share), upward vs downward
(requires an agreed class hierarchy), inflow (where destinations came from) and
outflow (where origins went) percentages. Absolute mobility is driven heavily by
**structural change** — e.g. expanding professional classes create upward mobility
even with unchanged fluidity.

## 3. Relative mobility (social fluidity)
Measured by odds ratios: the odds of a service-class vs working-class destination for
service-class vs working-class origins. Independent of the marginal distributions.
Log-linear models on cell counts (Poisson GLM). The R below was NOT run (no R here); `glm` models 1-2 were re-implemented as `smf.glm("n~C*O+C*D+O:D", family=Poisson)` in statsmodels on a simulated 2 x 3 x 3 table and fitted (independence deviance 113.3 on 8 df, constant-fluidity deviance 6.2 on 4 df), and the `gnm` Unidiff syntax matches the `Mult(Exp(educ), orig:dest)` example in the gnm package documentation; the Unidiff model itself was not executed (gated: unconfirmed, source is paywalled or blocked):
```r
# counts by origin (O), destination (D), survey/country (C)
m_cond_ind <- glm(n ~ O*C + D*C, family = poisson, data = t)          # no association
m_const    <- glm(n ~ O*C + D*C + O:D, family = poisson, data = t)    # constant fluidity
library(gnm)                                                           # Unidiff:
m_unidiff  <- gnm(n ~ O*C + D*C + Mult(Exp(C), O:D), family = poisson, data = t)
```
- **Constant social fluidity** model is the classic benchmark (Erikson & Goldthorpe,
  *The Constant Flux*).
- **Unidiff / log-multiplicative layer effect** (Xie 1992, ASR; Erikson & Goldthorpe 1992): a single
  parameter per survey scales the strength of association — "is fluidity rising?"
- **Quasi-independence / diagonal** terms handle class inheritance; **core model**
  topological designs capture hierarchy, inheritance, sector and affinity effects.
- Compare fit with deviance (G²), BIC (large samples make G² reject everything) and
  dissimilarity index Δ (% of cases misclassified).

## 4. Continuous approaches
Economists' intergenerational income elasticity (log child income on log parent
income) and **rank–rank slopes** (Chetty et al.) — rank–rank is less sensitive to
measurement error and changing inequality. Lifecycle bias: income measured too early
or for single years understates persistence; average several years at ages ~35–50.

## 5. Inequality measures
| Measure | Notes |
|---|---|
| Gini | Intuitive; most sensitive to the middle; not additively decomposable by subgroup (checked: on simulated lognormal data with 3 groups, within + between terms summed to 0.516 against a total Gini of 0.507, because of the overlap term) |
| Theil (GE(1)), MLD (GE(0)) | Decompose exactly into between- and within-group components (checked for MLD: total 0.47047 = within + between to 14 digits, with population-share weights) |
| Percentile ratios (P90/P10, P90/P50, P50/P10) | Show where inequality is changing |
| Top shares | Need tax data; surveys miss the top |
Equivalise household income (e.g. square-root or modified OECD scale) and state which.
Bootstrap CIs, respecting survey design.

## Gotchas
- Women's mobility: excluding them or using husband's class embeds assumptions — state yours.
- Comparing countries requires harmonised class coding; schema version differences can
  create spurious differences.
- Uncertain: which class schema is "best" is contested; justify by your question.

## Verify
- [ ] Class coding scheme, origin definition and age restriction documented.
- [ ] Absolute and relative mobility reported separately.
- [ ] Log-linear model comparison uses BIC/Δ as well as G².
- [ ] Income-based persistence uses multi-year averages and rank measures where possible.
- [ ] Inequality measure chosen for its decomposability/sensitivity; equivalence scale stated.
