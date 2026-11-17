---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-visualization-types
name: grafana-visualization-types
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, visualizations, panel-types, time-series-panel, stat-panel, gauge, bar-gauge, table-panel, state-timeline, status-history, heatmap, histogram-panel, bar-chart, pie-chart, logs-panel, traces-panel, node-graph, geomap, canvas, text-panel, field-overrides, value-mappings, units, thresholds, color-schemes, legend-calcs]
level: practitioner
status: gated
description: "Pick the right Grafana visualization and configure it well: time series vs stat vs state timeline vs heatmap vs table, units, thresholds, mappings, overrides, legend calcs, and common misuses."
sources: ["https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/", "https://grafana.com/docs/grafana/latest/panels-visualizations/configure-standard-options/", "https://grafana.com/docs/grafana/latest/panels-visualizations/configure-overrides/", "https://grafana.com/docs/grafana/latest/panels-visualizations/configure-thresholds/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana visualization types

**Goal:** every panel answers one question at a glance, with the visualization that fits
the data shape, and consistent units/thresholds so red means the same thing everywhere.

## 1. Choose by question and shape
| Question | Visualization | Data shape | Notes |
|---|---|---|---|
| How does X change over time? | **Time series** | 1–10 series | stack only for parts-of-whole; `bars` for per-interval counts (`increase`) |
| What is X right now? (and trend) | **Stat** | 1–few values | Calculation *Last\** ; sparkline on; colour by thresholds; text mode value/name |
| How close to a limit? | **Gauge** / **Bar gauge** | value with known max | set `max` from a quota (Config from query); bar gauge for many items side by side |
| Which state over time? (up/down, phases) | **State timeline** | discrete values per series | value mappings → colours; for `up`, `kube_pod_status_phase`, feature flags |
| How often was X in state S? | **Status history** | discrete, many entities | compact grid of boxes |
| Distribution over time? | **Heatmap** | Prometheus histogram buckets (`sum by (le) (rate(_bucket[5m]))`, format Heatmap) | *Calculate from data: off* for pre-bucketed; `le` buckets with log scale |
| Distribution now? | **Histogram** panel | raw values or buckets | |
| Compare categories? | **Bar chart** | one row per category (instant/table) | horizontal for long names |
| Share of total? | **Pie chart** | ≤ 6 categories | otherwise a bar chart; never for time-varying ratios |
| Many entities, many metrics? | **Table** | instant queries merged | cell display modes: colour background / gauge / sparkline |
| Which logs? traces? | **Logs**, **Traces**, **Node Graph**, **Flame Graph** (names as listed by `GET /api/plugins?type=panel` on 13.2.4; also present: Trend, XY Chart, Candlestick, Canvas, Annotations list, Logs Table) | Loki/Tempo/Pyroscope | |
| Where? | **Geomap** | lat/lon or geohash fields | |
| Explanatory text / links | **Text** (markdown), **Dashboard list**, **Alert list** | | |

## 2. Standard options that must be set
- **Unit**: always (`short`, `percentunit` for 0–1 ratios, `percent` for 0–100, `s`/`ms`,
  `bytes(IEC)`, `reqps`, `cps`). The unit ids `percentunit`, `percent`, `short`, `s`, `ms`, `bytes`, `decbytes`, `reqps` and `cps` exist in the 13.2.4 frontend (`bytes(IEC)` is the label of id `bytes`). Wrong unit is the number-one dashboard bug (`percent` on a 0–1 ratio).
- **Min/Max**: fix `0–1`/`0–100` on ratios so panels do not autoscale noise into drama.
- **Decimals**: set explicitly on stat/gauge.
- **Thresholds**: base + steps in absolute or percentage mode; the colour is used by stat,
  gauge, table cells, and time-series *Thresholds: show as lines/area*.
- **Value mappings**: value/range/regex/special → text + colour (`0 → DOWN red`, `1 → UP green`);
  essential for state timeline and stat.
- **Color scheme**: `Classic palette` for multi-series, `From thresholds` for status, a
  single colour for single series. Keep green/red for good/bad only.
- **Display name**: `${__series.name}`, `${__field.labels.pod}` to shorten legends.
- **Links**: data links with `${__value.raw}`, `${__field.labels.instance}`, `${__url_time_range}`.

## 3. Overrides
Use *Fields with name / name matching regex / type / query* to style one series differently:
right Y-axis for a ratio next to a count (`Axis placement: right`), dashed line for a
threshold series, custom colour for `errors`, hidden `Time` column in tables, per-column
units in merged tables (`Value #B` → bytes). Many overrides = wrong panel split; prefer
two panels.

## 4. Time series panel details
- Legend: table mode with calculations `Last*`, `Mean`, `Max` and *sort by* makes the
  legend a mini table; limit to ~15 series or the chart is unreadable.
- `Connect null values: < threshold` (e.g. 2× scrape interval) hides scrape gaps without
  inventing data; `Show points: never` for dense data.
- Stacking: *normal* only with same units and parts of a whole; *100%* for proportions.
- Transform `__interval`-dependent queries: use `$__rate_interval` in PromQL so bars/rates
  survive zooming.

## 5. Stat and gauge details
- Calculation defaults to *Last\** (last non-null). For "over the time range" choose
  *Mean*/*Max* deliberately, and title accordingly ("p99 latency (range max)").
- *Text mode: Value and name* when a stat shows many values (one per series); *Layout:
  horizontal/vertical* and *Orientation* control wrapping.
- Gauge needs a real `max`; without one it shows 0–100 and misleads.

## 6. Heatmap from Prometheus histograms
Query: `sum by (le) (rate(http_request_duration_seconds_bucket{job="api"}[$__rate_interval]))`,
Format **Heatmap**, panel *Calculate from data: No*, *Y axis: log 2*, colour scheme
`Spectral`/`Oranges` with *Scale: exponential* or `sqrt` for long tails (the option and scheme names exist in the 13.2.4 frontend; the heatmap was not rendered because the local exporter has no histogram) (gated: unconfirmed, source is paywalled or blocked). Add an overlay
time series panel of `histogram_quantile(0.99, ...)` to anchor the eye.

## Gotchas
- Pie/bar on time-series data silently reduces each series (default *Last*); say so in the title.
- Stat panel with a range query and *Last* hides outages mid-range; pair with a sparkline or a time series.
- Table *Cell type: gauge* needs min/max; otherwise every cell is full (not rendered here) (gated: unconfirmed, source is paywalled or blocked).
- `percentunit` vs `percent` mistakes make 0.95 show as 0.95% or 95% show as 9500%.
- Thresholds in *percentage* mode are relative to min/max, which autoscale unless fixed.

## Verify
- [ ] Every panel has a unit, and ratio panels have min 0 / max 1 (or 100).
- [ ] Status-style panels use value mappings, not raw 0/1.
- [ ] A stranger can read each panel title and know the calculation (last/mean/max) and window.
- [ ] No panel has more than ~15 visible series or more than ~5 overrides.

## Checked
Method: panel plugin names from `GET /api/plugins?type=panel` on Grafana 13.2.4; unit ids, heatmap option and colour scheme names searched in the shipped frontend bundle. The guidance on when to use each visualization is advice, and the rendering behaviour (heatmap, gauge cells) was not checked visually: gated markers, so the skill is `gated`.
