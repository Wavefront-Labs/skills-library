---
id: computing-software.data-science-and-analytics.data-visualization.matplotlib-dates-annotations
name: matplotlib-dates-annotations
category: computing-software
field: data-science-and-analytics
product: data-visualization
tags: [matplotlib-dates, annotate-plot, twin-axes]
level: practitioner
status: draft
description: "Format date axes, annotate key events and use secondary axes sparingly so time series charts stay readable."
sources:
  - https://matplotlib.org/stable/gallery/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dates and annotations
```python
import matplotlib.dates as mdates
ax.xaxis.set_major_locator(mdates.MonthLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.annotate("Launch", xy=(d, v), xytext=(d, v*1.2), arrowprops=dict(arrowstyle="->"))
ax.axvspan(start, end, alpha=0.15)
ax2 = ax.twinx()       # dual axis misleads easily; prefer two stacked panels
```
## Gotchas
- Dual axes let you imply any correlation by choosing scales.
## Verify
- [ ] Axis labels, units and dates readable without zooming.
