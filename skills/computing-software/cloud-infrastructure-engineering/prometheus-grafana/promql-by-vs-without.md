---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-by-vs-without
name: promql-by-vs-without
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [by-vs-without, without-clause, aggregation, sum-by, promql, recording-rules]
level: practitioner
status: verified
description: "Choose between by and without in PromQL aggregations: label preservation, robustness to new labels in rules, and interaction with joins and alerts."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/operators/#aggregation-operators", "https://prometheus.io/docs/practices/rules/", "https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# by vs without

- `sum by (a, b) (x)`: keep only `a` and `b`.
- `sum without (instance, pod) (x)`: drop those, keep everything else (including `job` and any target labels).

## When to use which
| Situation | Prefer | Why |
|---|---|---|
| Dashboards, ad hoc | `by` | explicit output labels, predictable legends |
| Recording rules (`level:metric:ops`) | `without` | prometheus.io rules practice: keeps labels like `job`, `cluster`, `env` that you did not think of, so later joins still work |
| Alerts routed by team/severity labels | `without` or `by` including routing labels | `sum by (service)` drops `team`, breaking Alertmanager routing |
| Fixed-shape outputs for joins | `by` | stable label sets |

## Examples
```promql
# keep all target labels except per-instance ones
sum without (instance, pod, container) (rate(http_requests_total[5m]))
# explicit for a panel
sum by (route) (rate(http_requests_total{job="api"}[5m]))
```
`by`/`without` may be placed before or after the expression: `sum(x) by (a)` is the same as `sum by (a) (x)`.

## Gotchas
- `without` keeps unexpected high-cardinality labels if a target adds one (e.g. `version`): output grows silently.
- `by ()` and plain `sum(x)` are the same (one series, no labels).
- `topk`/`bottomk`/`limitk` with `by` select per group but keep all original labels of selected series.
- Recording rules named with `job:` must actually keep `job`; with `by`, list it explicitly.

## Checked
Run on Prometheus 3.15.0: `sum(x) by (a)` and `sum by (a) (x)` return the same series, `sum by () (x)` equals `sum(x)`, and `topk by (version) (1, x)` returns one full-label series per group. The recording-rule advice is the docs rule "Always specify a `without` clause with the labels you are aggregating away" (prometheus.io/docs/practices/rules).

## Verify
- [ ] Alert expressions retain every label used in Alertmanager routing (test with `amtool config routes test`).
