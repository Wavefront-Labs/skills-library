---
id: computing-software.data-science-and-analytics.experiment-design.propensity-score-matching
name: propensity-score-matching
category: computing-software
field: data-science-and-analytics
product: experiment-design
tags: [propensity-score, inverse-probability-weighting, covariate-balance]
level: advanced
status: draft
description: "Model treatment assignment, weight or match on the score, and check covariate balance before estimating effects."
sources:
  - https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Propensity scores
```python
from sklearn.linear_model import LogisticRegression
ps = LogisticRegression(max_iter=1000).fit(X, t).predict_proba(X)[:, 1]
w = np.where(t == 1, 1/ps, 1/(1-ps))                 # IPW for ATE; trim extreme ps
ate = np.average(y[t==1], weights=w[t==1]) - np.average(y[t==0], weights=w[t==0])
```
Check standardised mean differences (|SMD| < 0.1) after weighting; plot propensity overlap.
## Gotchas
- Only measured confounders are handled; unmeasured confounding remains.
- Near-0/1 scores give unstable weights: trim or stabilise.
## Verify
- [ ] Balance table before vs after weighting.
