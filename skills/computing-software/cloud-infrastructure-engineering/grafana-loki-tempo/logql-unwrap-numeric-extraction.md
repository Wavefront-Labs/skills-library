---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.logql-unwrap-numeric-extraction
name: logql-unwrap-numeric-extraction
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [logql-unwrap, loki, unwrap, quantile_over_time, sum_over_time, duration-conversion, bytes-conversion]
level: practitioner
status: docs-checked
description: "Extract numbers from log lines with LogQL unwrap and aggregate them with quantile_over_time, sum_over_time and rate."
sources: ["https://grafana.com/docs/loki/latest/query/metric_queries/#unwrapped-range-aggregations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: latency percentiles or byte counts from fields inside logs.

```logql
# p95 of a duration label (logfmt lines such as duration=250ms route=/api) per route
quantile_over_time(0.95,
  {app="api"} | logfmt | unwrap duration(duration) [5m]
) by (route)

# sum of bytes sent per host
sum by (host) (sum_over_time({job="nginx"} | json | unwrap bytes_sent [1m]))

# average value, dropping lines that fail conversion
avg_over_time({app="api"} | logfmt | unwrap latency_ms | __error__="" [5m]) by (route)
```
`unwrap <label>` uses the label value as the sample; by default Loki tries to convert it to a 64-bit float, and on failure adds the `__error__` label to the sample. Conversion functions: `duration_seconds(label)` (short form `duration(label)`) parses Go duration strings such as `5m` or `24s30ms`; `bytes(label)` parses sizes such as `5 MiB`, `3k` or `1G`.

Unwrapped range functions: `rate`, `rate_counter`, `sum_over_time`, `avg_over_time`, `min_over_time`, `max_over_time`, `first_over_time`, `last_over_time`, `stdvar_over_time`, `stddev_over_time`, `quantile_over_time(scalar, ...)` and `absent_over_time`. All support `by`/`without` grouping except `sum_over_time`, `absent_over_time`, `rate` and `rate_counter`.

Gotchas
- End the log query with the unwrap expression, optionally followed by a label filter such as `__error__=""` to discard conversion errors.
- The unwrapped label is not kept in the result unless you group by it; group with `by (...)` for the labels you want.

## Verify
Run the query in Explore: one series per route with no `__error__` values. Compare with a known request using `logcli query` on the same selector.

## Checked
2026-11-03. Confirmed against the Loki "Metric queries" page (unwrap, conversion functions, function list, grouping exception). Removed: `__error_details__`, `0.25s`/`10MB` examples (replaced by documented forms), the `logcli` cardinality and cost gotchas not stated on the page.
Method: documentation only; no commands were run.
