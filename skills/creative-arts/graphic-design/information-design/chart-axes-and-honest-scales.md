---
id: creative-arts.graphic-design.information-design.chart-axes-and-honest-scales
name: chart-axes-and-honest-scales
category: creative-arts
field: graphic-design
product: information-design
tags: [graphic-design, information-design, chart-design, data-visualisation, chart-axes, truncated-axis, zero-baseline, log-scale, dual-axis, aspect-ratio, gridlines, tick-labels, lie-factor]
level: practitioner
status: draft
description: "Set chart axes honestly: zero baselines for bars, when lines may be truncated, log scales, avoiding dual axes, aspect ratio and banking, ticks, gridlines and labelling units."
sources:
  - https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/
  - https://github.com/Financial-Times/chart-doctor
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Chart axes and honest scales

**Goal:** scales that show the data's real proportions and are easy to read.

## Baselines
- **Bar and column charts must start at zero**: bar length encodes value, so a truncated axis exaggerates differences
  (Tufte's "lie factor" = size of effect in graphic / size in data; aim for ~1).
- **Line charts may start above zero** when the variation is the story (temperatures, stock prices) - but label the
  axis clearly and do not crop to manufacture drama. If zero is meaningful (unemployment rate), consider including it.
- Area charts: zero baseline (area encodes value).

## Scale types
- **Linear** by default.
- **Logarithmic** when data spans orders of magnitude or growth rates matter (epidemics, compound growth). Label
  "log scale" and use ticks at 1, 10, 100 or 1, 2, 5, 10. Many readers misread log charts - annotate.
- **Dual axes** (two y-scales): avoid; the crossing points are arbitrary and imply false correlations. Use two charts
  side by side, or index both series to 100 at a start date.

## Aspect ratio
Line slopes depend on the chart's width/height. "Banking to 45 degrees" (Cleveland): choose an aspect ratio where
the important slopes average about 45 degrees. Do not squash or stretch to exaggerate trends.

## Ticks, gridlines, labels
- 4-6 ticks at round numbers; light, thin gridlines (or none - direct labels instead).
- Units in the axis title or on the top tick (`$m`, `%`); thousands separators; consistent decimals.
- Rotated tick labels are hard to read - switch to horizontal bars or abbreviate.
- Time axes: equal intervals for equal time (missing years must leave gaps).

## Gotchas
- Default software axes often start at the data minimum for bars (Excel can) - check.
- Comparing charts side by side: use the **same scale** on all (or say clearly that they differ).

## Verify
- [ ] Bars start at zero; any truncated line axis is labelled and justified.
- [ ] No dual axes; units and scale type labelled; consistent scales across a set.
