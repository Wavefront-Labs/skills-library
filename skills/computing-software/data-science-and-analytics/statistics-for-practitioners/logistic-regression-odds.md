---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.logistic-regression-odds
name: logistic-regression-odds
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [logistic-regression, odds-ratio, logit-statsmodels, st-glm]
level: practitioner
status: draft
description: "Model binary outcomes with logit, convert coefficients to odds ratios and evaluate with ROC AUC and calibration."
sources:
  - https://www.statsmodels.org/stable/discretemod.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Logit
```python
m = smf.logit("churn ~ tenure + C(plan)", data=df).fit()
np.exp(m.params); np.exp(m.conf_int())          # odds ratios with CI
from sklearn.metrics import roc_auc_score
roc_auc_score(df["churn"], m.predict(df))
```
## Gotchas
- Perfect separation causes non-convergence; regularise or drop the offender.
- Odds ratios are not risk ratios when outcomes are common.
- Rare outcomes: accuracy is meaningless; use AUC/PR and calibration.
## Verify
- [ ] Calibration (predicted vs observed rate by decile).
