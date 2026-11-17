---
id: computing-software.ai-ml-engineering.scikit-learn.poisson-and-tweedie-glms
name: poisson-and-tweedie-glms
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, poisson-regression, tweedie-regression, glm, exposure, insurance-pricing]
level: practitioner
status: verified
description: "Model counts, frequencies and insurance claims in scikit-learn with PoissonRegressor, GammaRegressor and TweedieRegressor, using exposure weights and deviance metrics."
sources:
  - https://scikit-learn.org/stable/modules/linear_model.html#generalized-linear-models
  - https://scikit-learn.org/stable/auto_examples/linear_model/plot_poisson_regression_non_normal_loss.html
  - https://scikit-learn.org/stable/auto_examples/linear_model/plot_tweedie_regression_insurance_claims.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Poisson / Tweedie GLMs

Least squares assumes constant variance and allows negative predictions. Counts and claim amounts have variance that grows with the mean and are non-negative. GLMs with a log link fix both.

## Which distribution
| Target | Estimator | Variance ~ |
|---|---|---|
| Counts / frequencies (events per exposure) | `PoissonRegressor` | mu |
| Positive continuous, skewed (claim severity, durations) | `GammaRegressor` | mu^2 |
| Non-negative with exact zeros + continuous (pure premium, total claims) | `TweedieRegressor(power=1.5, link="log")` | mu^p, 1<p<2 |

## Frequency with exposure
Model the rate `claims / exposure` and weight by exposure:
```python
from sklearn.linear_model import PoissonRegressor
from sklearn.metrics import mean_poisson_deviance
freq = df["ClaimNb"] / df["Exposure"]
glm = make_pipeline(preprocessor, PoissonRegressor(alpha=1e-4, max_iter=1000))
glm.fit(X_train, freq_train, poissonregressor__sample_weight=exposure_train)
pred_counts = glm.predict(X_test) * exposure_test
print(mean_poisson_deviance(freq_test, glm.predict(X_test), sample_weight=exposure_test))
```
Ran on simulated data (20000 policies): held-out weighted Poisson deviance 0.672 for the GLM against 0.698 for an exposure-weighted `DummyRegressor`; `exp(coef_)` recovered the area multiplier (1.39 for area B vs about 0.8 for the others, true effect e^0.5 = 1.65 before centring/regularisation).
This is equivalent to an offset of `log(exposure)` in classic GLM software.

## Pure premium (Tweedie)
Either frequency x severity (Poisson for counts, Gamma on positive claims weighted by claim count) or one Tweedie model on `amount / exposure`. Tune `power` (1.1-1.9) by deviance on validation data.

## Non-linear models with the same losses
`HistGradientBoostingRegressor(loss="poisson")` (also `"gamma"`); LightGBM `objective="poisson"`/`"tweedie"`; XGBoost uses different names: `objective="count:poisson"`, `"reg:tweedie"`, `"reg:gamma"` (plain `"poisson"` and `"tweedie"` raise `Unknown objective function` on XGBoost; all four accepted names ran with lightgbm 4.7.0 and xgboost installed from PyPI). Typically more accurate; the GLM remains the interpretable, regulator-friendly baseline.

## Metrics
- Use deviance matching the distribution: `mean_poisson_deviance`, `mean_gamma_deviance`, `mean_tweedie_deviance(power=...)`, or `d2_tweedie_score` (pseudo-R2).
- MSE/MAE ignore the variance structure and favour different models.
- Check calibration of totals: sum of predictions vs observed sum overall and per segment (Lorenz curve / Gini for ranking quality in pricing).

## Gotchas
- `alpha` is L2 strength (default 1.0 on Poisson, Gamma and Tweedie regressors, often too strong); scale numeric features; one-hot categoricals. `TweedieRegressor` defaults are `power=0.0` (normal distribution) and `link="auto"`, so always set `power` (and `link="log"`) explicitly.
- Gamma requires y > 0 strictly; Poisson requires y >= 0 (checked: Poisson accepted all-zero y and rejected negatives with `Some value(s) of y are out of the valid range of the loss 'HalfPoissonLoss'`; Gamma rejected zeros with the `HalfGammaLoss` message).
- Log link: coefficients are multiplicative effects: `exp(coef)` per unit change.
- Ordinary `LinearRegression` on `log(y+1)` is a different model (biased low on the original scale: on lognormal y, back-transformed predictions averaged 1.24 against a true mean of 1.67).

## Verify
Compare deviance on held-out data against a mean-only model (`DummyRegressor` weighted by exposure) and check that predicted total claims are within a few percent of actual.
