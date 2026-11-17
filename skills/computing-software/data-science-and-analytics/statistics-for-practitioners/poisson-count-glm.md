---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.poisson-count-glm
name: poisson-count-glm
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [poisson-regression, glm-families, overdispersion]
level: advanced
status: docs-checked
description: "Model counts with Poisson or negative binomial GLMs in statsmodels and use exposure or offset terms."
sources:
  - https://www.statsmodels.org/stable/glm.html
  - https://www.statsmodels.org/stable/generated/statsmodels.genmod.generalized_linear_model.GLM.html
  - https://www.statsmodels.org/stable/generated/statsmodels.genmod.families.family.Poisson.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Count GLM
```python
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
m = smf.glm("claims ~ age + C(region)", data=df, family=sm.families.Poisson(),
            offset=np.log(df["exposure"])).fit()
m.pearson_chi2 / m.df_resid          # Pearson chi-square per residual degree of freedom
```
## Gotchas
- `GLM` accepts `offset` (added to the linear predictor with coefficient fixed at 1) and `exposure` (log of it is added; only valid with the log link). Poisson uses the log link by default.
- Exposure goes in as an offset or `exposure`, not as an ordinary covariate.
- `sm.families.NegativeBinomial` is available for count data (NB2 form, with an `alpha` parameter).
- The log-likelihood and deviance are not valid in models where scale is fixed at 1 (Binomial, NegativeBinomial, Poisson) when variance weights are used; AIC and likelihood-ratio tests based on them are not appropriate then.
- `pearson_chi2` and `df_resid` are attributes of the GLM results.
## Verify
- [ ] Compare the Pearson chi-square per degree of freedom before and after switching to the negative binomial family.

## Checked

2026-11-09. Confirmed against the statsmodels GLM page (offset and exposure parameters, df_resid, pearson_chi2, scale-1 warning), Poisson family page (log default link) and the GLM overview (NegativeBinomial family, NB2). The formula.api.glm page lists the entry point (read signature only). Removed: the rule that a ratio well above 1 means overdispersion, quasi-Poisson standard errors, and zero-inflated model advice (not on the pages read). Fixed: the example now imports numpy and statsmodels.formula.api.
Method: docs-checked 2026-11-09 against the three statsmodels pages named above and the formula.api.glm signature.
