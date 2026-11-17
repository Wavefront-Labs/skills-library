---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-subqueries-and-smoothing
name: promql-subqueries-and-smoothing
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, subqueries, subquery-resolution, max-over-time-subquery, smoothing-over-time, avg-over-time-smoothing, quantile-over-time, recording-rules]
level: advanced
status: verified
description: "Use subqueries ([range:resolution]) for max_over_time(rate()) questions, pick the resolution, smooth series with *_over_time, and know when to record instead."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/basics/#subquery", "https://prometheus.io/docs/prometheus/latest/querying/functions/#aggregation_over_time", "https://prometheus.io/blog/2019/01/28/subquery-support/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subqueries and smoothing

## Subquery syntax
`<instant expression>[<range>:<resolution>]` evaluates the inner expression every `resolution` across
`range`, producing a range vector for an `*_over_time` function.
```promql
max_over_time(rate(http_requests_total[5m])[1d:5m])            # peak 5m request rate in the last day
quantile_over_time(0.95, sum(rate(http_requests_total[5m]))[7d:10m])   # p95 of traffic over a week
min_over_time((sum(up{job="api"}) / count(up{job="api"}))[1h:1m])      # worst availability minute in last hour
```
- Omitted resolution (`[1d:]`) uses the global `evaluation_interval` (docs; default `1m`, many configs set `15s`,
  which is 5,760 evaluations per day). Always set it explicitly.
- Resolution should be >= the inner rate's scrape interval and usually equal to the rate window's step
  you care about (5m rate -> 1m-5m resolution).
- Cost ~ (range / resolution) x inner query cost. A 30-day subquery on raw data in a dashboard is a classic
  Prometheus killer.

## Prefer recording rules
If the inner expression is reused or the range is long, record it:
```yaml
- record: job:http_requests:rate5m
  expr: sum by (job) (rate(http_requests_total[5m]))
```
then `max_over_time(job:http_requests:rate5m[1d])`: no subquery, raw samples of a cheap series.

## Smoothing
```promql
avg_over_time(node_load1[15m])                                    # moving average of a gauge
avg_over_time(job:http_requests:rate5m[1h])                       # smoothing a recorded rate
rate(x[30m])                                                       # for counters, a longer window IS smoothing
```
`*_over_time` family: `avg`, `min`, `max`, `sum`, `count`, `quantile`, `stddev`, `stdvar`, `last`,
`present`, `mad_over_time` (experimental). They work on raw samples of gauges; for counters use
rate first (via subquery or recording rule).

## Gotchas
- Staleness markers are not counted: a promtool test with samples `1 2 3 stale` gave `count_over_time(x[10m]) = 3`. `count_over_time` tells you how many real samples were present.
- Smoothing delays alert detection (a moving average lags by roughly half its window); use it for dashboards, not fast alerts.
- Checked on 3.15.0: `[10m:]` with a 1m evaluation interval produced 10 steps (`count_over_time(rate(reqs[5m])[10m:])` = 10); `mad_over_time` needs `--enable-feature=promql-experimental-functions` (`function "mad_over_time" is not enabled` otherwise).

## Verify
- [ ] Every subquery in dashboards/rules has an explicit resolution.
- [ ] Long-range subqueries replaced by recording rules (query log shows no multi-second subqueries).
