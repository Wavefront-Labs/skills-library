---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.regression-diagnostics
name: regression-diagnostics
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [regression-diagnostics, vif-multicollinearity, cooks-distance]
level: advanced
status: docs-checked
description: "Check leverage, influence, multicollinearity and heteroscedasticity with statsmodels OLSInfluence, VIF and Breusch-Pagan."
sources:
  - https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.OLSInfluence.html
  - https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html
  - https://www.statsmodels.org/stable/generated/statsmodels.stats.diagnostic.het_breuschpagan.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnostics
```python
from statsmodels.stats.outliers_influence import OLSInfluence, variance_inflation_factor as vif
from statsmodels.stats.diagnostic import het_breuschpagan
infl = OLSInfluence(m)          # m: a fitted OLS results object
cooks = infl.cooks_distance; lev = infl.hat_matrix_diag
X = m.model.exog; [vif(X, i) for i in range(X.shape[1])]
lm, lm_p, f, f_p = het_breuschpagan(m.resid, m.model.exog)
```
## Gotchas
- `OLSInfluence(results)` assumes OLS results. `hat_matrix_diag`, `cooks_distance`, `resid_studentized_internal` need no leave-one-out loop; the `_external` measures, `dfbetas` and `dffits` do and are slower. The page recommends leave-one-out measures only for data sets that are not too large.
- `dffits_threshold` is 2 * sqrt(k / n), where k is the number of parameters; the page recommends investigating observations above it.
- `variance_inflation_factor(exog, exog_idx)` takes the whole design matrix and a column index. One recommendation on the page is that a VIF above 5 means the variable is highly collinear with the others and its estimates have large standard errors.
- `het_breuschpagan(resid, exog_het)` returns the LM statistic and p-value plus the F statistic and p-value. It assumes the exog contains a constant, and the page says the F statistic is preferable in small or moderately large samples. `robust=True` (default) is the Koenker version.
- Investigate high-influence points; do not auto-delete.
## Verify
- [ ] Residuals vs fitted and Q-Q plot inspected.

## Checked

2026-11-09. Confirmed against the statsmodels OLSInfluence, variance_inflation_factor and het_breuschpagan pages (signatures, attributes, dffits threshold, VIF recommendation of 5, constant-in-exog note, return values). Removed: the 5-10 VIF range, the claim that VIF inflates standard errors but not bias, the Cook's-distance tuple indexing, `get_influence`, and the remedies for heteroscedasticity and nonlinearity (not on the pages read).
Method: docs-checked 2026-11-09 against the three statsmodels pages named above, read in full.
