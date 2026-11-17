---
id: computing-software.data-science-and-analytics.data-visualization.choose-the-right-chart
name: choose-the-right-chart
category: computing-software
field: data-science-and-analytics
product: data-visualization
tags: [chart-selection, comparison-vs-trend, small-multiples, viz-design]
level: intro
status: draft
description: "Map the question (comparison, trend, distribution, relationship, composition) to a chart type and prefer small multiples over cluttered overlays."
sources:
  - https://clauswilke.com/dataviz/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Chart selection
- Compare categories: sorted horizontal bars. Trend: line. Distribution: histogram/ECDF/box. Relationship: scatter. Composition: stacked bar (few parts); avoid pies beyond 2-3 slices.
- Many series: small multiples with shared axes.
- Ranking: bars sorted by value, not alphabetically.
## Gotchas
- 3-D effects and dual axes distort comparison.
- Order categories meaningfully; label directly rather than relying on a legend.
## Verify
- [ ] State the one message of the chart in a sentence; the title says it.
