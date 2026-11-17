---
id: computing-software.data-science-and-analytics.data-visualization.seaborn-heatmaps-regression
name: seaborn-heatmaps-regression
category: computing-software
field: data-science-and-analytics
product: data-visualization
tags: [seaborn-heatmap]
level: practitioner
status: docs-checked
description: "Draw annotated seaborn heatmaps with explicit colour limits and a centred colour map for divergent data such as correlations."
sources:
  - https://seaborn.pydata.org/generated/seaborn.heatmap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heatmaps
```python
import seaborn as sns
sns.heatmap(df[cols].corr(), annot=True, fmt=".2f", center=0, vmin=-1, vmax=1, square=True)
```
## Gotchas
- `center` sets the value at which to centre the colour map for divergent data, and changes the default `cmap` if none is given. If `cmap` is not provided, the default depends on whether `center` is set.
- `vmin` and `vmax` fix the colour range; with `robust=True` and no `vmin` or `vmax`, the range uses robust quantiles instead of extreme values.
- `annot=True` writes the value in each cell; `fmt` is the string format for annotations (default `.2g`). `annot` can also be a same-shaped table of labels, matched by position, not index.
- `square=True` sets the aspect to equal so each cell is square.
## Verify
- [ ] Colour bar limits are explicit and labelled.

## Checked

2026-11-09. Confirmed against the seaborn.heatmap reference page: signature and defaults, center, vmin/vmax, robust, annot, fmt, square. Removed: the lmplot example, the vlag colour map, the sequential-versus-diverging rule and the regression gotchas (not on the heatmap page); trimmed tags regplot-lmplot and clustermap for the same reason.
Method: docs-checked 2026-11-09 against the seaborn.heatmap reference page, searched by parameter name.
