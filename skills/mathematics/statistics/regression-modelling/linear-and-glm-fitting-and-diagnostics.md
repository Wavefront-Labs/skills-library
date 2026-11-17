---
id: mathematics.statistics.regression-modelling.linear-and-glm-fitting-and-diagnostics
name: linear-and-glm-fitting-and-diagnostics
category: mathematics
field: statistics
product: regression-modelling
tags: [statistics, regression-modelling, regression, linear-regression, ols, glm, generalised-linear-model, logistic-regression, poisson-regression, negative-binomial, overdispersion, mixed-effects, lme4, residuals, residual-diagnostics, heteroscedasticity, robust-standard-errors, multicollinearity, vif, interaction, odds-ratio, model-selection, statsmodels, r]
level: practitioner
status: gated
description: "Fit and check linear and generalised linear models: choose the family, read coefficients correctly, run residual diagnostics, handle overdispersion and clustering."
sources:
  - https://www.statsmodels.org/stable/example_formulas.html
  - https://patsy.readthedocs.io/en/latest/spline-regression.html
  - https://cran.r-project.org/package=logistf
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Linear and GLM fitting and diagnostics

**Goal:** fit a regression whose coefficients mean what you say they mean, and
whose standard errors you can trust.

## 1. Choose the model from the outcome
| Outcome | Model | Link | Coefficient reads as |
|---|---|---|---|
| Continuous, roughly symmetric | Linear (OLS) | identity | change in y per unit x |
| Positive, right-skewed | Linear on log(y), or Gamma GLM | log | ≈ % change (exp(b) − 1) |
| Binary 0/1 | Logistic | logit | log-odds; exp(b) = odds ratio |
| Counts | Poisson → negative binomial if overdispersed | log | exp(b) = rate ratio |
| Counts per exposure | Poisson/NB with `offset(log(exposure))` | log | rate per unit exposure |
| Grouped/repeated rows | Mixed model (random intercepts) or cluster-robust SEs | — | — |

R: `lm(y ~ x1 + x2)`, `glm(y ~ x, family = binomial)`, `MASS::glm.nb`, `lme4::lmer(y ~ x + (1|id))`.
Python: `statsmodels.formula.api.ols/glm/mixedlm`.

## 2. Prepare predictors
- **Centre continuous predictors** (subtract the mean) so the intercept is meaningful
  and interactions are interpretable. Scale by 1 or 2 SD to compare effects.
- **Categorical variables:** know your reference level; change it deliberately
  (`relevel()` in R, `C(x, Treatment('b'))` in statsmodels).
- **Nonlinearity:** use splines (`splines::ns(x, 3)`; in statsmodels formulas `bs(x, df=3)`, or `cr(x, df=3, constraints='center')` / `cr(x, df=3) - 1`, because a bare `cr(x, df=3)` alongside the intercept is rank-deficient and statsmodels warns) rather than
  guessing polynomial degrees.
- **Interactions:** include both main effects. With `x * group`, the "main effect" of x
  is its slope *in the reference group* — a classic misreading.

## 3. Diagnostics (linear models)
Plot, don't test:
1. **Residuals vs fitted** — curvature means missing nonlinearity; a funnel means
   heteroscedasticity → use robust (HC3) SEs or model log(y).
2. **QQ plot of residuals** — matters for prediction intervals and small n, less for coefficients.
3. **Scale-location** — confirms variance pattern.
4. **Leverage / Cook's distance** — points with Cook's D well above the rest deserve a
   look; refit without them to see if conclusions change, but don't silently drop them.
R: `plot(fit)`; Python: `sm.graphics.plot_regress_exog`, `fit.get_influence()`.

## 4. Diagnostics (GLMs)
- Raw residuals are useless for logistic models; use **randomised quantile residuals**
  (R `DHARMa`) or binned residual plots.
- **Overdispersion check** for Poisson: Pearson χ² / residual df. Well above 1
  (rule of thumb > 1.5) (gated: unconfirmed, source is paywalled or blocked) → switch to negative binomial or quasi-Poisson; otherwise SEs
  are too small and p-values too optimistic.
- **Separation** in logistic regression (a predictor perfectly predicts y) gives huge
  coefficients and SEs; use Firth's penalised logistic (`logistf`) or a weak prior.
- **Calibration** for prediction: compare predicted vs observed proportions in deciles.

## 5. Multicollinearity
VIF > ~5–10 (gated: unconfirmed, source is paywalled or blocked) means coefficients are unstable and individually uninterpretable, though
predictions may be fine. Don't drop variables only for this if they're needed for
confounding control; combine them or accept wide CIs.

## 6. Model selection without fooling yourself
- Decide confounders from subject knowledge (see the causal-inference skill
  mathematics.statistics.causal-inference.confounding-control-with-dags-and-propensity-scores),
  not stepwise p-values. Stepwise selection biases coefficients and understates SEs.
- For prediction, compare by cross-validation or AIC; for explanation, pre-specify.
- Rule of thumb: ~10–20 observations (or events, for logistic) per estimated parameter. (gated: unconfirmed, source is paywalled or blocked)

## Gotchas
- R² says nothing about whether coefficients are causal or correct.
- Log-transforming y with zeros: `log(y + 1)` makes coefficients scale-dependent; prefer
  a Poisson/Gamma GLM with log link.
- Logistic odds ratios overstate risk ratios when the outcome is common (>10%).
- Repeated measures treated as independent rows understate SEs — the most common
  real-world error.
- Uncertain: the overdispersion threshold of 1.5 and VIF cutoffs are conventions, not tests.

## Verify
- [ ] Family/link matches the outcome type; offsets used for exposure.
- [ ] Reference levels and centring are known and stated.
- [ ] Residual plots show no curvature or funnel (or robust SEs are used).
- [ ] Overdispersion and separation checked for GLMs.
- [ ] Clustering handled with mixed models or cluster-robust SEs.
- [ ] Coefficients reported on an interpretable scale (OR, rate ratio, % change) with CIs.
