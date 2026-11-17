---
id: computing-software.data-science-and-analytics.data-visualization.seaborn-distribution-plots
name: seaborn-distribution-plots
category: computing-software
field: data-science-and-analytics
product: data-visualization
tags: [seaborn-histplot, kde-ecdf, displot-hue, viz-seaborn]
level: practitioner
status: docs-checked
description: "Compare distributions with histplot, kdeplot and ecdfplot and violin or box plots, choosing bins and bandwidth with care."
sources:
  - https://seaborn.pydata.org/tutorial/distributions.html
  - https://seaborn.pydata.org/tutorial/categorical.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributions
```python
import seaborn as sns
sns.histplot(df, x="v", hue="group", stat="density", common_norm=False, bins=40)
sns.kdeplot(df, x="v", hue="group", cut=0)
sns.ecdfplot(df, x="v", hue="group")
sns.catplot(data=df, x="group", y="v", kind="box")
sns.catplot(data=df, x="group", y="v", kind="violin", cut=0)
```
## Gotchas
- The axes-level distribution functions are `histplot()`, `kdeplot()`, `ecdfplot()` and `rugplot()`; `displot()` is the figure-level wrapper and defaults to a histogram.
- `bins` can be an integer number of bins (for example `bins=20`) or an array of bin breaks (for example `bins=[1, 2, 3, 4, 5, 6, 7]`).
- With `hue`, normalisation is applied to the whole distribution by default; `common_norm=False` normalises each subset independently.
- KDE accuracy depends on the smoothing bandwidth: over-smoothing can erase meaningful features and under-smoothing can obscure the shape in noise. Adjust it to check robustness.
- `cut` controls how far a KDE curve extends beyond the extreme datapoints. It only changes where the curve is drawn; the estimate still smooths over the range where no data can exist, so it can be artificially low at the extremes.
- The ECDF directly represents each datapoint, so there is no bin size or smoothing parameter, and it suits comparing several distributions.
- Box plots show the three quartile values and extreme values, with whiskers reaching to points within 1.5 IQRs of the quartiles.
## Verify
- [ ] Try two bin widths and confirm the story holds.

## Checked

2026-11-09. Confirmed against the seaborn distributions tutorial (histplot/kdeplot/ecdfplot, bins, common_norm=False, stat="density", bandwidth, cut, ECDF advantages) and the categorical tutorial (catplot kinds box and violin, cut=0 with violin, boxplot quartile and 1.5 IQR whisker description). Both pages were searched by keyword rather than read end to end. Changed: violin and box examples now use catplot with kind, as in the tutorial; removed the direct violinplot call and the advice about KDE on bounded data beyond what the cut paragraph says.
Method: docs-checked 2026-11-09 against the seaborn distributions and categorical tutorial pages (keyword searched).
