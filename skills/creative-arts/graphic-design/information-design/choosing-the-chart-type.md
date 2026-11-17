---
id: creative-arts.graphic-design.information-design.choosing-the-chart-type
name: choosing-the-chart-type
category: creative-arts
field: graphic-design
product: information-design
tags: [graphic-design, information-design, chart-design, data-visualisation, chart-selection, comparison, distribution, composition, relationship, change-over-time, ft-visual-vocabulary, perceptual-ranking]
level: practitioner
status: draft
description: "Pick the chart type from the question the data answers (comparison, change, distribution, part-to-whole, relationship, ranking, geography) using perceptual accuracy, not habit."
sources:
  - https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary
  - https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing the chart type

**Goal:** a chart whose form makes the intended comparison effortless.

## Start with the message
Write the one-sentence takeaway first ("Sales in Asia overtook Europe in 2023"). The chart's job is to show that
comparison. Then choose by relationship type (FT Visual Vocabulary categories):
| Relationship | Good forms | Avoid |
|---|---|---|
| **Magnitude / comparison** | bar (horizontal for long labels), dot plot, grouped bars (2-3 groups max) | 3D bars, radial bars |
| **Change over time** | line (many points), column (few periods), slope chart (two points), area (cumulative) | pie per year |
| **Ranking** | ordered bar, dot plot, bump chart (rank over time) | unordered bars |
| **Part-to-whole** | stacked bar (100%), waffle, treemap; **pie/donut only for 2-3 parts** | pies with 6+ slices |
| **Distribution** | histogram, box plot, violin, strip/beeswarm | average-only bars |
| **Correlation / relationship** | scatter (+ trend line), bubble (third variable), connected scatter | dual-axis line charts (misleading) |
| **Deviation** | diverging bar, surplus/deficit area | |
| **Geography** | choropleth (rates, not counts), proportional symbol map (counts) | choropleth of raw totals |
| **Flow** | Sankey, waterfall (cumulative changes) | |

## Perceptual accuracy (Cleveland and McGill)
People judge **position on a common scale** most accurately, then length, then angle/slope, area, volume, colour
saturation. So bars and dots beat pies and bubbles for precise comparison; use area/colour when precision matters less
than overview.

## Practical rules
- Sort bars by value unless the category order is meaningful (time, age groups).
- Bars start at zero (see axes skill); lines need not.
- More than ~5 lines: highlight one or two, grey the rest, or use small multiples (see small multiples).
- If a table answers the question better (exact values, few numbers), use a table (see data tables skill).

## Verify
- [ ] Takeaway sentence written; chart form matches its relationship type.
- [ ] A colleague states the takeaway within 5 seconds of seeing the chart.
