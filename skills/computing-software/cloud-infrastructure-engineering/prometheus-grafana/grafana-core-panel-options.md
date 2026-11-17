---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-core-panel-options
name: grafana-core-panel-options
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, time-series-options, stacking, fill-below-to, axis-config, table-cell-display, cell-coloring, column-filter, stat-options, gauge-thresholds-display, sparkline, value-mapping-rules, field-override-rules]
level: practitioner
status: gated
description: "Configure the workhorse Grafana panels: time series (stacking, fill below to, axes, threshold style), table cell types and filters, stat/gauge modes, value mappings and overrides."
sources: ["https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/time-series/", "https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/table/", "https://grafana.com/docs/grafana/latest/panels-visualizations/configure-overrides/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Core panel options

## Time series
- **Stacking**: Normal for parts of a whole (CPU modes, per-pod requests); Off for comparing independent series.
  "100 %" shows shares.
- **Fill below to** (override on a series): shade between series, e.g. p50 fills to p99 to draw a latency band.
- **Axes**: placement Right for a second unit (field option `axisPlacement`; the UI label is "Placement"), soft min 0 (`axisSoftMin`), log scale for
  wide ranges (the UI offers "Logarithmic" as a scale type); "Centered zero" (`axisCenteredZero`) for diverging values.
- **Thresholds style** (`thresholdsStyle`): As lines / As filled regions to draw SLO lines (e.g. 0.3 s) without extra queries (the options exist; the drawing was not rendered here) (gated: unconfirmed, source is paywalled or blocked).
- Negative-Y transform (override "Negative Y"; value `negative-Y`) for RX/TX on one graph.
- Legend: Table mode with Mean/Max/Last calcs, sort by Max to find the worst series.

## Table
- Cell type per column (`cellOptions`): Colored text / Colored background (by thresholds), Gauge (display modes basic, gradient and `lcd`, which the UI labels "Retro LCD"), Sparkline,
  JSON View, Image, Data links, Actions (all these labels and ids exist in the 13.2.4 frontend).
- **Column filter** (Field -> Column filter) adds per-column filter dropdowns; footer with Sum/Mean.
- Column widths, min width, text wrap; hide `Time` with Organize fields.

## Stat / gauge / bar gauge
- Stat: Value / Value and name / Name; Color mode Value / Background solid / gradient; **Graph mode Area** adds
  a sparkline (`graphMode`, `colorMode`, `textMode` are the option ids); Text size; Calculation (Last *, Mean, Max) - "Last *" is `lastNotNull`: "Last non-null value (also excludes NaN)" in Grafana's own description.
- Gauge: thresholds drawn as arcs (the option ids are `showThresholdMarkers` and `showThresholdLabels`; their UI labels were not confirmed); set min/max explicitly (0-1 for ratios).
- Bar gauge: orientation, display mode, "Show unfilled area"; good for top-N lists.

## Value mappings and overrides
- Value mappings: Value (`1 -> UP` green, `0 -> DOWN` red), Range (0-0.9 -> "degraded"), Regex, Special
  (null/NaN -> "no data"); the four mapping types exist in the 13.2.4 frontend, the colour examples were not rendered.
- Overrides: match **Fields with name**, **Fields with name matching regex**, **Fields returned by query**, **Fields with type**;
  then set unit, colour, axis, display name, hide in legend/tooltip. Order matters: later overrides win (not run here) (gated: unconfirmed, source is paywalled or blocked).
- Standard options (unit, min/max, decimals, display name `${__field.labels.pod}`) apply to all fields first.

## Verify
- [ ] Units set on every panel (no raw seconds/bytes).
- [ ] Threshold colours consistent with alert thresholds.

## Checked
Method: Grafana 13.2.4 shipped frontend (`public/build/*.js`) and `public/locales/en-US/grafana.json` searched for each option id and UI label named in the skill (option ids `axisPlacement`, `axisSoftMin`, `axisCenteredZero`, `fillBelowTo`, `thresholdsStyle`, `spanNulls`, `graphMode`, `colorMode`, `textMode`, `cellOptions`, `showUnfilled`, `lastNotNull` all present; labels such as "Fill below to", "Connect null values", "Column filter", "Time shift" present). Where a label differs it is corrected above.
- Visual behaviour (what each option draws) was not rendered, and the override ordering rule was not run: gated markers, so the skill is `gated`.
