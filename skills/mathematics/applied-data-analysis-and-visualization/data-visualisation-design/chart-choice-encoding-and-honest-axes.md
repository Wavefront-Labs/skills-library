---
id: mathematics.applied-data-analysis-and-visualization.data-visualisation-design.chart-choice-encoding-and-honest-axes
name: chart-choice-encoding-and-honest-axes
category: mathematics
field: applied-data-analysis-and-visualization
product: data-visualisation-design
tags: [data-visualisation-design, data-visualization, dataviz, chart-selection, chart-type, visual-encoding, cleveland-mcgill, bar-chart, line-chart, scatterplot, dot-plot, small-multiples, pie-chart, dual-axis, log-scale, zero-baseline, truncated-axis, aspect-ratio, colour, color, colorblind, viridis, colorbrewer, sequential-palette, diverging-palette, annotation, direct-labelling, chart-junk, ggplot2, matplotlib, data-analysis]
level: practitioner
status: draft
description: "Pick the chart that answers the question, encode the key comparison by position, set axes and scales that don't distort, and use colour and labels that survive greyscale and colour-blindness."
sources: ["Cleveland & McGill (1984), Graphical Perception, JASA", "Munzner, Visualization Analysis and Design (CRC)", "Wilke, Fundamentals of Data Visualization (O'Reilly, free online)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Chart choice, encoding and honest axes

**Goal:** a chart where the intended comparison is the easiest thing to see and nothing
about the scales exaggerates or hides it.

## 1. Start from the question, not the chart type
Write the one sentence the chart must support ("Region B overtook A in 2023"). Then pick:
| Comparison | Default chart |
|---|---|
| Values across categories | Horizontal bar (sorted) or dot plot |
| Change over time | Line chart |
| Relationship between two numbers | Scatterplot (+ trend line if justified) |
| Distribution | Histogram, density, box/violin; strip plot for small n |
| Part-to-whole | Stacked bar or 100% bar; pie only for 2–3 parts |
| Many groups × same chart | Small multiples with shared axes |
| Geography | Choropleth of **rates**, not counts (or it's a population map) |

## 2. Encode the main comparison by position
Cleveland-McGill ranking of perceptual accuracy: position on a common scale > position on
non-aligned scales > length > angle/slope > area > colour saturation/hue.
So: comparisons you care about go on a shared axis. Pie and bubble charts make readers
compare angles and areas — they are imprecise by design. Stacked bars make only the
bottom segment easy to compare; put the most important series there or use small multiples.

## 3. Axes and scales
- **Bars must start at zero** — bar length *is* the value. Truncating the axis turns a
  2% difference into a visual doubling.
- Lines and dots **may** use a non-zero baseline when the variation is the point; label
  the axis clearly.
- **Log scale** for data spanning orders of magnitude or for growth rates (equal slopes =
  equal % growth). Say "log scale" on the axis.
- **Dual y-axes:** avoid. Any apparent crossing or correlation depends on arbitrary
  scaling. Use two panels or index both series to 100 at a common start.
- Aspect ratio changes perceived slope; banking to ~45° for key segments is a useful default.
- Same scale across small multiples unless you say otherwise (`facet_wrap(scales = "fixed")`
  is the ggplot2 default — keep it).

## 4. Colour
- Categorical: ≤ 6–8 distinguishable hues; beyond that, group or label directly.
- Ordered values: **sequential** palette (light → dark). Data with a meaningful midpoint
  (change, anomaly): **diverging** palette centred on it.
- Use perceptually uniform, colour-blind-safe palettes (viridis family, ColorBrewer
  safe sets). Avoid red/green as the only distinction (~8% of men have red-green deficiency).
- Use colour to highlight one series and grey for the rest when telling one story.
- Check it in greyscale.

## 5. Text and annotation
- Title states the finding; subtitle gives units, population, period, source.
- Direct-label lines instead of a legend where possible.
- Annotate events that explain features (policy change, method change, missing period).
- Remove gridline clutter, 3D effects, shadows — anything that carries no data.
- Show uncertainty (CIs, ranges) when the reader might over-read small differences.

## 6. Tool notes
ggplot2: `geom_col()` (zero baseline built in), `scale_y_log10()`, `scale_colour_viridis_d()`.
matplotlib/seaborn: `ax.set_yscale("log")`, `cmap="viridis"`, `sns.relplot(col=...)` for small
multiples. Spreadsheet tools sometimes auto-truncate bar axes — set the minimum to 0 manually.

## Uncertainty notes
Perceptual rankings come from controlled experiments and are guidelines; the colour-blindness
prevalence figure is the commonly cited approximation for people of Northern European descent.

## Verify
- [ ] You can state the chart's one-sentence message and the chart makes it obvious.
- [ ] Key comparison is on a common position scale.
- [ ] Bar charts start at zero; log scales and non-zero baselines are labelled.
- [ ] No dual y-axis (or a strong, stated reason).
- [ ] Palette is colour-blind-safe and type-appropriate (categorical / sequential / diverging).
- [ ] Title, units, source and period present; maps show rates.
