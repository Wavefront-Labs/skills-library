---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.ols-formula-regression
name: ols-formula-regression
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [ols-regression, statsmodels-formula, regression-summary, st-regression]
level: practitioner
status: docs-checked
description: "Fit OLS with statsmodels formulas, read coefficient intervals and use robust or clustered standard errors via cov_type."
sources:
  - https://www.statsmodels.org/stable/generated/statsmodels.formula.api.ols.html
  - https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLS.fit.html
  - https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.get_robustcov_results.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OLS
```python
import statsmodels.formula.api as smf
m = smf.ols("price ~ sqft + C(region) + income", data=df).fit(cov_type="HC3")
print(m.summary()); m.conf_int()
# clustered errors need the group labels:
m2 = smf.ols("price ~ sqft", data=df).fit(cov_type="cluster", cov_kwds={"groups": df["group_id"]})
```
## Gotchas
- `smf.ols(formula, data)` builds the model from a formula and a data frame; the formula is evaluated by patsy in the calling namespace by default.
- `fit(cov_type=...)` defaults to `'nonrobust'`. The robust values `'HC0'`, `'HC1'`, `'HC2'`, `'HC3'` give heteroscedasticity-robust covariance and `'cluster'` gives a clustered estimator.
- `'cluster'` needs `groups`, an integer-valued index of clusters, passed through `cov_kwds`.
- `RegressionResults.conf_int([alpha])` returns the confidence interval of the fitted parameters.
- Coefficients are conditional on the other terms; interpret them "holding others fixed".
## Verify
- [ ] Residual plots and a held-out error check.

## Checked

2026-11-09. Confirmed against the statsmodels formula.api.ols page (formula, data, patsy namespace), OLS.fit page (cov_type default nonrobust) and RegressionResults.get_robustcov_results page (HC0 to HC3, cluster and its groups argument); conf_int listed on the RegressionResults page. Removed: the claim that C() makes dummies with a reference level, `predict`, and the advice on when to prefer HC3 (not stated on the pages). Fixed: the example shows the groups argument for clustering; the np.log term was dropped from the example formula as unconfirmed. C() is used on the statsmodels ANOVA page examples.
Method: docs-checked 2026-11-09 against the statsmodels OLS.fit, formula.api.ols and get_robustcov_results pages and the RegressionResults method listing.
