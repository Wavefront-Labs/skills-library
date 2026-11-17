---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-double-exponential-smoothing
name: promql-double-exponential-smoothing
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [double-exponential-smoothing, holt-winters, promql, forecasting, gauges, promql-experimental-functions]
level: advanced
status: verified
description: "Smooth and trend gauges with double_exponential_smoothing (formerly holt_winters): parameters, enabling the experimental flag, and when predict_linear is better."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/#double_exponential_smoothing", "https://prometheus.io/docs/prometheus/latest/migration/", "https://prometheus.io/docs/prometheus/latest/feature_flags/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# double_exponential_smoothing

`double_exponential_smoothing(v range-vector, sf scalar, tf scalar)` produces a smoothed value for each series using double exponential smoothing (Holt linear). `sf` (smoothing factor) and `tf` (trend factor) must be strictly between 0 and 1 (3.15.0: `sf = 1.5` returned `invalid smoothing factor. Expected: 0 < sf < 1`). Should only be used with gauges.

## Version notes
- Prometheus 2.x: `holt_winters(v, sf, tf)`.
- Prometheus 3.x: renamed `double_exponential_smoothing` and requires `--enable-feature=promql-experimental-functions` (migration guide). Without the flag it fails with `function "double_exponential_smoothing" is not enabled`, and `holt_winters` is an unknown function. Update rules when upgrading.

## Usage
```promql
# smoothed queue depth, low sf = smoother, higher tf = follows trend faster
double_exponential_smoothing(queue_depth[30m], 0.3, 0.5)
# on a counter, smooth the rate via subquery
double_exponential_smoothing(rate(http_requests_total[5m])[1h:1m], 0.2, 0.3)
```

## Choosing parameters
- `sf` near 0: heavy smoothing, slow to react; near 1: follows raw data.
- `tf` near 0: ignores trend; near 1: reacts strongly to recent slope.
- Start with sf=0.3, tf=0.3 and compare against the raw series on a known incident.

## When to use something else
- Forecasting time-to-full: `predict_linear(x[6h], 3600*24)` is simpler and explainable.
- Simple smoothing: `avg_over_time(x[10m])`.
- Seasonal baselines (daily patterns): use offset-based baselines (`avg_over_time(x[1h] offset 1w)`) or recording-rule bands; this function has no seasonality term despite the old name.

## Gotchas
- Result is the last smoothed point only (per evaluation), not a forecast.
- Needs at least two samples in the range (3.15.0: one sample returned nothing).
- Checked against a Python implementation of the Holt linear recursion (initial level = first sample, initial trend = second minus first): sf=0.3, tf=0.5 over a 31-sample window gave 3.5348551668000656 in both.

## Verify
- [ ] Experimental flag present on servers whose rules use it; `promtool check rules` passes against the target version.
