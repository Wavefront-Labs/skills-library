---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.logql-queries
name: logql-queries
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, loki, logql, logql-queries, logql-pipeline, logql-parsers, logql-metric-queries, stream-selector, line-filter, label-filter, json-parser, logfmt-parser, pattern-parser, regexp-parser, unwrap, rate, count-over-time, bytes-rate, sum-by, topk, line-format, label-format, unpack, structured-metadata, query-performance, logcli]
level: practitioner
status: verified
description: "Write fast, correct LogQL: stream selectors, line filters before parsers, json/logfmt/pattern parsers, label filters, line_format, and metric queries (rate, count_over_time, unwrap quantiles)."
sources: ["https://grafana.com/docs/loki/latest/query/", "https://grafana.com/docs/loki/latest/query/log_queries/", "https://grafana.com/docs/loki/latest/query/metric_queries/", "https://grafana.com/docs/loki/latest/query/bp-query/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LogQL queries

**Goal:** find the lines you need in seconds and turn logs into metrics for panels and
alerts, without melting the queriers.

## 1. Shape of a query
```
{stream selector}  |= "line filter"  | parser  | label filter  | line_format ...   # log query
<agg>( <range fn>( {selector} ... [5m] ) ) by (labels)                           # metric query
```
Order matters for speed: **selector → line filters → parser → label filters**. Line filters
run on raw bytes (cheap); parsers allocate per line (expensive);
label filters after a parser run on parsed fields.

## 2. Stream selector and line filters
```logql
{namespace="prod", app=~"api|worker", container!="istio-proxy"}
{app="api"} |= "error" != "healthcheck" |~ "status=5\\d\\d" !~ "(?i)debug"
{app="api"} |= `user_id="42"`          # backticks: no escaping
{app="api"} |= ip("10.0.0.0/8")        # ip filter
```
Selectors need at least one non-empty matcher. `=~` is anchored RE2. Several `|=` are
AND. Case-insensitive via `(?i)`.

## 3. Parsers
| Parser | Use when | Note |
|---|---|---|
| `| json` | JSON lines | nested keys flattened with `_` (`http_status`); `| json status="http.status"` extracts selectively (cheaper) |
| `| logfmt` | `key=value` lines | `--strict` stops at the first malformed pair and sets `__error__` (non-strict skips bad pairs); `logfmt status, path` selective |
| `| pattern "<ip> - - <_> \"<method> <path> <_>\" <status> <size>"` | fixed-format text (nginx, Apache) | `<_>` skips |
| `| regexp "(?P<method>\\w+) (?P<path>\\S+)"` | anything else | named groups become labels |
| `| unpack` | Promtail/Alloy `pack` stage | restores embedded labels |
Parse errors add `__error__`/`__error_details__` labels; drop them with `| __error__=""` or
inspect them. Labels extracted by parsers are **query-time** and free in cardinality terms.

## 4. Label filters, formatting
```logql
{app="api"} | json | status >= 500 and duration > 1s | path =~ "/api/v2/.*"
{app="api"} | logfmt | level="error" | line_format "{{.ts}} {{.method}} {{.path}} -> {{.status}} ({{.duration}})"
{app="api"} | json | label_format service=`{{ .app }}-{{ .env }}` | drop pod, container
{app="api"} | json | duration > 500ms | keep path, status, duration
```
Label filters understand durations (`1s`, `500ms`), bytes (`10MB`), numbers and strings.
`line_format` uses Go templates with sprig functions (`{{ .level | upper }}`, `{{ __timestamp__ }}`,
`{{ regexReplaceAll }}`); `decolorize` strips ANSI.

## 5. Metric queries
```logql
# log lines per second by app (unwrapped count)
sum by (app) (rate({namespace="prod"} |= "error" [5m]))
# count per interval (for bars)
sum by (status) (count_over_time({app="api"} | json | __error__="" [1m]))
# bytes
sum(bytes_rate({namespace="prod"}[5m])) by (app)
# latency quantiles from a parsed field
quantile_over_time(0.99, {app="api"} | json | unwrap duration [5m]) by (path)   # unwrap duration(...) / bytes(...) converts units
sum by (path) (sum_over_time({app="api"} | json | unwrap bytes_sent [1m]))
avg_over_time({app="api"} | logfmt | unwrap latency_ms [5m]) by (route)
# ratio
sum(rate({app="api"} | json | status >= 500 [5m])) / sum(rate({app="api"} | json [5m]))
# top talkers
topk(5, sum by (pod) (rate({namespace="prod"}[5m])))
# absence
absent_over_time({app="batch"} |= "run complete" [2h])
```
Range functions over **log lines**: `rate`, `count_over_time`, `bytes_rate`,
`bytes_over_time`, `absent_over_time`. Over **unwrapped values** (`rate`, `rate_counter`, `sum_over_time` and `absent_over_time` take no `by (...)`: wrap them in `sum by (...)`): `rate`, `sum_over_time`,
`avg/min/max/stddev/stdvar/first/last/quantile_over_time`, `rate_counter`. Aggregations
match PromQL (`sum`, `avg`, `topk`, `bottomk`, `count`, `max`, `min`, `sort`). Offsets and
binary ops work as in PromQL. `offset` goes inside the range selector: `count_over_time({job="mysql"}[5m] offset 5m)`; after the range it is invalid.

## 6. Performance habits
- Narrow the **selector** first (namespace + app), then a literal `|=` before any parser.
- Prefer `pattern`/`logfmt` over `regexp`; prefer selective `json field="path"` over full `json`.
- Keep ranges in alerts short (`[5m]`), and let the query-frontend split long dashboard ranges.
- Use `/loki/api/v1/index/volume` and `--stats` from `logcli` to see bytes
  scanned: `logcli query --stats '{app="api"} |= "x"' --since=1h`.
- Structured metadata (`trace_id`, `pod`) is filterable without a parser: `{app="api"} | trace_id="abc"`.

## 7. logcli
```bash
export LOKI_ADDR=https://loki.internal LOKI_ORG_ID=team-payments
logcli labels ; logcli labels app ; logcli series '{namespace="prod"}' --analyze-labels
logcli query '{app="api"} |= "error"' --since=2h --limit=500 --forward -o jsonl
logcli instant-query 'sum(rate({app="api"}[5m]))'
```

## Gotchas
- A matcher that can match the empty string (`app=~".*"`) is rejected ("queries require at least one regexp or equality matcher that does not have an empty-compatible value"); `app=~".+"` is accepted but selects every stream, so use literal matchers.
- `| json` on non-JSON lines sets `__error__=JSONParserErr`; an `=` label filter on a missing field then drops them, but a `!=` filter keeps them, and a metric query fails outright until you add `| __error__=""`.
- `unwrap` of a non-numeric value (for example `2.5s` without `duration(...)`) yields `__error__=SampleExtractionErr` and fails a metric query; an unwrap of a field that does not exist returns no series. `sum_over_time(...) by (x)` is a parse error (grouping not allowed).
- Query limits (Loki 3.7.9 defaults: `max_entries_limit_per_query` 5000, `max_query_series` 500, `max_query_length` 30d1h) reject or truncate queries.
- `rate()` on logs is lines/sec, not a counter rate; `rate_counter` is the counter version for unwrapped values.

## Verify
- [ ] `logcli query --stats` shows bytes processed dropping when you add the line filter before the parser.
- [ ] Metric query returns the same count as the log query's line count for the same range.
- [ ] No `__error__` labels in the result set of your dashboard queries.

## Checked
Ran Loki 3.7.9 and logcli 3.7.9 on 60+ JSON, logfmt, nginx and nested-JSON lines through the HTTP API and logcli: selectors and empty-matcher rejection, line filters, json/logfmt/pattern/regexp/unpack parsers, nested key flattening and selective `json status="http.status"`, label filters, `line_format`/`label_format`/`drop`/`keep`, every metric query on the page (rate, count_over_time, bytes_rate, quantile_over_time, sum/avg_over_time, rate_counter, topk, absent_over_time, sort, offset), `unwrap duration(...)`, structured-metadata filter without a parser, `logcli labels|series --analyze-labels|query --stats|instant-query|volume`, `/index/volume`, and `LOKI_ORG_ID`/`LOKI_ADDR` in `logcli --help`. Corrections: `toUpper` is not a template function (use `upper`), `app=~".*"` is rejected, `logfmt --strict` flags errors rather than dropping, grouping is not allowed on `sum_over_time`/`rate`. Docs read: query/log_queries, query/metric_queries (function lists, `offset` placement), query/template_functions.
