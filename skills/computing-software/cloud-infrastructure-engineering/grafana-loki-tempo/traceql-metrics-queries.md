---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.traceql-metrics-queries
name: traceql-metrics-queries
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [traceql-metrics, tempo, rate, quantile_over_time, histogram_over_time, compare, metrics-from-traces]
level: practitioner
status: docs-checked
description: "Compute rate, error and latency series from traces with TraceQL metrics functions, sampling hints, exemplars and the query_range API."
sources: ["https://grafana.com/docs/tempo/latest/metrics-from-traces/metrics-queries/", "https://grafana.com/docs/tempo/latest/metrics-from-traces/metrics-queries/functions/", "https://grafana.com/docs/tempo/latest/metrics-from-traces/metrics-queries/configure-traceql-metrics/", "https://grafana.com/docs/tempo/latest/metrics-from-traces/metrics-queries/sampling-guide/", "https://grafana.com/docs/tempo/latest/api_docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: RED metrics computed ad hoc from stored spans (TraceQL metrics), powered by the TraceQL metrics API on the query-frontend.

Functions (append to a span selector): `rate`, `count_over_time`, `sum_over_time`, `min_over_time`, `max_over_time`, `avg_over_time`, `quantile_over_time`, `histogram_over_time`, `compare`. Optional `by()` groups; `topk()`/`bottomk()` and comparison operators go after the metrics query.
```traceql
{ resource.service.name = "foo" && span:status = error } | rate() by (span.http.route)
{ span:name = "GET /:endpoint" } | quantile_over_time(span:duration, .99, .9, .5) by (span.http.target)
{ span:name = "GET /:endpoint" } | count_over_time() by (span.http.status_code)
{ } | histogram_over_time(span:duration) by (span.http.target)
{ } | rate() by (resource.service.name) | topk(10)
100 * ({status=error} | rate()) / ({} | rate())
{ resource.service.name="a" && span.http.path="/myapi" } | compare({span:status=error})
```
`compare({subset filter}, <topN>, <start>, <end>)` splits spans into selection and baseline; run it as an instant query, and it cannot be used in arithmetic expressions or with comparison operators, `topk` or `bottomk`. Arithmetic needs each sub-query in parentheses.

API: `GET /api/metrics/query_range` with `q`, `start`, `end`, `since` (default 1h), `step` (dynamic if omitted), `exemplars`; `GET /api/metrics/query` is the instant version (no `step`). Parameters must be URL-encoded. In Grafana (Cloud or 10.4+) use Explore with the Tempo data source; no extra setup needed.

Config (`query_frontend.metrics`): default max range 24h (`max_duration`; the normal TraceQL max is 168h); `query_backend_after` default 15m; tune `concurrent_jobs` and `target_bytes_per_job` (docs: cloud ~1000 jobs of ~225 MB; on-prem 8 jobs of ~1.25 GB). Raise timeouts: `querier.search.query_timeout`, `server.http_server_read_timeout`, `server.http_server_write_timeout`, and any proxy in front of Grafana.

Exemplars: set `query_frontend.metrics.max_exemplars` or use the hint `with (exemplars=true)`.

Sampling hints for speed: `with(sample=true)` (dynamic, safe for most queries), `with(span_sample=0.1)`, `with(trace_sample=0.1)` (for structural or spanset queries), `with(sample=0.xx)`. Sampling needs Tempo 3.0 or later. Heavy queries like `{ } | rate()` gain about 2-4 times.

vParquet5 uses a span-only fetch layer by default for non-structural metrics queries; opt out with `with (spanonly_fetch=false)` (needs `unsafe_query_hints`) or the per-tenant override `read.metrics_spanonly_fetch: false`. Experimental extrapolation of ingest-time sampling: `with (extrapolate=true)` or `read.metrics_extrapolate: true`.

Gotchas
- Queries are expensive; time out in proxies before Tempo is the usual failure.
- Sampled results are approximate and may under-sample rare events.

## Verify
Run `{ } | rate()` in Explore over the last hour and confirm a non-empty series; compare with span-metrics `traces_spanmetrics_calls_total` rate if you generate it.

## Checked
2026-11-03. Confirmed against the TraceQL metrics overview, functions, configure, sampling and HTTP API pages. Removed: the claim that the `local-blocks` processor and `flush_to_storage` are required (not in current docs; `local-blocks` was removed in Tempo 3.0), `GET` example parameters with `step=60s` implying Explore-only behaviour, the sampled-estimate claim for large ranges, and bare `duration` examples (docs use `span:duration`).
Method: documentation only; no commands were run.
