---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.one-way-anova-posthoc
name: one-way-anova-posthoc
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [anova-oneway, tukey-hsd, statsmodels-anova, st-anova-multiple]
level: practitioner
status: docs-checked
description: "Compare several group means with anova_lm on a formula model and follow with Tukey HSD or Games-Howell pairwise comparisons."
sources:
  - https://www.statsmodels.org/stable/anova.html
  - https://www.statsmodels.org/stable/generated/statsmodels.stats.anova.anova_lm.html
  - https://www.statsmodels.org/stable/generated/statsmodels.stats.multicomp.pairwise_tukeyhsd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ANOVA
```python
import statsmodels.formula.api as smf, statsmodels.api as sm
m = smf.ols("y ~ C(group)", data=df).fit()
sm.stats.anova_lm(m, typ=2)
from statsmodels.stats.multicomp import pairwise_tukeyhsd
res = pairwise_tukeyhsd(df["y"], df["group"], alpha=0.05)   # use_var="unequal" gives Games-Howell
print(res.summary())
```
## Gotchas
- `anova_lm` needs models fitted with the formula API. The result table has columns `sum_sq`, `df`, `F` and `PR(>F)`.
- `typ` defaults to Type I (sequential), whose results depend on term order when the design is unbalanced. Type II tests each term after all others except higher-order terms containing it, and suits designs without interactions of interest. Type III tests each term after all others, including interactions, and can depend on the contrast coding.
- `robust="hc3"` gives a heteroscedasticity-corrected covariance in `anova_lm`; the page recommends hc3 if robust covariance is wanted.
- Tukey HSD assumes equal within-group variances and is not robust to unequal variances, especially with unequal group sizes. `use_var="unequal"` returns Games-Howell p-values (Welch t-tests with Satterthwaite degrees of freedom).
- The Tukey results hold `reject`, adjusted `pvalues`, `summary()` and `summary_frame()`.
## Verify
- [ ] Residuals vs fitted show no strong pattern.

## Checked

2026-11-09. Confirmed against the statsmodels ANOVA page, the anova_lm page (parameters, typ defaults and Type I/II/III notes, robust option, output columns) and the pairwise_tukeyhsd page (signature, use_var, heteroscedasticity note, results attributes). Removed: the advice to check residual plots rather than raw group normality and the pointer to Welch ANOVA (not on the pages read).
Method: docs-checked 2026-11-09 against the three statsmodels pages named above, read in full.
