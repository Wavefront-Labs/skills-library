---
id: creative-arts.graphic-design.information-design.chart-and-infographic-design
name: chart-and-infographic-design
category: creative-arts
field: graphic-design
product: information-design
tags: [graphic-design, information-design, infographic, data-visualisation, data-visualization, dataviz, chart-design, bar-chart, line-chart, pie-chart, scatter-plot, small-multiples, annotation, colour-palette, colorblind-safe, direct-labelling, data-ink, chartjunk, tufte, datawrapper, flourish, illustrator, accessibility]
level: practitioner
status: draft
description: "Design honest, readable charts and infographics: state the takeaway, pick the chart by the comparison, start bars at zero, label directly, use colour for meaning, and annotate the point."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Chart and infographic design — show the point, honestly

**Goal:** a graphic where a reader gets the main finding in a few seconds, can check
it against accurate scales, and isn't misled by design choices.

## 1. Write the takeaway first
One sentence: "Rents rose twice as fast as wages since 2015." The chart exists to
make that sentence visible; it becomes the title (an **active title** states the
finding, not just "Rent and wages, 2015–2025").

## 2. Pick the chart by the comparison
| Comparison | Default chart |
|---|---|
| Categories against each other | Horizontal bar (long labels fit), sorted by value |
| Change over time | Line (many points) or columns (few periods) |
| Part of a whole | Stacked bar or a single 100% bar; pie only for 2–3 parts |
| Relationship between two variables | Scatter plot |
| Distribution | Histogram, box plot, dot/strip plot |
| Many series | Small multiples (same axes, repeated) instead of a spaghetti chart |
| Geography | Choropleth only for rates/normalised values; otherwise symbols on a map |
Humans judge position and length best, angle and area worse, colour intensity worst —
so bars and dots beat pies, bubbles and heat maps for precise comparison.

## 3. Honesty rules
- **Bar charts start at zero.** Bar length encodes value; a truncated axis exaggerates.
  Line charts may start elsewhere when the range matters — mark it clearly.
- Don't use **3D** effects or perspective — they distort length and area.
- Scale **area** symbols by area, not by radius (a common error that squares the visual difference).
- Show the **data source and date** under every chart; note sample size and
  definitions where relevant.
- Normalise maps and comparisons (per capita, per 100,000) when population differs.
- Consistent axes across small multiples, unless explicitly labelled otherwise.

## 4. Reduce, label, annotate
- Remove what doesn't carry information: heavy gridlines (keep light ones or none),
  borders, background fills, redundant tick labels, legends you can replace.
- **Label directly** — put series names at the end of lines and values on bars instead of a legend.
- **Annotate** the moment that matters: a short text note and a line pointing at the
  spike, the policy change, the outlier.
- Round numbers to the precision readers need.

## 5. Colour with meaning
- Use grey for context and **one highlight colour** for the story series.
- Sequential palettes (light→dark) for ordered values; diverging (two hues meeting at a
  neutral midpoint) for above/below a meaningful centre; categorical for unrelated groups (≤6–8).
- Check colour-blind safety (simulators in Illustrator/Photoshop View › Proof Setup,
  or tools like Color Oracle) and don't rely on red/green alone; add labels or patterns.
- Ensure text contrast meets WCAG (4.5:1 for small text).

## 6. Infographics: structure the story
- Lay out as a reading path: headline → key number → supporting charts → detail → source.
- Icons and illustration support, not replace, data. Pictograms (isotype-style rows
  of icons) work for countable quantities when each icon equals a stated unit.
- Tools: Datawrapper and Flourish for accurate, accessible charts; export SVG to
  Illustrator for styling. Draw charts from data, not by hand, to keep them accurate.

## Gotchas
- **Dual-axis charts** invite false correlations; prefer two aligned charts.
- **Restyling in Illustrator** can break accuracy — never resize individual bars by eye.
- **Pie charts with many slices** or similar values are unreadable; sort and use bars.
- Perception ranking follows well-known research (Cleveland & McGill); other numbers
  here are conventions.

## Verify
- [ ] Active title states the finding.
- [ ] Chart type matches the comparison; bars start at zero; no 3D.
- [ ] Direct labels and one annotation for the key point; legend removed where possible.
- [ ] Colour encodes meaning, passes colour-blind and contrast checks.
- [ ] Source, date and units shown; chart generated from data.
