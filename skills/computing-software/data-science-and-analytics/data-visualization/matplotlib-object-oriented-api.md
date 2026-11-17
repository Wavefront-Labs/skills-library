---
id: computing-software.data-science-and-analytics.data-visualization.matplotlib-object-oriented-api
name: matplotlib-object-oriented-api
category: computing-software
field: data-science-and-analytics
product: data-visualization
tags: [matplotlib-oo-api, subplots-axes, pyplot-vs-oo, mpl-anatomy]
level: intro
status: docs-checked
description: "Create figures with plt.subplots and draw on Axes objects instead of implicit pyplot state to get predictable multi-panel charts."
sources:
  - https://matplotlib.org/stable/users/explain/quick_start.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OO API
```python
import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
axs[0].plot(x, y, label="obs")
axs[0].set_xlabel("Day"); axs[0].set_ylabel("Users"); axs[0].set_title("Daily users")
axs[0].legend()
axs[1].hist(v, bins=30)
```
## Gotchas
- The quick start describes two interfaces: explicitly create Figures and Axes and call methods on them (the object-oriented style), or rely on pyplot to create and manage them implicitly. This skill uses the explicit style.
- `plt.subplots()` returns a figure and one Axes, or an array of Axes for a grid such as `plt.subplots(2, 2)`; `subplot_mosaic` gives layouts where Axes span rows or columns.
- `layout="constrained"` is the layout argument the quick start passes to `plt.subplots` and `plt.figure`.
- Axes methods `set_title()`, `set_xlabel()` and `set_ylabel()` add the title and axis labels; `ax.legend()` adds a legend.
- Keep references to the Figure and Axes objects so you can add Artists to a specific one.
## Verify
- [ ] Every axis has a label with units, and the saved image is legible at final size.

## Checked

2026-11-09. Confirmed against the Matplotlib quick start guide (read the interfaces section and the code examples via keyword search of the stripped page, not every paragraph): subplots, layout="constrained", set_xlabel/set_ylabel/set_title, legend, hist, subplot_mosaic, explicit versus implicit interfaces. Removed: the `.set(...)` shortcut, `savefig` with dpi, `plt.close` in loops and the claim that constrained layout stops overlapping labels (not found on the page).
Method: docs-checked 2026-11-09 against the Matplotlib quick start page (searched for the specific calls above).
