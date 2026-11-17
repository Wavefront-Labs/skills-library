---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-topk-bottomk-limitk
name: promql-topk-bottomk-limitk
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, topk, bottomk, topk-pitfalls, topk-time-series, limitk, limit-ratio, grafana-top-n]
level: practitioner
status: verified
description: "Get stable top-N graphs from topk/bottomk (per-step selection pitfalls, @ end() fix) and sample series with limitk and limit_ratio."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/operators/#aggregation-operators", "https://prometheus.io/docs/prometheus/latest/querying/basics/#modifier"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# topk, bottomk, limitk, limit_ratio

## The topk-over-time pitfall
In a range query, `topk(5, rate(x[5m]))` is evaluated **at every step independently**: the top 5 changes over
time, so the graph shows 15-30 different series with gaps. Fixes:
```promql
# Top 5 by the value at the END of the dashboard range, then graph those series over the whole range
rate(http_requests_total[5m])
  and on (pod)
topk(5, sum by (pod) (rate(http_requests_total[5m] @ end())))

# Top 5 by average over the range ($__range in Grafana): put @ end() on the subquery, not after the function call
rate(http_requests_total[5m])
  and on (pod)
topk(5, avg_over_time(sum by (pod) (rate(http_requests_total[5m]))[$__range:1m] @ end()))
```
In Grafana tables/bar gauges use an **instant** query, where topk does what you expect.

## Semantics
- `topk(k, v)` keeps the original labels of selected series (unlike most aggregations).
- `topk by (namespace) (3, ...)` = top 3 per namespace.
- Instant queries return the selected series ordered by value; "no sorting applies to range queries" (docs). The docs do not specify tie order.
- NaN is treated as farthest from the top or bottom, so it is only returned when `k` exceeds the number of non-NaN series (3.15.0: `topk(8, ...)` and `bottomk(8, ...)` over 8 numbers plus one NaN returned the 8 numbers).

## limitk and limit_ratio (added in Prometheus 2.54.0; still experimental and gated in 3.15.0)
```promql
limitk(10, http_requests_total)            # any 10 series (deterministic per label set), for previews
limit_ratio(0.1, http_requests_total)      # ~10% sample of series by label hash, consistent over time
limit_ratio(-0.9, http_requests_total)     # the complement (the other 90%)
```
Use to preview huge metrics in Explore without loading all series, or to split work. Without `--enable-feature=promql-experimental-functions` they fail with `limitk() is experimental and must be enabled`. On 3.15.0 `limit_ratio(0.5, ...)` kept 5 of 9 series and `limit_ratio(-0.5, ...)` the other 4; `limitk(2, ...)` returned the same two series at different times.

## Checked
On 3.15.0 with 8 series whose ranking flips every 10 minutes, `topk(2, rq)` over a range produced 4 distinct series of 30 points each, while `rq and on (pod) topk(2, rq @ end())` produced exactly 2 series of 60 points. `topk(5, avg_over_time(...[10m:]) @ end())` is a parse error (`@ modifier must be preceded by an instant vector selector or range vector selector or a subquery`), hence the subquery placement above.

## Verify
- [ ] Top-N dashboard panels show exactly N stable series across the range.
- [ ] Table panels using topk are set to Instant.
