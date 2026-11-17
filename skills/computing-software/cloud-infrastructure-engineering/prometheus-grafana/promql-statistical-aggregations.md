---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-statistical-aggregations
name: promql-statistical-aggregations
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, quantile-operator, aggregated-quantile, stddev-stdvar, variance-aggregation, count-values-usage, value-distribution, anomaly-detection, outliers]
level: advanced
status: verified
description: "Use quantile(), stddev()/stdvar() and count_values() across series: outlier detection, z-score bands, version distribution, and how they differ from histogram_quantile."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/operators/#aggregation-operators", "https://about.gitlab.com/blog/2019/07/23/anomaly-detection-using-prometheus/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Statistical aggregations across series

## quantile(phi, v): across series, not across requests
```promql
# Median CPU across pods of a deployment, and the worst 10% boundary
quantile by (deployment) (0.5, rate(container_cpu_usage_seconds_total[5m]))
quantile by (deployment) (0.9, rate(container_cpu_usage_seconds_total[5m]))
```
It answers "what does the 90th-percentile **pod** look like", not request latency (that's
`histogram_quantile`). Useful for outlier detection: pods > 2x the median.

## stddev / stdvar
```promql
# Pods whose error rate is > 3 standard deviations above their peers (z-score)
(
  sum by (pod) (rate(http_requests_total{code=~"5.."}[5m]))
  - on() group_left avg(sum by (pod) (rate(http_requests_total{code=~"5.."}[5m])))
)
/ on() group_left stddev(sum by (pod) (rate(http_requests_total{code=~"5.."}[5m]))) > 3
```
Over time (seasonal bands for one series) use `stddev_over_time` with an offset baseline:
```promql
abs(job:requests:rate5m - avg_over_time(job:requests:rate5m[1d] offset 1w))
  > 3 * stddev_over_time(job:requests:rate5m[1d] offset 1w)
```
Precompute the baselines with recording rules; raw subqueries over days are expensive.

## count_values
```promql
count_values("version", build_info_version_number)          # how many instances per value
count by (version) (app_build_info)                          # usually better: version is already a label
count_values("replicas", kube_deployment_spec_replicas)      # distribution of replica counts
```
It turns sample **values** into a label; avoid on high-variety values (creates one series per distinct value).

## Gotchas
- `stddev` is the population standard deviation, so no series can exceed `sqrt(n - 1)` standard deviations from the mean: with 10 pods the largest possible z-score is 3.0 (3.15.0 returned 2.9999999999999996 for one pod at 1000x its peers) and the `> 3` alert above can only fire with 11 or more series (12 pods gave 3.3166 = sqrt(11)). Guard with `count(...) >= 11` or lower the threshold for small groups.
- These operators drop all labels not in `by`; join back with `on() group_left` as above.

## Checked
Run on 3.15.0: `quantile by (deployment) (0.5, ...)` and `(0.9, ...)` over four pods returned the median (0.0417) and 0.0617; `count_values("version", ...)` returned one series per distinct value with its count; the `*_over_time ... offset` band expression parses and returned nothing on flat data.

## Verify
- [ ] Outlier alert backtested: fires on known bad-pod incidents, quiet otherwise.
- [ ] Baseline recording rules exist for any `*_over_time ... offset 1w` used in alerts.
