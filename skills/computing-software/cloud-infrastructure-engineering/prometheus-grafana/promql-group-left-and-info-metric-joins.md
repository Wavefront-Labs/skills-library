---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-group-left-and-info-metric-joins
name: promql-group-left-and-info-metric-joins
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, vector-matching, group-left, many-to-one-matching, group-left-labels, group-operator, info-metric-join-aggregation, info-function]
level: advanced
status: docs-checked
description: "Join metadata labels onto series with on() and group_left, collapse the one side with group, and use the experimental info() function instead."
sources:
  - https://prometheus.io/docs/prometheus/latest/querying/operators/#vector-matching
  - https://prometheus.io/docs/prometheus/latest/querying/functions/#info
  - https://www.robustperception.io/how-to-have-labels-for-machine-roles/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# group_left and info-metric joins

## Pattern
```promql
<many side>  * on (<join labels>) group_left (<labels to copy>)  <one side>
```
- `on(...)` restricts matching to the listed labels; `ignoring(...)` matches on everything else.
- `group_left` allows many-to-one matching where the left vector has the higher cardinality; `group_right` is the mirror. The label list on the modifier names extra labels to copy from the "one" side into the result.
- Group modifiers work only with comparison, arithmetic and trigonometric operators, not with `and`, `or` or `unless`.
- With `on`, a label can only appear in one of the lists, and every series in the result must be uniquely identifiable.
- The manual's advice: many-to-one matching is an advanced case, and often `ignoring(<labels>)` alone gives the result you want.

Worked example from the Robust Perception post, where a textfile-collector metric `machine_role{role="apache"} 1` carries a role that would be a bad target label because it changes over a machine's life:
```promql
up * on (instance, job) group_left(role) machine_role{role="apache"}

sum by (job, role) (
  up * on (instance, job) group_left(role) machine_role{role="apache"}
)
```
The info-style series has value 1, so multiplying keeps the left-hand value while the role label is copied over. The same pattern works for any metadata series you expose (illustrative names):
```promql
sum by (job, instance) (rate(http_requests_total[5m]))
  * on (job, instance) group_left (version)
    app_build_info
```
In an arithmetic operation between vectors the metric name is dropped, even if `__name__` is in `on`.

## group() to make the one side unique
`group(v)` returns 1 for each group that has any value, so `group by (<join labels>, <copied labels>) (<info metric>)` collapses the right side to one series per label set before the join:
```promql
... * on (job, instance) group_left (version)
  group by (job, instance, version) (app_build_info)
```
This matters because the result must be uniquely identifiable. The `info()` page describes the failure case: when an info series changes a data label and the old series is not marked stale, the query fails for up to 5m (the lookback delta) because it finds a conflicting match with both the old and the new series.

## info() function (experimental)
```promql
info(rate(http_server_request_duration_seconds_count[2m]), {k8s_cluster_name=~".+"})
info(rate(http_server_request_duration_seconds_count[2m]))   # add all data labels
```
- Experimental: behaviour may change, including removal. Enable with `--enable-feature=promql-experimental-functions`.
- For each series in the first argument it finds info series with matching identifying labels and adds their data (non-identifying) labels. The optional second argument is a set of label matchers only, in curly braces.
- It resolves a conflict between old and new versions of an info series in favour of the newer one.
- If no info series matches and any matcher in the second argument does not match the empty string (such as `=~".+"`), the series is dropped; if all matchers match the empty string or there is no second argument, the series is returned without enrichment.
- Limitations: it considers only `target_info` by default and assumes the identifying labels are always `instance` and `job`. Other names via `__name__`, e.g. `{__name__=~"(target|build)_info"}`. With only negated `__name__` matchers it considers all metrics matching `.+_info`.

## Verify
- [ ] The joined query returns the same number of series as the left side alone.
- [ ] Removing the group-by on the one side reproduces the uniqueness failure you are guarding against.

## Checked
Checked 2026-11-08 against the PromQL operators page (vector matching, group modifiers, name dropping, group aggregation), the functions page (info) and the Robust Perception machine-roles post. Removed because the pages do not state them: kube-state-metrics `kube_pod_labels` and container CPU examples, the node_uname_info example, the exact many-to-many error text, "max by also works", "copied labels overwrite same-named left labels", the claim about instance format mismatches, and the "Prometheus 3.x" version tag.

Method: docs-only read of cited pages, 2026-11-08
