---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-heatmap-panel
name: grafana-heatmap-panel
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [heatmap-panel-config, histogram-heatmap, grafana-visualizations, heatmap-from-buckets, native-histograms]
level: practitioner
status: docs-checked
description: "Configure the Grafana heatmap panel for Prometheus histogram buckets (Heatmap format, Calculate from data off) or calculated heatmaps from raw values; options that matter."
sources: ["https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/heatmap/", "https://grafana.com/docs/grafana/latest/datasources/prometheus/query-editor/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heatmap panel

A heatmap shows histograms over time. It supports time series data.

## Prometheus classic histogram buckets
Illustrative query:
```promql
sum by (le) (increase(http_request_duration_seconds_bucket{job="api"}[$__rate_interval]))
```
- Query editor **Format = Heatmap**: "displays histogram-type metrics in a Heatmap panel by converting cumulative histograms to
  regular ones and sorting the series by bucket boundary." Legend can be a custom template such as `{{le}}`.
- Query editor Min interval sets the minimum interval between returned data points and supports `$__interval` and `$__rate_interval`.
- Heatmap panel **Calculate from data**: "determines if the data is already a calculated heatmap (from the data source or
  transformer), or one that should be calculated in the panel." For pre-bucketed data leave it **No**.
- With Calculate from data = No, the Y Bucket scale offers Auto, Linear, Log (base 2 or 10) and Symlog; **Tick alignment** (Auto,
  Top (LE), Middle, Bottom (GE)) appears only when Calculate from data is No and Y Bucket scale is Auto.

## Raw values (calculated)
With Calculate from data = Yes, set **X Bucket** (a time interval Size, or Count) and **Y Bucket** (Size or Count) and the Y Bucket
scale (Linear, Logarithmic base 2 or 10, Symlog with a linear threshold).

## Options that matter
- Colours: mode Scheme (pick a scheme; **Steps** 1 to 128) or Opacity (scale Exponential with an Exponent above 0, or Linear).
  Optional start and end values for the colour scale override the series min and max.
- Cell display: **Cell gap**, **Hide cells with values <=** and **>=**.
- Tooltip: with Tooltip mode **Single**, **Show histogram (Y axis)** adds a histogram of the y-axis to the tooltip.
- Exemplars: toggle in the Prometheus query editor; they are not available with Instant query types.

## Verify
- [ ] A bucketed query uses Format = Heatmap and Calculate from data = No.
- [ ] A raw-value heatmap has Calculate from data = Yes with X and Y buckets set.

## Checked
Checked 2026-11-07. Read the Heatmap page through its panel options, y-axis, colour, cell display, tooltip, legend and annotation
sections (lines 12-136 of the stripped page; I did not read any examples below that), and the Prometheus query editor page's
Format, Type, Legend, Min interval and Exemplars parts (not the whole page). Removed as not on those pages: the native histogram
rendering claim and the native histogram query, the "Hide cells <= 0" example, the "gradient that means nothing" gotcha, the
noisy-buckets remark, the p50 check against a RED dashboard, and the guidance on increase versus rate. The histograms practices page
was dropped from sources because no claim here depends on it. The query above is an illustration, not a page-verified recipe.
Method: documentation only; no commands were run.
