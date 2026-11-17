---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-many-to-many-and-duplicate-series-errors
name: promql-many-to-many-and-duplicate-series-errors
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [many-to-many-error, duplicate-series-error, vector-matching, group-left, info-metrics-pattern, promql]
level: advanced
status: verified
description: "Fix 'many-to-many matching not allowed' and 'found duplicate series for the match group' errors caused by info metric churn, missing labels or wrong grouping."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/operators/#many-to-one-and-one-to-many-vector-matches", "https://prometheus.io/docs/prometheus/latest/querying/operators/#vector-matching", "https://prometheus.io/docs/practices/naming/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Many-to-many and duplicate series errors

## The errors
Messages from Prometheus 3.15.0 (the query API returns them as `execution` errors):
- Duplicates on the right-hand side, with or without `group_left`: one combined error, `found duplicate series for the match group {instance="a"} on the right hand-side of the operation: [...];many-to-many matching not allowed: matching labels must be unique on one side`.
- Duplicates on the left-hand side with plain `on()`/`ignoring()` matching: `multiple matches for labels: many-to-one matching must be explicit (group_left/group_right)`.

## Causes and fixes
| Cause | Fix |
|---|---|
| Info metric changed labels during a deploy (two `*_info` series for the same instance briefly) | dedupe the one side: `max by (instance, version) (app_build_info)` won't help if both versions exist; use `topk by (instance) (1, app_build_info)` or `last_over_time` window shorter than rollout |
| Join key not unique (matching on `pod` across namespaces) | add `namespace` to `on(...)` |
| Side not aggregated (several containers per pod) | `sum by (namespace, pod) (...)` before the join |
| HA replicas both present (Thanos without dedup) | enable dedup / match ignoring the replica label |

## Pattern for safe info joins
```promql
sum by (namespace, pod) (rate(container_cpu_usage_seconds_total{container!=""}[5m]))
* on (namespace, pod) group_left (node)
max by (namespace, pod, node) (kube_pod_info)
```
`max by` collapses duplicates that share all kept labels. It does nothing when the duplicates differ in a kept label such as `version`: that case still errored on 3.15.0, while `topk by (instance) (1, app_build_info)` worked. The pattern above ran correctly on test data with the same pod name in two namespaces.

## Debugging
Run the "one" side with `count by (<matching labels>) (...) > 1` to see which groups are duplicated and when.

## Gotchas
- Errors can appear only for some time ranges (during rollouts), making alerts fail intermittently: test rules over a deploy window.
- `group_left` without a label list copies nothing extra; the error still applies (checked on 3.15.0).

## Verify
- [ ] `count by (<join labels>) (<one side>) > 1` returns nothing over the last 7 days.
