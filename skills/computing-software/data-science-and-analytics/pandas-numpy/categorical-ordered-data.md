---
id: computing-software.data-science-and-analytics.pandas-numpy.categorical-ordered-data
name: categorical-ordered-data
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [categorical-dtype, ordered-categories, cut-qcut]
level: practitioner
status: docs-checked
description: "Declare ordered categories for sorting and comparisons and bin numerics with cut and qcut into labelled intervals."
sources:
  - https://pandas.pydata.org/docs/user_guide/categorical.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Categoricals and binning
```python
sz = pd.CategoricalDtype(["S","M","L"], ordered=True)
df["size"] = df["size"].astype(sz)
df[df["size"] >= "M"]
df["band"] = pd.cut(df["age"], [0,18,65,120], labels=["child","adult","senior"], right=False)
```
## Gotchas
- Values not in the categories become NaN when converting to a categorical dtype.
- `cut` bins on fixed edges; `right=False` makes the bins left-closed.
- Ordered comparisons (`>`, `<`) work against a scalar, or between categoricals that are ordered with the same categories; other non-equality comparisons raise `TypeError`.
## Verify
- [ ] `df["band"].isna().sum()` is zero or explained.

## Checked

Method: docs-checked 2026-11-09 against the pandas categorical user guide (CategoricalDtype, pd.cut and comparisons sections, read via text conversion). Dropped the `qcut` line and its equal-counts claim, which that page does not cover.
