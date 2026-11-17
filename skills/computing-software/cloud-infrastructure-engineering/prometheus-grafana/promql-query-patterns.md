---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.promql-query-patterns
name: promql-query-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [promql, prometheus, query-patterns, vector-matching, group-left, group-right, on-modifier, ignoring-modifier, info-metrics, label-replace, label-join, topk, bottomk, count-values, or-vector, unless, absent-over-time, predict-linear, deriv, delta, over-time-functions, quantile-over-time, subqueries, offset, at-modifier, bool-modifier, changes, clamp-min]
level: advanced
status: docs-checked
description: "PromQL patterns checked against the Prometheus docs: vector matching and group_left, set operators, bool, topk, absent, label functions, subqueries, offset and @."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/operators/", "https://prometheus.io/docs/prometheus/latest/querying/functions/", "https://prometheus.io/docs/prometheus/latest/querying/basics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PromQL query patterns

## Vector matching
Binary operations between vectors match entries with the exact same label set by default. `on(labels)` restricts the
match to the listed labels; `ignoring(labels)` ignores them.
```promql
method_code:http_errors:rate5m{code="500"} / ignoring(code) method:http_requests:rate5m
```
Without `ignoring(code)` there is no match because the label sets differ; entries with no match on the other side drop
out of the result.

### group_left / group_right
`group_left` allows many-to-one matching (the left side has higher cardinality); `group_right` the reverse. Labels listed
in the modifier are copied from the "one" side into the result. Every result series must be uniquely identifiable, and a
label can only appear in one of the `on` list and the group list. The docs say these are advanced and that
`ignoring(...)` alone often gives what you want. Group modifiers work with comparison, arithmetic and trigonometric
operators, not set operators.
```promql
left_vector * on (instance, job) group_left (info_label) right_vector     # shape of the docs' info-label example
```

## Set operators
`and` keeps left-side elements that have an exactly matching label set on the right (name and values come from the
left); `or` returns the left side plus right-side elements with no matching label set on the left; `unless` keeps left
elements with no match on the right.

## Comparisons: filter or bool
By default `x > 0.5` filters. With `bool` it returns 0 or 1 for every matched element and drops the metric name; elements
with no match still return nothing. Between two scalars `bool` is required.

## Aggregation
- `topk(k, v)` and `bottomk(k, v)` return a subset of k input samples with their original labels; `by`/`without` only
  bucket the input. They only act on floats, and no sorting applies to range queries.
- `count_values("version", build_version)` outputs one series per unique value, with the value in the named label and the
  count as the sample value.
- `limitk` and `limit_ratio` are experimental and need `--enable-feature=promql-experimental-functions`.

## Functions
- `delta(v[range])`: last minus first value of each series, extrapolated to the full range; for gauges.
- `deriv(v[range])`: per-second slope by simple linear regression, needs at least two float samples.
- `predict_linear(v[range], t)`: value t seconds from now by linear regression, needs at least two float samples.
- `changes(v[range])`: how many times the value changed in the range.
- `clamp_min(v, min)`: lower bound on float samples.
- `label_replace(v, dst, replacement, src, regex)`: expands `$1`/`$name` into dst when regex matches src, else returns
  the series unchanged. `label_join(v, dst, separator, src1, src2, ...)` joins label values.
- `absent(v)` and `absent_over_time(v[range])` return one series valued 1 only when the input is empty. They derive
  labels from the equality matchers of the selector (`absent(nonexistent{job="myjob"})` gives `{job="myjob"}`); over an
  aggregation such as `sum(...)` the result has no labels.

## Time modifiers and subqueries
- `offset` and `@` must immediately follow the selector: `sum(x{m="GET"} offset 5m)` is valid,
  `sum(x{m="GET"}) offset 5m` is invalid. Example: `rate(http_requests_total[5m] offset 1w)`.
- `@ <unix timestamp>`, `@ start()` and `@ end()` pin the evaluation time; `@` and `offset` can be combined in either
  order.
- Subquery syntax: `<instant_query>[<range>:<resolution>]`; the resolution is optional and defaults to the global
  evaluation interval. The result is a range vector, for example `max_over_time(sum(rate(x[5m]))[1d:5m])`.

## Verify
- [ ] Each join returns the series count you expect from its left side.
- [ ] Queries run in the Prometheus UI and the result labels are what an alert or dashboard needs.

## Checked

2026-11-08. Confirmed against the Prometheus operators, functions and basics pages (current docs). Removed as
unconfirmed: the info-metric duplicate-fix advice, `or vector(0)` and zero-fill advice, the topk-per-step graph
explanation, quantile_over_time and `*_over_time` notes, the `predict_linear` alert floor advice, the safe-division
tricks, NaN comparison notes, and the "enabled since 2.33" claim for `@`. The query examples page and the
kube-state-metrics source were not used.
Method: documentation only; no commands were run.
