---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.logql-metric-queries-and-range-aggregations
name: logql-metric-queries-and-range-aggregations
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [logql-metric-queries, loki, logql, rate, count_over_time, bytes_rate, topk, sum-by]
level: practitioner
status: docs-checked
description: "Turn logs into time series with LogQL range aggregations (rate, count_over_time, bytes_over_time) and vector aggregations."
sources: ["https://grafana.com/docs/loki/latest/query/metric_queries/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: error rates, throughput and top talkers from logs without pre-built metrics.

A metric query wraps a log selector (and optional pipeline) in a range aggregation, then optionally a vector aggregation.

```logql
# per-second log rate per service over 5 minutes
sum by (service_name) (rate({env="prod"} [5m]))

# error lines per app
sum by (app) (count_over_time({env="prod"} |= "level=error" [1m]))

# bytes per second per namespace, top 5
topk(5, sum by (namespace) (bytes_rate({cluster="main"} [5m])))

# error ratio
sum(rate({app="api"} |= "error" [5m])) / sum(rate({app="api"} [5m]))
```
Log range aggregations: `rate` (entries per second), `count_over_time`, `bytes_rate`, `bytes_over_time`, `absent_over_time`. The duration may follow the selector or sit at the end of the pipeline. Vector aggregations: `sum`, `avg`, `min`, `max`, `stddev`, `stdvar`, `count`, `topk`, `bottomk`, `sort`, `sort_desc`, with `by` or `without`; `topk` and `bottomk` need a parameter.

Other points from the docs
- `offset` must immediately follow the range: `count_over_time({job="mysql"}[5m] offset 5m)` is valid, `count_over_time({job="mysql"}[5m]) offset 5m` is invalid.
- `vector(0)` supplies a value when a query would return nothing: `sum(count_over_time({namespace="traefik"}[5m])) or vector(0)`.
- Result order is not guaranteed unless `sort` or `sort_desc` is used, and those only affect instant queries.
- `approx_topk` is an experimental instant-query-only alternative to `topk` that needs `limits_config.shard_aggregations: approx_topk`.

Gotchas
- `sum by` over a high-cardinality label returns many series; `max_query_series` (default 500) limits this.
- Unwrapped functions (`sum_over_time` and similar) are covered in the unwrap skill.

## Verify
```
logcli instant-query 'sum by (app) (rate({env="prod"}[5m]))'
```
The result is one vector sample per app.

## Checked
2026-11-03. Confirmed against the Loki "Metric queries" page and configuration reference (`max_query_series`). Removed: the claim that `{app=~".+"}` is rejected, `$__auto` and `$__interval` Grafana variables, the recording-rule advice, and "metric queries over long ranges are expensive" (none on the page).
Method: documentation only; no commands were run.
