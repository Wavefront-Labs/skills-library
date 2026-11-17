---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.traceql-structural-aggregate-and-metrics-queries
name: traceql-structural-aggregate-and-metrics-queries
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [traceql, structural-queries, ancestor-descendant-queries, traceql-aggregates, spanset-aggregates, traceql-metrics-queries, histogram-over-time-traceql, compare-function, span-scopes, event-scope, link-scope, instrumentation-scope, traceql-performance, search-tuning]
level: advanced
status: gated
description: "Write advanced TraceQL: scopes and intrinsics, structural operators, spanset aggregates, TraceQL metrics (rate, quantile_over_time, compare) and keeping searches fast."
sources: ["https://grafana.com/docs/tempo/latest/traceql/", "https://grafana.com/docs/tempo/latest/traceql/metrics-queries/", "https://grafana.com/docs/tempo/latest/operations/backend_search/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TraceQL: scopes, structure, aggregates, metrics

## Scopes and intrinsics
```traceql
{ span.http.response.status_code >= 500 }                   # span attribute
{ resource.service.name = "checkout" && resource.k8s.namespace.name = "prod" }
{ event.exception.type = "TimeoutError" }                   # span events
{ link:traceID != nil }                                      # spans with links (intrinsic form)
{ instrumentation:name = "io.opentelemetry.jdbc" }          # instrumentation scope (colon form; `instrumentation.name` matched nothing)
{ name = "SELECT orders" && kind = client && status = error && duration > 500ms }   # intrinsics
{ trace:rootService = "frontend" && trace:duration > 2s }    # trace-level intrinsics
```
Always prefer scoped attributes (`span.`, `resource.`) over unscoped `.attr`: unscoped searches both scopes (slower).

## Structural operators
```traceql
{ resource.service.name = "frontend" } >> { resource.service.name = "payments" && status = error }   # descendant
{ name = "HTTP GET /cart" } > { kind = client }                    # direct child
{ name = "load-profile" } ~ { name = "load-cart" }                 # siblings
{ resource.service.name = "checkout" } !>> { resource.service.name = "payments" }   # payments spans that are NOT descendants of a checkout span
{ } << { status = error }                                          # error spans that are ancestors of some span (matches the right-hand side)
```
## Spanset aggregates
```traceql
{ resource.service.name = "checkout" } | count() > 50              # traces with > 50 checkout spans (N+1 queries)
{ span.db.system = "postgresql" } | avg(duration) > 200ms
{ } | select(span.http.route, resource.service.version)            # add columns to results
```
## TraceQL metrics (Tempo 3.1.1 served these with no metrics-generator configuration; for older 2.x releases confirm the `local-blocks` requirement in that release's TraceQL metrics docs)
```traceql
{ resource.service.name = "checkout" && status = error } | rate() by (span.http.route)
{ kind = server } | quantile_over_time(duration, .5, .99) by (resource.service.name)
{ name = "GET /api/products" } | histogram_over_time(duration)
{ resource.service.name = "checkout" } | compare({ status = error })   # which attribute values are over-represented in errors
```
Run as range queries against `/api/metrics/query_range` (tested with `step=60s`), or in Grafana's Tempo data source / Traces Drilldown (gated: unconfirmed, source is paywalled or blocked): Grafana was not driven here. The default maximum range is 24h (`query_frontend.metrics.max_duration`).

## Performance
- Put the most selective, indexed condition first: `resource.service.name` and dedicated attribute columns
  (configure frequently queried attributes as dedicated columns in the parquet schema).
- Narrow the time range; use `limit`/`spss` (spans per spanset) in Grafana.
- Regex (`=~`, fully anchored) and unscoped attributes are slowest (Tempo tuning page: prefer scoped attributes).
- Backend search tuning: `querier.search.query_timeout`, `query_frontend.search.concurrent_jobs`, `query_frontend.search.target_bytes_per_job` (all accepted by `tempo -config.verify=true`).

## Verify
- [ ] Queries return in seconds over 1 h; Tempo query frontend shows no timeouts.
- [ ] Structural query finds the known failing path in a test trace.

## Checked
Ran Tempo 3.1.1 (windows-amd64, single binary, local backend, OTLP/HTTP receiver) and pushed 12 synthetic traces through `/v1/traces` (frontend root span, payments child with an `exception` event on 4 error traces, checkout database spans, instrumentation scope names, int and string attributes), then queried `/api/search`, `/api/metrics/query_range` and `tempo-cli` 3.1.1. Every query in the page was run (annotations after `#` removed, since `#` is a parse error): scopes and intrinsics, `>>`, `>`, `~`, `!>>`, `<<`, `count()`, `avg()`, `select()`, and the metrics queries `rate() by`, `quantile_over_time(duration, .5, .99) by`, `histogram_over_time`, `count_over_time`, `compare({ status = error })`. Corrections: the `!>>` meaning (per the docs: spans matching the right side that are not descendants of the left side; a frontend `!>>` cache query returned nothing), `<<` returns the right-hand spans, dotted `instrumentation.`/`link.` forms are attribute lookups. Docs read: Tempo traceql/construct-traceql-queries (structural operator definitions), metrics-from-traces/metrics-queries/configure-traceql-metrics (24h default, `query_backend_after` 15m). The Grafana UI sentence is gated as marked.
