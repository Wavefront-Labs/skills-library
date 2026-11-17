---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-one-to-one-matching-on-ignoring
name: promql-one-to-one-matching-on-ignoring
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [on-ignoring, one-to-one-matching, vector-matching, binary-operators, promql]
level: practitioner
status: verified
description: "Make binary operations match the right series with on() and ignoring() in one-to-one vector matching, and debug empty results from label mismatches."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/operators/#vector-matching", "https://prometheus.io/docs/prometheus/latest/querying/operators/#one-to-one-vector-matches", "https://prometheus.io/docs/prometheus/latest/querying/examples/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# One-to-one matching with on and ignoring

By default a binary operator between two vectors pairs series with exactly the same label set (metric name excluded). If labels differ at all, the result is empty.

## Keywords
- `ignoring(a, b)`: ignore these labels when matching.
- `on(a, b)`: match only on these labels.

## Examples
```promql
# errors have label code, totals do not: ignore it
rate(http_errors_total{code="500"}[5m]) / ignoring(code) rate(http_requests_total[5m])

# memory usage vs limit from different exporters with different label sets: match on pod identity
sum by (namespace, pod) (container_memory_working_set_bytes{container!=""})
  / on (namespace, pod)
sum by (namespace, pod) (kube_pod_container_resource_limits{resource="memory"})
```
Result labels: arithmetic keeps the left-hand side's labels (minus the metric name); comparison filters return the matching left-hand series.

## Debugging empty results
1. Run each side alone; compare label sets (`{__name__=~"a|b"}` in the table view).
2. Look for extra labels: `instance` formats (`ip:port` vs hostname), `job` differences, exporter-added labels (`container`, `endpoint`, `service`).
3. Aggregate both sides to the common labels first with `sum by (...)`, then match with `on` the same labels.

## Gotchas
- If multiple series on either side share the same matching labels, you get "many-to-many matching not allowed" (or need `group_left`).
- `on()` with an empty list matches everything to everything: only valid when each side has one series (Prometheus 3.15.0 with several series on a side: `multiple matches for labels: many-to-one matching must be explicit (group_left/group_right)`).
- Run on 3.15.0: `rate(http_errors_total{code="500"}[5m]) / ignoring(code) rate(http_requests_total[5m])` returns one series with labels `instance` and `job` (no `code`); without `ignoring(code)` the result is empty.

## Verify
- [ ] Each side's series count after aggregation equals the result series count for one-to-one ratios.
