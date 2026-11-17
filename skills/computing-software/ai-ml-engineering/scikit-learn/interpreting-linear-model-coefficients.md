---
id: computing-software.ai-ml-engineering.scikit-learn.interpreting-linear-model-coefficients
name: interpreting-linear-model-coefficients
category: computing-software
field: ai-ml-engineering
product: scikit-learn
tags: [scikit-learn, coefficient-interpretation, linear-models, standardized-coefficients, multicollinearity, odds-ratio]
level: practitioner
status: verified
description: "Interpret scikit-learn linear model coefficients correctly: units and scaling, conditional effects, collinearity, regularisation bias, coefficient variability across CV folds."
sources:
  - https://scikit-learn.org/stable/auto_examples/inspection/plot_linear_model_coefficient_interpretation.html
  - https://scikit-learn.org/stable/modules/linear_model.html
  - https://www.statsmodels.org/stable/regression.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interpreting linear model coefficients

A coefficient is the change in prediction for a one-unit change in that feature **holding all other features fixed**, in the model's units. Most misreadings break one of those clauses.

## Units and scale
- Raw features: coefficient magnitude depends on units (income in dollars vs thousands). Never rank raw coefficients by size.
- Standardised features (`StandardScaler` in the pipeline): effect per one standard deviation; comparable across features. Or multiply raw coefficients by each feature's std.
- Log-transformed target (`TransformedTargetRegressor(func=np.log1p, ...)`): coefficient ~ relative change in y (exp(coef) - 1 per unit).
- Logistic regression: coefficients are log-odds; `exp(coef)` is an odds ratio per unit (or per SD if standardised).
- One-hot categoricals: each coefficient is relative to the dropped/reference category (or to the intercept balance when none is dropped with regularisation).

## Conditional, not marginal
A coefficient can have the opposite sign from the simple correlation because it's conditional on other features (e.g. "years of experience" negative once "age" is included). Explain the conditioning.

## Collinearity
Correlated features make coefficients unstable: they trade off, signs flip between folds, magnitudes balloon. Diagnose:
```python
from sklearn.model_selection import cross_validate, RepeatedKFold
cv = cross_validate(pipe, X, y, cv=RepeatedKFold(n_splits=5, n_repeats=5, random_state=0), return_estimator=True)
coefs = pd.DataFrame([e[-1].coef_ for e in cv["estimator"]],
                     columns=cv["estimator"][0][:-1].get_feature_names_out())   # `pipe` itself is unfitted
coefs.boxplot(vert=False)                   # wide boxes / boxes crossing 0 = unreliable
```
In a test with a feature duplicated plus 1% noise, the per-fold coefficient std across 25 fits was about 17.7 for both features and the VIF was about 10,000 (`variance_inflation_factor`, statsmodels). Also variance inflation factors (`statsmodels.stats.outliers_influence.variance_inflation_factor`). Remedies: drop or combine features, Ridge, or interpret groups jointly.

## Regularisation bias
Ridge/Lasso shrink coefficients toward 0: magnitudes are biased low, Lasso zeroes are not proof of no effect (another correlated feature took it). sklearn gives no standard errors; for confidence intervals and p-values fit an unpenalised `statsmodels.OLS`/`Logit` with robust standard errors, and check assumptions.

## Prediction model is not a causal model
Coefficients describe associations given the included features. Omitted confounders, colliders and reverse causation change them. Don't tell stakeholders "increasing X by 1 raises Y by b" without a causal design.

## Verify
Coefficients stable in sign and roughly in size across CV folds; interpretation statements tested by the pipeline's own `get_feature_names_out()` mapping (misaligned names after ColumnTransformer are a common bug).
