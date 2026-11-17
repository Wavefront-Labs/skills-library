---
id: computing-software.data-science-and-analytics.data-visualization.matplotlib-styling-export
name: matplotlib-styling-export
category: computing-software
field: data-science-and-analytics
product: data-visualization
tags: [matplotlib-style, savefig-formats, rcparams]
level: practitioner
status: gated
description: "Set rcParams or style sheets once, choose vector or raster export and size figures for print or slides."
sources:
  - https://matplotlib.org/stable/users/explain/customizing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Style and export
```python
plt.style.use("seaborn-v0_8-whitegrid")     # style names depend on version; list plt.style.available
plt.rcParams.update({"font.size": 11})
```
## Gotchas
- Matplotlib styles and defaults are customised through rcParams and style sheets; the shipped style list includes `seaborn-v0_8-whitegrid`.
- `font.size` is the default font size in points; the default `dpi` rcParam is 100.
- `savefig` arguments (`dpi`, `bbox_inches`), SVG vs PNG scaling and the spine settings: not covered by the customizing page read (gated: unconfirmed, source is paywalled or blocked). Check the `Figure.savefig` reference.

## Verify
- [ ] Open the exported file at target size.

## Checked

2026-11-02. Confirmed against the Matplotlib customizing page (style list incl. seaborn-v0_8-whitegrid, font.size, dpi default 100, rcParams). Gated: savefig options and raster/vector behaviour; source not read (savefig reference not fetched), not unreadable.
Method: documentation only; no commands were run.
