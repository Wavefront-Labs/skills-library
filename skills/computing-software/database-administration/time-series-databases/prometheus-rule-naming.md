---
id: computing-software.database-administration.time-series-databases.prometheus-rule-naming
name: prometheus-rule-naming
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-recording, prometheus-rule-naming, prometheus]
level: practitioner
status: docs-checked
description: "Name recording rules level:metric:operations so they are discoverable, and aggregate ratios correctly with a without clause."
sources:
  - https://prometheus.io/docs/practices/rules/
  - https://prometheus.io/docs/practices/naming/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rule naming conventions

**Goal:** Name recording rules so they are discoverable and unambiguous.

## Steps
- General form `level:metric:operations`, for example `job:request_latency_seconds_count:avg_rate5m`.
- `level` is the aggregation level and labels of the rule output.
- `metric` is the metric name, unchanged except for stripping `_total` off counters when using `rate()` or `irate()`.
- `operations` lists the operations applied, newest first. `_sum` is omitted if there are other operations, and associative operations can be merged (`min_min` is `min`). If no operation is obvious, use `sum`.
- For a ratio by division, separate the metrics with `_per_` and call the operation `ratio`.
- When aggregating ratios, aggregate numerator and denominator separately and then divide; do not average a ratio or an average.
- Always use a `without` clause listing the labels you aggregate away, so other labels such as `job` are preserved. The labels in `without` disappear from the `level` of the output name.
- Example: `path:requests:rate5m` from `sum without (instance)(instance_path:requests:rate5m{job="myjob"})`.
- Metric names should use base units with a unit suffix in plural form (for example `_seconds`, `_bytes`).

**Gotcha:** If the level in the output name does not match the labels left after aggregation, a mistake has likely been made in the rule.

## Verify
- `promtool check rules` passes on the file.
- Names follow `level:metric:operations` across the file.

## Checked
2026-11-03. Confirmed against the Prometheus recording rule practices page (naming form, `_total` stripping, newest-first operations, `_per_`/`ratio`, aggregation rules, without clause) and the metric naming page (base units, unit suffix). Removed: the `job:node_cpu_seconds:avg_rate5m` example (replaced by the documented-style one), the `instance:cluster` level example, one-file-per-team advice, and the claim about reusing raw metric names (not on a page read).
Method: documentation only; no commands were run.
