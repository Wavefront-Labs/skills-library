---
id: computing-software.data-science-and-analytics.data-visualization.honest-axes-and-scales
name: honest-axes-and-scales
category: computing-software
field: data-science-and-analytics
product: data-visualization
tags: [truncated-axis, log-scale, aspect-ratio-bank]
level: practitioner
status: draft
description: "Start bar charts at zero, justify truncated line axes, use log scales with labelled ticks and avoid misleading aspect ratios."
sources:
  - https://clauswilke.com/dataviz/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Honest axes
- Bars encode length: baseline must be zero. Lines/dots may use a non-zero range if marked.
- Log scale for multiplicative change; label ticks as plain numbers.
- Same units and scale across small multiples when comparing.
- Show uncertainty (intervals) where the number is an estimate.
## Gotchas
- Cumulative charts hide recent change; plot rates too.
- Indexing to 100 at a start date depends on that date; state it.
## Verify
- [ ] A reader can recover the actual values and units from the chart.
