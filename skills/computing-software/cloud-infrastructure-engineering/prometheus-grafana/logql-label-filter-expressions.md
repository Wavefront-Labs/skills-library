---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.logql-label-filter-expressions
name: logql-label-filter-expressions
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [logql-label-filters, label-filter-expression, logql, logql-parsers, error-label]
level: practitioner
status: verified
description: "Filter parsed logs with LogQL label filters: string, numeric, duration and bytes comparisons, and/or logic, type coercion and handling __error__."
sources: ["https://grafana.com/docs/loki/latest/query/log_queries/#label-filter-expression", "https://grafana.com/docs/loki/latest/query/log_queries/#parser-expression", "https://grafana.com/docs/loki/latest/query/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LogQL label filter expressions

After a parser (`json`, `logfmt`, `pattern`, `regexp`), extracted fields are labels you can filter on.

## Types
```logql
{app="api"} | json | level = "error"                      # string (=, !=, =~, !~)
{app="api"} | logfmt | status >= 500                      # number (==, !=, >, >=, <, <=)
{app="api"} | logfmt | duration > 2s                      # duration (ns, us, ms, s, m, h)
{app="api"} | json | response_size > 1MB                  # bytes (B, KB, MB, KiB, MiB...)
{app="api"} | json | level="error" or (status >= 500 and route!="/health")
{app="api"} | json | level="error", status>=500           # comma = and
```

## Type coercion and errors
- Numeric/duration/bytes comparisons try to convert the label value; a failed conversion keeps the line but sets `__error__="LabelFilterErr"` (with `__error_details__`, for example `time: missing unit in duration "0.05"`). Add `| __error__=""` to drop those lines. A duration filter needs a value with a unit suffix (`2.5s`, not `2.5`); a bytes filter converts `1255KB` and accepts `1KiB`, `1000B`, `1MB`.
- Parser failures (`JSONParserErr`, `LogfmtParserErr`) also set `__error__`:
```logql
{app="api"} | json | __error__ != ""          # find unparsable lines
{app="api"} | json | __error__ = ""           # explicitly exclude them
```
- In metric queries, any `__error__` makes the query fail; add `| __error__=""` before aggregation.

## Placement
Label filters can appear before or after `line_format`; put them as early as possible after the parser. Filters on stream labels belong in the selector `{...}`, not in a label filter.

## Gotchas
- `| json` extracts all fields (expensive on wide JSON); use `| json status, route` to extract only what you need.
- Label names with dots/dashes are sanitised to underscores by parsers (`a.b` became `a_b`, `user-agent` became `user_agent`; nested `http.status` became `http_status`).
- `=~` and `!~` on labels are fully anchored (`level=~"err"` matched nothing, `level=~"err.*"` matched).

## Verify
- [ ] Metric queries over parsed fields run without `__error__` failures across 24h.

## Checked
Ran Loki 3.7.9 (windows-amd64, local TSDB v13) with 60 JSON lines, 60 logfmt lines and one non-JSON line, and queried it through the HTTP API: string, number, duration and bytes comparisons, `or`/`and`/comma forms, `__error__` filtering, selective `| json status, route`, and the metric query that fails on `JSONParserErr` and works with `| __error__=""`. The doc claim that a failed label filter drops the line was wrong (the line is kept with `LabelFilterErr`). Docs read: Loki query/log_queries (label filter types, duration and bytes units).
