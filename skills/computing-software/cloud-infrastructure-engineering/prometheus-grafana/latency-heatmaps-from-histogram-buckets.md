---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.latency-heatmaps-from-histogram-buckets
name: latency-heatmaps-from-histogram-buckets
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, heatmap-from-buckets, histogram-heatmap, heatmap-panel, promql, native-histograms, latency]
level: practitioner
status: docs-checked
description: "Build a Grafana latency heatmap from Prometheus histogram buckets: query format Heatmap, increase vs rate, le ordering, and pre-bucketed panel settings."
sources: ["https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/heatmap/", "https://grafana.com/blog/2020/06/23/how-to-visualize-prometheus-histograms-in-grafana/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Latency heatmaps from histogram buckets

## Query
```promql
sum by (le) (increase(http_request_duration_seconds_bucket{job="api"}[$__rate_interval]))
```
In the Prometheus query options set the format to **Heatmap**, legend `{{le}}`.
- Prometheus histogram buckets are cumulative: each `le` bucket counts every sample at or below its bound. With the **Time series** format you see cumulative counts, and buckets sort alphabetically (10 before 2).
- The **Heatmap** format tells Grafana the data is a histogram, so it sorts buckets numerically and shows distinct counts per bucket.
- `increase` gives counts per interval; `rate` gives the per-second average. The relative difference between buckets, hence the picture, is the same.
- Keep Max data points low (the blog used 25): heatmaps are dense and slow the browser at high resolution.

## Panel settings (Heatmap panel)
- **Calculate from data**: set to No when the data is already bucketed (it states whether the data is already a calculated heatmap or should be calculated in the panel).
- **Y Bucket scale** with Calculate from data = No: Auto, Linear, Log (base 2 or 10) or Symlog. Use log for exponential bucket layouts.
- Colors: mode Scheme (color by count) or Opacity (opacity by count); the Opacity Exponential scale uses value ^ k, with k below 1 logarithmic and above 1 exponential. Steps range 1 to 128.
- **Hide cells with values <=** and **>=** hide cells outside a range (for example, zero counts).
- Tooltip mode Single, All or Hidden; the legend shows the color scale.

## Reading it
- A second band above the main one is a new slow path; the whole band shifting up is a global slowdown; the top bucket lighting up means requests land at the largest bounds (check `+Inf`).

## Gotchas
- `sum by (le)` is needed: keeping other labels such as `pod` leaves per-series bucket data.
- Quantile estimates from buckets are approximations. If the value exceeds the largest finite bucket, Prometheus returns the largest bucket's `le`. For an SLO prefer "proportion of requests over X seconds" computed from bucket counts.
- Native histograms are not covered by the sources read; check the Prometheus data source docs for your Grafana version.

## Checked
2026-11-08. Confirmed in the Grafana Heatmap panel page (Calculate from data, Y Bucket scale options, color modes, Steps, Hide cells options, tooltip and legend) and the Grafana blog on Prometheus histograms (cumulative buckets, Time series vs Heatmap format, increase/rate equivalence, Max data points, quantile approximation caveat). Removed: Oranges/Spectral scheme names, native histogram query and Grafana version claim, Max data points ~200, p99 overlay claim, the Verify checklist.
Method: documentation only; no commands were run.
