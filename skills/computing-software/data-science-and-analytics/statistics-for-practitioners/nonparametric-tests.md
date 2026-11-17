---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.nonparametric-tests
name: nonparametric-tests
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [mann-whitney, wilcoxon-signed-rank, kruskal-wallis]
level: practitioner
status: docs-checked
description: "Apply Mann-Whitney, Wilcoxon and Kruskal-Wallis when normality or interval-scale assumptions fail, and state what each actually tests."
sources:
  - https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rank-based tests
```python
stats.mannwhitneyu(a, b, alternative="two-sided")
```
## Gotchas
- `mannwhitneyu(x, y, use_continuity=True, alternative='two-sided', axis=0, method='auto', ...)`; `alternative` is `'two-sided'`, `'less'` or `'greater'`.
- The `'asymptotic'` method corrects for ties; the `'exact'` method makes no correction for ties, so many ties degrade it.

## Verify
- [ ] Report an effect size alongside the p-value.

## Checked

2026-11-02. Confirmed against scipy.stats.mannwhitneyu (signature, alternative values, ties behaviour of exact vs asymptotic). Removed: wilcoxon and kruskal calls, the stochastic-dominance statement, probability-of-superiority wording (pages not read).
Method: documentation only; no commands were run.
