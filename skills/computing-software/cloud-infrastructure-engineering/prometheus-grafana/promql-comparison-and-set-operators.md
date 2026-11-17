---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-comparison-and-set-operators
name: promql-comparison-and-set-operators
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, comparison-filtering, bool-comparison, logical-set-operators, unless-operator, or-fallback, operator-precedence, promql-precedence]
level: practitioner
status: verified
description: "Filter with comparison operators (with and without bool), combine conditions with and/or/unless, and avoid PromQL precedence traps with explicit parentheses."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/operators/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comparison, set operators and precedence

## Comparison: filter vs bool
```promql
node_load1 > 4                    # FILTER: keeps series whose value > 4, value unchanged
node_load1 > bool 4               # BOOL: every series, value 1 or 0 (use for counting/ratios)
sum(up == bool 0)                 # number of down targets (0 when none; `sum(up == 0)` returns nothing, checked on 3.15.0)
avg_over_time((probe_success == bool 1)[1d:1m])   # availability fraction from a gauge
```
Alert expressions use the filter form: the alert fires for every series that survives.

## Set operators (match on all labels unless on()/ignoring())
```promql
# and: keep left series that also exist on the right (intersection by labels)
rate(http_requests_total{code=~"5.."}[5m]) > 1 and on (job) (sum by (job) (rate(http_requests_total[5m])) > 100)
# or: union; left wins on label collision -> fallback values
sum by (job) (rate(errors_total[5m])) or sum by (job) (rate(requests_total[5m])) * 0
# unless: left series that have NO match on the right (suppress)
up == 0 unless on (instance) maintenance_mode == 1
kube_deployment_spec_replicas unless on (deployment) kube_deployment_status_replicas_available
```
`and`/`or`/`unless` are many-to-many and never need `group_left`.

## Precedence (highest to lowest)
1. `^` (right-associative)
2. `*` `/` `%` `atan2`
3. `+` `-`
4. `==` `!=` `<=` `<` `>=` `>`
5. `and` `unless`
6. `or`
Traps:
```promql
a > 0 and b > 0 or c > 0       # = ((a>0) and (b>0)) or (c>0)
-2 ^ 2                          # = -(2^2) = -4
x / y > 0.05 * 100              # comparison against 5, not "ratio as percent > 5"
```
Parenthesise every mixed expression. `/api/v1/format_query` and `promtool promql format` only pretty-print: they keep the parentheses you wrote and do not add any, so they do not reveal how an unparenthesised expression groups. Check grouping by evaluating both forms on test data (Prometheus 3.15.0 gave `cc` for `a > 0 and b > 0 or cc > 0` with a=5, b=0, cc=7, and `a` for the other grouping).

## Verify
- [ ] Every alert with multiple conditions is parenthesised.
- [ ] Counting queries use `bool` so they return 0 instead of no data.
