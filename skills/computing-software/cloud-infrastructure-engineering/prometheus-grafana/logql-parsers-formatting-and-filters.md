---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.logql-parsers-formatting-and-filters
name: logql-parsers-formatting-and-filters
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [logql, logql-parsers, pattern-parser-usage, pattern-syntax, unwrap-aggregations, quantile-over-time-logs, rate-counter, line-format-templates, logql-template-functions, ip-matcher, ip-filter, drop-keep-labels, keep-labels]
level: advanced
status: verified
description: "Write advanced LogQL: pattern parser, unwrap range aggregations (quantile_over_time, rate_counter), line_format templates, ip() matching, and drop/keep stages."
sources: ["https://grafana.com/docs/loki/latest/query/log_queries/", "https://grafana.com/docs/loki/latest/query/metric_queries/", "https://grafana.com/docs/loki/latest/query/template_functions/", "https://grafana.com/docs/loki/latest/query/ip/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LogQL: parsers, unwrap, formatting, filters

## Pattern parser
For fixed-format lines (nginx, envoy) it's faster and simpler than regex:
```logql
{app="nginx"} | pattern `<ip> - - [<_>] "<method> <uri> <_>" <status> <size> <_> "<agent>" <_>`
              | status >= 500
```
`<name>` captures, `<_>` skips; literals must match exactly; captures stop at the next literal.

## Unwrap: metrics from values in logs
```logql
quantile_over_time(0.99,
  {app="nginx"} | pattern `<_> - - [<_>] "<_>" <status> <_> <latency>`
                | unwrap latency [5m]) by (status)
sum by (route) (rate_counter({app="api"} | logfmt | unwrap requests_total [5m]))   # counter values in logs
avg_over_time({app="worker"} | json | unwrap duration(took) [5m])                 # duration("1.5s") / bytes("10MB") converters
```
Group explicitly: without `by (...)` an unwrapped `avg_over_time`/`quantile_over_time`/`rate_counter` returns one series per label set (30 series from 3 streams in a test). `rate`, `rate_counter` and `sum_over_time` accept no `by (...)` (parse error): wrap them in `sum by (...)`.
Lines where the unwrapped value doesn't parse produce `__error__`; drop with `| __error__=""`.

## line_format and template functions
```logql
{app="api"} | json | line_format `{{ .level | upper }} {{ .method }} {{ .path }} {{ printf "%.0fms" (mulf .duration_s 1000) }}`
{app="api"} | json | label_format svc=`{{ .service | lower }}`, slow=`{{ if gt (float64 .duration_s) 1.0 }}yes{{ else }}no{{ end }}`
```
Functions include `upper`, `lower`, `trim`, `replace`, `regexReplaceAll`, `default`, `toDateInZone`, `unixEpoch`,
`addf`/`mulf`/`divf`, `b64dec`, `urldecode`, `__line__`, `__timestamp__`.

## IP matching
```logql
{app="nginx"} |= ip("10.0.0.0/8")                          # line filter
{app="nginx"} | logfmt | remote_addr = ip("192.168.4.5-192.168.4.20")   # label filter
```
Supports single IP, range, CIDR, IPv4 and IPv6.

## drop and keep
```logql
{app="api"} | json | drop trace_id, span_id, __error__              # remove labels
{app="api"} | json | keep level, method, status                      # keep only these (+ stream labels selectors)
{app="api"} | json | drop level="debug"                              # drop label only when it has that value
```
Reduces result series in metric queries and noise in Explore.

## Verify
- [ ] Explore shows parsed fields without `__error__` for the sample stream.
- [ ] Metric queries return a bounded number of series (check legend count).

## Checked
Ran Loki 3.7.9 on nginx-style, JSON and logfmt lines: `pattern` parser with `status >= 500`, `quantile_over_time ... unwrap latency ... by (status)` (the original pattern did not match a common-log line, replaced with one that does), `rate_counter`, `unwrap duration(took)`, `line_format`/`label_format` with `upper`, `lower`, `mulf`, `addf`, `divf`, `trim`, `replace`, `default`, `regexReplaceAll`, `unixEpoch`, `b64dec`, `urldecode`, `__line__`, `__timestamp__`, `toDateInZone` (signature from the template_functions docs), `ip()` for CIDR, range and IPv6 forms, `drop` and `keep`. Docs read: query/template_functions, query/ip, query/metric_queries (grouping rules).
