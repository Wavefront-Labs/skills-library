---
id: social-sciences.social-research-methods.social-statistics.regression-multilevel-and-missing-data-for-social-data
name: regression-multilevel-and-missing-data-for-social-data
category: social-sciences
field: social-research-methods
product: social-statistics
tags: [social-statistics, applied-statistics, regression, ols, logistic-regression, odds-ratio, average-marginal-effects, ordinal-regression, poisson, negative-binomial, multilevel-models, mixed-models, hierarchical-linear-models, random-intercepts, random-slopes, icc, lme4, mixed, missing-data, mcar, mar, mnar, multiple-imputation, mice, rubins-rules, listwise-deletion, measurement-error, reliability, cronbachs-alpha, clustered-standard-errors, survey-weights]
level: practitioner
status: gated
description: "Fit and report the models social data need: OLS and logit with marginal effects, count and ordinal models, multilevel models with ICC, and multiple imputation for missing data."
sources: ["Gelman, Hill & Vehtari, Regression and Other Stories (Cambridge 2020)", "Snijders & Bosker, Multilevel Analysis (2nd ed., Sage 2012)", "van Buuren, Flexible Imputation of Missing Data (2nd ed., CRC 2018)", "Mood (2010), European Sociological Review 26(1)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Social statistics — the right model, honest uncertainty, missing data

**Goal:** models whose structure matches how human-subjects data are generated —
categorical outcomes, people nested in places, gaps in the data — and results reported
in units a reader can interpret.

## 1. Match the model to the outcome
| Outcome | Model | Report |
|---|---|---|
| Continuous | OLS (robust SEs) | Coefficient in outcome units |
| Binary | Logit / probit (or linear probability model as a check) | **Average marginal effects** (percentage points) |
| Ordered categories | Ordered logit — test proportional odds | Predicted probabilities per category |
| Unordered categories | Multinomial logit | Predicted probabilities |
| Counts | Poisson with robust SEs, or negative binomial if overdispersed | Incidence rate ratios |

**Do not compare logit coefficients or odds ratios across models or groups** — they
are scaled by unobserved variance, so adding an uncorrelated covariate changes them (Mood
2010). Compare average marginal effects. Stata: `margins, dydx(*)`; R: `marginaleffects::avg_slopes()`.

## 2. Nesting: pupils in schools, people in neighbourhoods, waves in people
1. Fit an **empty model** (random intercept only) and compute the
   **ICC** = between-group variance / total variance. Even 0.05 matters with large groups.
2. Options:
   - **Cluster-robust SEs** when nesting is a nuisance and you have ≥ ~30–50 clusters.
   - **Multilevel (mixed) model** when group-level variation is of interest, or you need
     predictors at both levels. R: `lme4::lmer(y ~ x + (1 | school))`; Stata:
     `mixed y x || school:`. Binary: `glmer(..., family = binomial)` / `melogit`.
   - **Fixed effects** for groups when you want within-group estimates and do not trust
     that group effects are uncorrelated with predictors.
3. **Random slopes** only when theory says the effect varies by group and you have enough
   groups; otherwise models fail to converge or produce singular fits.
4. **Centre** level-1 predictors: group-mean centring separates within- from between-group
   effects; grand-mean centring does not.
5. Few groups (< ~20) make level-2 variance estimates unreliable; consider Bayesian
   estimation (`brms`) or fixed effects.

## 3. Missing data
- Diagnose: share missing per variable, patterns (`mice::md.pattern`, `misstable patterns`),
  and predictors of missingness.
- Mechanisms: **MCAR** (unrelated to anything), **MAR** (explained by observed variables),
  **MNAR** (depends on the missing value itself). You cannot test MAR vs MNAR from the data;
  argue it.
- **Listwise deletion** is unbiased under MCAR (and some MAR cases for regression) but wastes
  power. Mean imputation and missing-indicator dummies bias estimates — avoid.
- **Multiple imputation** under MAR: include the outcome and all analysis variables, plus
  auxiliary predictors of missingness, in the imputation model; match the model to the
  analysis (interactions, nesting). Use m ≥ the percentage of incomplete cases as a rough
  guide (often 20–50; White, Royston & Wood 2011, Statistics in Medicine, cited second-hand). Pool with Rubin's rules (`mice::pool`, `mi estimate:`).
- Run a sensitivity analysis (e.g. delta adjustment) for plausible MNAR.

## 4. Measurement error
- Report reliability of scales (Cronbach's alpha or, better, McDonald's omega) and check
  dimensionality first (factor analysis).
- Error in a predictor attenuates its coefficient toward zero and can bias others; latent
  variable models (SEM) correct for it.

## 5. Weights and design
With survey data, use design-based estimation (strata, PSUs, weights) — see
social-sciences.social-research-methods.survey-design.questionnaire-wording-sampling-and-weighting.

## Gotchas
- Interactions in logit: the product-term coefficient is not the interaction on the
  probability scale; plot predicted probabilities.
- Significance stars without effect sizes and intervals tell readers little.
- Standardised coefficients depend on the sample's variance; avoid comparing them across samples.

## Verify
- [ ] Model family matches outcome type; dispersion / proportional odds checked.
- [ ] Binary results reported as AMEs or predicted probabilities.
- [ ] ICC computed; clustering handled by a stated method.
- [ ] Missingness described; MI model includes outcome and auxiliaries; m justified.
- [ ] Scale reliability and dimensionality reported.
- [ ] Results reproducible from a script.

*Checked 2026-10-19 by simulation in statsmodels: omitting an uncorrelated covariate z shrinks the logit coefficient on x (0.668 vs 0.799, true 0.8 in latent-logistic scale) while the average marginal effect is unchanged (0.1517 vs 0.1517); a random-intercept model recovers ICC 0.205 vs true 0.20. The R (`lme4`, `mice`, `marginaleffects`, `brms`) and Stata (`margins`, `mixed`, `mi estimate`) commands were not run (gated: unconfirmed, source is paywalled or blocked). Cluster-count thresholds are rules of thumb, not hard limits.*
