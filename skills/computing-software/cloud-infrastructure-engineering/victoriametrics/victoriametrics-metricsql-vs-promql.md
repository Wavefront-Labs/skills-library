---
id: computing-software.cloud-infrastructure-engineering.victoriametrics.victoriametrics-metricsql-vs-promql
name: victoriametrics-metricsql-vs-promql
category: computing-software
field: cloud-infrastructure-engineering
product: victoriametrics
tags: [metricsql, promql, with-templates, keep-metric-names, rollup, default-operator, lookbehind]
level: advanced
status: docs-checked
description: "Write MetricsQL using its differences from PromQL: implicit windows, WITH templates, default and if operators, and keep_metric_names."
sources: ["https://docs.victoriametrics.com/victoriametrics/metricsql/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Victoriametrics metricsql vs promql

MetricsQL is backwards compatible with most PromQL but behaves differently in places.

- `rate()` and `increase()` use the last raw sample before the lookbehind window, so no increase is lost between windows, and they do not extrapolate (integer counters give integer increases). `rate()` still returns results when the step is smaller than the sample interval. `rate_prometheus` and `increase_prometheus` (from v1.120.0) match Prometheus semantics.
- Lookbehind windows are optional: `rate(node_network_receive_bytes_total)` works. For most rollups the default window is `step`; for `default_rollup` and `rate` it is `max(step, scrape_interval)`. The `i` suffix means steps: `rate(metric[10i] offset 5i)`.
- NaN values are dropped, so `(-1)^0.5` is empty.
- Metric names are dropped by functions and binary operators unless you add `keep_metric_names`; without it, mixed names can cause a `duplicate time series` error. Example: `rate({__name__=~"foo|bar"}) keep_metric_names`.

Extras:
- `WITH (commonPrefix="long_metric_prefix_") {__name__=commonPrefix+"suffix1"} / {__name__=commonPrefix+"suffix2"}`.
- Durations can appear anywhere (`sum_over_time(m[1h]) / 1h`); a missing suffix means seconds; `K`, `Ki`, `M`, `Mi` number suffixes and `1_234_567` underscores work.
- `@` modifier: `sum(foo) @ end()`.
- Selectors with `or`: `{env="prod",job="a" or env="dev",job="b"}`; Graphite style `{__graphite__="foo.*.bar"}`.
- Operators: `q1 default q2`, `q1 if q2`, `q1 ifnot q2`, numeric sets `status_code == (300, 301, 304)`, `group_left(*) prefix "ns_"`.
- Aggregates take many arguments and a `limit N` suffix, for example `sum(x) by (y) limit 3`.
- `histogram_quantile` accepts an optional `boundsLabel` third argument; `rollup(m[d])` returns min, max and avg.

## Checked

2026-11-03. Flags, endpoints, HTTP paths, defaults, limits and version gates were checked against the official VictoriaMetrics documentation pages cited in `sources` (docs.victoriametrics.com, fetched this batch) with a phrase-by-phrase comparison. No wrong claims were found; no claims were removed.

Method: documentation only; no commands were run.
