---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-counting-series-and-targets
name: promql-counting-series-and-targets
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [count-series, count-by, aggregation, cardinality-analysis, up-metric, promql]
level: practitioner
status: verified
description: "Count series, targets, distinct label values and instances per group with count, count by and nested counts, and know when these queries are expensive."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/operators/#aggregation-operators", "https://prometheus.io/docs/prometheus/latest/querying/examples/", "https://prometheus.io/docs/prometheus/latest/querying/api/#tsdb-stats"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Counting series and targets

```promql
count(up)                                   # targets
count by (job) (up)                         # targets per job
count by (job) (up == 0)                    # down targets per job (no result if none)
sum by (job) (up == bool 0)                 # down targets as 0/1 sum, always returns a value per job
count(count by (version) (app_build_info))  # distinct versions deployed
count by (job) (count by (job, instance) ({__name__=~"node_.+"}))  # instances per job exposing node_* metrics
count({__name__="http_request_duration_seconds_bucket"})           # series of one metric
count by (__name__) ({job="api"})          # series per metric for one job
```

## Patterns
- Distinct values of a label: inner `count by (label)`, outer `count`.
- Ratio of healthy: `avg by (job) (up)` = fraction of targets up.
- Missing groups: `count by (x)` returns nothing for empty groups; combine with `or` and a reference series if you need 0s: `count by (job) (up == 0) or count by (job) (up) * 0`.

## Cost
- `count by (__name__) ({job="api"})` touches every series of that job; fine for one job, expensive for `{__name__=~".+"}` on big servers. Prefer `/api/v1/status/tsdb` or `promtool tsdb analyze` for whole-server cardinality.
- Counting raw histograms multiplies by buckets; count `_count` series instead.

## Gotchas
- `count` counts series, not samples; over a range use `count_over_time` per series.
- Filtering with `== 0` drops non-matching series; `== bool 0` keeps them as 0/1.

## Checked
Run on Prometheus 3.15.0 with three targets (one down): `count(up)` = 3; `count by (job) (up == 0)` returned only the job with a down target; `sum by (job) (up == bool 0)` returned 1 and 0; `count by (job) (up == 0) or count by (job) (up) * 0` returned both jobs; `count(count by (version) (app_build_info))` = 2; `count by (__name__) ({job="a"})` listed series per metric; `avg by (job) (up)` returned 0.5 and 1. `/api/v1/status/tsdb` is in the HTTP API docs and `promtool tsdb analyze` in the promtool docs.

## Verify
- [ ] Target counts per job match the expected inventory (CMDB/kubectl count).
