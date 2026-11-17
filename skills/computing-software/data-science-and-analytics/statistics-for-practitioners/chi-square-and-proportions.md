---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.chi-square-and-proportions
name: chi-square-and-proportions
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [chi-square-test, fisher-exact, proportions-ztest]
level: practitioner
status: docs-checked
description: "Test independence in contingency tables with chi-square or Fisher exact and compare proportions with z-tests from statsmodels."
sources:
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html
  - https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportions_ztest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Categorical tests
```python
chi2, p, dof, exp = stats.chi2_contingency(table)
```
## Gotchas
- `chi2_contingency(observed, correction=True, ...)`: with 1 degree of freedom, Yates' continuity correction adjusts each observed value 0.5 towards the expected value. Pass `correction=False` if you do not want it.
- The expected frequencies are computed from the marginal sums under independence and returned for inspection.
- statsmodels provides `proportions_ztest` (`statsmodels.stats.proportion`) for proportion tests.
- Significance does not give effect size; report rates and difference.

## Verify
- [ ] Observed and expected tables printed and compared.

## Checked

2026-11-02. Confirmed against scipy.stats.chi2_contingency (signature, Yates correction at 1 dof, expected frequencies) and the statsmodels proportions_ztest page (existence and module). Removed: fisher_exact, proportion_confint, and the expected count at least 5 rule (not on the pages read).
Method: documentation only; no commands were run.
