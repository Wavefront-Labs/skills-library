---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.t-tests-welch-paired
name: t-tests-welch-paired
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [t-test, welch-test, paired-t-test, st-hypothesis-tests]
level: practitioner
status: docs-checked
description: "Choose between Welch, paired and one-sample t-tests, run them in SciPy and report effect size with a confidence interval, not just p."
sources:
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# t-tests
```python
stats.ttest_ind(a, b, equal_var=False)       # Welch's t-test
```
## Gotchas
- `ttest_ind` defaults to `equal_var=True` (assumes identical population variances); `equal_var=False` runs Welch's test, which does not assume equal variances.
- The result object has a `confidence_interval(confidence_level=0.95)` method.
- Pairing is a design property, not a choice made after seeing p; paired designs need a paired test (see the SciPy `ttest_rel` page).
- Report the mean difference and its interval.

## Verify
- [ ] Sanity check sign and magnitude of the difference against group means.

## Checked

2026-11-02. Confirmed against scipy.stats.ttest_ind (signature, equal_var default and Welch behaviour, confidence_interval method). Removed: ttest_rel and ttest_1samp calls and the Cohen's d formula (pages not read), "Welch default choice" opinion.
Method: documentation only; no commands were run.
