---
id: computing-software.data-science-and-analytics.statistics-for-practitioners.multiple-testing-correction
name: multiple-testing-correction
category: computing-software
field: data-science-and-analytics
product: statistics-for-practitioners
tags: [multiple-testing, benjamini-hochberg, bonferroni-holm]
level: practitioner
status: docs-checked
description: "Adjust p-values for many tests with Bonferroni, Holm and Benjamini-Hochberg via statsmodels multipletests."
sources:
  - https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple testing
```python
from statsmodels.stats.multitest import multipletests
rej, p_adj, alpha_sidak, alpha_bonf = multipletests(pvals, alpha=0.05, method="fdr_bh")   # or "holm", "bonferroni"
```
## Gotchas
- Decide the family of tests before looking at results.
- `pvals` must be 1-dimensional. Method names include `bonferroni`, `sidak`, `holm`, `holm-sidak`, `simes-hochberg`, `hommel`, `fdr_bh` (Benjamini/Hochberg) and `fdr_by` (Benjamini/Yekutieli). The default is `holm-sidak` (`'hs'`).
- The corrected p-values come back in the original order. Except for the two-stage FDR methods they do not depend on `alpha`, so they can be compared with a different alpha.
- `hommel` is very slow for large arrays.
- Slicing a metric many ways without correction manufactures significance.
## Verify
- [ ] Report both raw and adjusted p-values and how many tests were run.

## Checked

2026-11-09. Confirmed against the statsmodels multipletests reference page: function signature and defaults, the method list, the four return values (reject, corrected p-values, alphacSidak, alphacBonf), original-order output, alpha independence except for two-stage FDR, and the hommel timing note. Removed: the claim about which method families control family-wise error versus false discovery rate (the page only says the procedures control FWER or FDR in the independent case).
Method: docs-checked 2026-11-09 against the statsmodels multipletests page, read in full.
