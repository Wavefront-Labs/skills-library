---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-ratios-and-missing-series
name: promql-ratios-and-missing-series
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, ratio-queries, percentage-queries, division-by-zero, absent-function, absent-over-time, default-values, or-vector-zero, error-ratio, missing-metric-alerts]
level: practitioner
status: verified
description: "Write error ratios and percentages that survive zero traffic, label mismatches and missing series: ignoring/on, NaN handling, absent(), absent_over_time and or vector(0)."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/operators/", "https://prometheus.io/docs/prometheus/latest/querying/functions/#absent"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ratios and missing series

## Error ratio done right
```promql
sum by (job) (rate(http_requests_total{code=~"5.."}[5m]))
/
sum by (job) (rate(http_requests_total[5m]))
```
- Aggregate both sides to the **same** label set before dividing; dividing raw series fails to match because
  `code` differs.
- If one side keeps extra labels use `/ ignoring(code)` or `/ on(job)` (+ `group_left` if many-to-one).
- Percent: multiply by 100 only where a consumer needs a percentage, otherwise keep the 0-1 ratio.

## Zero traffic and NaN
- `0/0 = NaN`, `x/0 = +Inf`. NaN compares false, so `ratio > 0.05` doesn't fire at zero traffic (usually
  wanted). Graphs show gaps.
- When there are **no** 5xx series at all, the numerator is empty and the ratio returns nothing (not 0):
```promql
(sum by (job) (rate(http_requests_total{code=~"5.."}[5m])) or sum by (job) (rate(http_requests_total[5m])) * 0)
/ sum by (job) (rate(http_requests_total[5m]))
```
The `or ... * 0` supplies a 0 numerator with the right labels. `or vector(0)` works only for
label-less results (`sum(...) or vector(0)`), since `vector(0)` has no labels.
- Measured on Prometheus 3.15.0: with no 5xx series the plain ratio returned only the job that had errors, the `or ... * 0` form also returned the error-free job with value 0; `zero / zero` returned NaN, `vector(1) / 0` returned `+Inf`, and `zero / zero > 0.05` returned nothing; `absent(up{job="nonexist"})` carried `job="nonexist"`, `absent(up{job=~"nonexist"})` carried no labels, and `absent(up{job="x"} == 1)` (all targets down) returned one series with no labels.
- Guard low-volume alerts: `... and sum by (job) (rate(http_requests_total[5m])) > 1`.

## Detecting absence
```promql
absent(up{job="payments"})                         # 1 when no such series exists right now
absent_over_time(heartbeat_timestamp{job="batch"}[2h])  # none in the last 2h
```
- `absent()` copies equality matchers into its result labels (`job="payments"`), so alerts get useful labels;
  regex matchers are not copied.
- `absent(up{job="x"} == 1)` is wrong for "all down": it fires only if no target is up and alerts
  once without per-instance labels. Use `up == 0` for per-target, `absent` for whole-job disappearance.
- One `absent` per critical job; `absent` over many jobs at once can't tell you which is missing.

## Verify
- [ ] Ratio panels show 0 (not "No data") for a service without errors.
- [ ] Stopping a scraped job fires its `absent` alert within the `for` window.
