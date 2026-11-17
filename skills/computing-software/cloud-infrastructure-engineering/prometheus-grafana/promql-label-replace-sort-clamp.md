---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-label-replace-sort-clamp
name: promql-label-replace-sort-clamp
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, label-replace-usage, label-join-usage, sort-by-label, clamp-functions, round-function, label-manipulation]
level: practitioner
status: verified
description: "Reshape PromQL results: label_replace and label_join to align labels for joins, sort/sort_by_label for tables, clamp/clamp_min/clamp_max and round for display and guards."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/functions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# label_replace, label_join, sort, clamp, round

## label_replace(v, dst, replacement, src, regex)
```promql
# Extract host from instance "10.0.0.5:9100" to join with a metric labelled by host
label_replace(up{job="node"}, "host", "$1", "instance", "([^:]+):\\d+")
# Make kube metrics joinable with node_exporter: node -> instance
label_replace(kube_node_info, "instance", "$1:9100", "internal_ip", "(.*)")
# Rename a label (copy then ignore the old one in aggregation)
sum by (service) (label_replace(rate(x[5m]), "service", "$1", "job", "(.*)"))
```
- Regex is fully anchored (docs); if it doesn't match, the series is returned **unchanged** (no error).
- Capture groups `$1`, `${1}` and named groups `$name`; `$1abc` reads a group called `1abc` (empty), so write `${1}abc` (3.15.0: `${1}abc` produced `host=1abc`, `$1abc` produced no `host` label).
- Backslashes double inside the PromQL string literal (`\\d`); a single `\d` is a parse error (`unknown escape sequence U+0064 'd'`), the doubled form worked on 3.15.0.

## label_join(v, dst, separator, src1, src2, ...)
```promql
label_join(kube_pod_info, "pod_ns", "/", "namespace", "pod")    # "default/web-7d9"
```

## Sorting (instant queries only; range results are not ordered)
```promql
sort_desc(sum by (namespace) (rate(container_cpu_usage_seconds_total[5m])))
sort_by_label(kube_pod_info, "namespace", "pod")         # experimental: needs --enable-feature=promql-experimental-functions (3.15.0: `function "sort_by_label" is not enabled` without it)
sort_by_label_desc(...)
```

## Clamp and round
```promql
clamp_min(free_bytes / total_bytes, 0)              # guard negative values from bad exporters
clamp_max(rate(x[5m]) / capacity, 1)                # utilisation never shows > 100%
clamp(v, 0, 100)                                    # both bounds
round(increase(orders_total[1h]))                   # whole numbers for tables
round(latency_seconds, 0.001)                       # to the nearest millisecond
```
Round in display (Grafana decimals) when possible; round in PromQL only when the value itself should be integral.

## Verify
- [ ] Joins after label_replace return the expected series count (no silent non-matches).
- [ ] Table panels using sort functions are instant queries.
