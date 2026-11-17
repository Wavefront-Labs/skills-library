---
id: computing-software.data-science-and-analytics.experiment-design.cuped-variance-reduction
name: cuped-variance-reduction
category: computing-software
field: data-science-and-analytics
product: experiment-design
tags: [cuped, pre-experiment-covariate, variance-reduction]
level: advanced
status: docs-checked
description: "Adjust the metric with a pre-experiment covariate (CUPED) to tighten intervals without biasing the estimate."
sources:
  - https://exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CUPED
```python
theta = np.cov(y, x)[0, 1] / np.var(x, ddof=1)     # x = same metric from the pre-experiment period
y_adj = y - theta * (x - x.mean())
```
Then run the usual test on `y_adj`. With the optimal theta = cov(Y, X) / var(X), variance is multiplied by (1 - rho^2), where rho is the correlation of Y and X; theta is the OLS slope of centred Y on centred X.
## Gotchas
- The covariate must not be affected by the experiment's treatment. Pre-experiment data guarantees this; so do covariates fixed when a user first appears (such as day of week of first visit). If treatment moves X, the estimate is biased: using clicks as covariate in a page-load-time experiment adjusts part of the effect away.
- Users without pre-period data: add a binary covariate for "appeared in the pre-period" and set the missing covariate to any constant (equivalent to stratifying on presence).
- The same theta must be used for control and treatment.
## Verify
- [ ] Adjusted mean difference is close to the raw one; the standard error is smaller.

## Checked
Confirmed in the CUPED paper (Deng, Xu, Kohavi, Walker, WSDM 2013): control variate form Y - theta(X - E(X)), optimal theta = cov(Y, X)/var(X), variance factor (1 - rho^2), OLS connection, independence requirement and the page-load/clicks bias example, missing pre-period handling with an indicator covariate, and that the same theta is used for both arms. Removed: the instruction to use the mean of x for users without pre-period data (the paper allows any constant plus an indicator) and the "pooled over arms" comment, which I could not confirm. Read the PDF as text (sections 3.2, 3.3, 4.2, 4.3 and the Bing example); the two-column layout made some formulas partly garbled.
Method: docs-checked 2026-11-09 against the CUPED paper PDF, downloaded and converted with pdftotext.
