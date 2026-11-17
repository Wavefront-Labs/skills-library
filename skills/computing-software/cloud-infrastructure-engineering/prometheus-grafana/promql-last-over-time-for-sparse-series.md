---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-last-over-time-for-sparse-series
name: promql-last-over-time-for-sparse-series
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [last-over-time, sparse-series, staleness-markers, lookback-window, promql, pushgateway]
level: practitioner
status: verified
description: "Use last_over_time to read the latest value of sparse or infrequently scraped series beyond the 5m lookback, and to bridge gaps in joins and dashboards."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/#aggregation_over_time", "https://prometheus.io/docs/prometheus/latest/querying/basics/#staleness", "https://prometheus.io/docs/prometheus/latest/command-line/prometheus/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# last_over_time for sparse series

`last_over_time(v range-vector)` returns the most recent sample in the range for each series. It ignores the lookback delta, so it finds values older than 5m (within the range).

## When you need it
- Series written sparsely: remote-written edge data every 10m, metrics from slow scrape intervals (5m+), recording rules with long intervals, data pushed from batch jobs via remote write.
- Info-style metrics that may briefly disappear, used in joins:
```promql
rate(http_requests_total[5m]) * on (instance) group_left (version) last_over_time(app_build_info[15m])
```
- Showing the last known value of a gauge on a stat panel even after the target went away (debugging).

Measured on 3.15.0: with samples every 10 minutes the plain selector returned the value 4 minutes after a sample and nothing 5 minutes after, while `last_over_time(x[1h])` kept returning it. In the join above, a plain `* on (instance) group_left (version) app_build_info` was empty once the info series had been absent for 10 minutes, and the `last_over_time` form still returned the version.

## Examples
```promql
last_over_time(battery_level_percent[1h])
time() - last_over_time(job_last_success_timestamp_seconds[1d])      # age of the last success (the metric's value is the timestamp)
ts_of_last_over_time(sparse_metric[1h])                               # sample time of the last sample (experimental function flag)
```
`timestamp(last_over_time(x[1h]))` does not give the sample time: on Prometheus 3.15.0 it returned the evaluation time, so `time() - timestamp(last_over_time(...))` is always 0.

## Lookback alternative
`--query.lookback-delta=15m` changes it globally (default `5m`; affects every query). The query API also accepts a per-query `lookback_delta` parameter (docs; it returned a series after a 10 minute gap on 3.15.0). Prefer `last_over_time` or the per-query parameter over the global flag.

## Gotchas
- Staleness markers end a series in instant queries, but `last_over_time` still returns the last real sample before the marker within the range, which can show values for targets that are gone (promtool test: after a staleness marker `x` returned nothing, `last_over_time(x[10m])` still returned 3 and `count_over_time` counted 3 real samples). That may be what you want for debugging, not for "current state" panels.
- Large ranges over many series are expensive; keep ranges tight.

## Verify
- [ ] Sparse-series panels show continuous lines at the expected cadence with no 5m gaps.
