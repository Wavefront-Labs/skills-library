---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.tempo-traceql-queries
name: tempo-traceql-queries
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana, tempo, traceql, trace-search, span-attributes, resource-attributes, intrinsics, duration, status, span-kind, structural-operators, descendant, child, sibling, aggregates, count, avg, traceql-metrics, rate, quantile-over-time, select, by, exemplars, trace-id-lookup, tempo-cli, search-api]
level: practitioner
status: gated
description: "Query traces with TraceQL: span/resource attribute filters, intrinsics, structural operators (>>, >, ~), aggregates, TraceQL metrics (rate, quantile_over_time by), and keeping searches fast."
sources: ["https://grafana.com/docs/tempo/latest/traceql/", "https://grafana.com/docs/tempo/latest/traceql/construct-traceql-queries/", "https://grafana.com/docs/tempo/latest/traceql/metrics-queries/", "https://grafana.com/docs/tempo/latest/api_docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TraceQL queries

**Goal:** find the traces that explain a symptom (slow checkout, 500s from one pod, a
retry storm) with one query, and turn span data into time series when no metric exists.

## 1. Grammar in one glance
```
{ <spanset filter> } [ <structural op> { <spanset filter> } ] [ | <aggregate/pipeline> ]
```
- A **spanset** is the set of spans in a trace matching the braces; a trace matches when
  the whole expression matches. Results are traces, highlighting matching spans.
- Attribute scopes: `span.http.status_code`, `resource.service.name`, `event.exception.message`,
  `link:` intrinsics (`link:traceID`), `instrumentation:name` (colon forms; `instrumentation.name` matched nothing); unscoped `.http.method` checks span then resource (slower).
- **Intrinsics**: `duration`, `name`, `status` (`ok`, `error`, `unset`), `statusMessage`,
  `kind` (`server`, `client`, `producer`, `consumer`, `internal`), `traceDuration`,
  `rootName`, `rootServiceName`, `nestedSetParent`, `span:id`, `trace:id`, `event:name`.
- Operators: `= != > >= < <= =~ !~`, `&&`, `||`; durations `100ms`, `2s`; strings quoted;
  `nil` for missing attribute; regex `=~` is RE2 and **fully anchored** (`name =~ "HTTP"` matched nothing, `"HTTP.*"` matched). `#` comments are not TraceQL: strip the annotations below before running.

## 2. Everyday queries
```traceql
{ resource.service.name = "checkout" && span.http.status_code >= 500 }
{ resource.service.name = "checkout" && duration > 2s && kind = server }
{ status = error && resource.k8s.pod.name =~ "api-.*" }
{ name = "SELECT orders" && span.db.system = "postgresql" && duration > 500ms }
{ span.http.route = "/api/v2/cart" } && { span.messaging.system = "kafka" }     # both present in the trace
{ resource.service.name = "frontend" } >> { resource.service.name = "payments" && status = error }   # descendant
{ name = "HTTP GET" } > { name = "cache.get" }                                   # direct child
{ status = error } ~ { status = error }                                          # sibling errors
{ rootServiceName = "frontend" && traceDuration > 3s }
{ event.exception.type = "TimeoutException" }
{ span.http.status_code = 200 && span.http.response_content_length > 1e6 }
{ resource.service.name = "api" && span.user.id = nil }                         # attribute missing
```
Structural ops (each returns the spans matching the right-hand side): `{A} >> {B}` B is a descendant of A, `{A} > {B}` B is a direct child, `{A} ~ {B}` B has a sibling matching A, `!>>`/`!>` B is NOT a descendant/child of A, `<<`/`<` B is an ancestor/parent of an A span; `&&`/`||` between spansets = same trace.

## 3. Aggregates and selection
```traceql
{ resource.service.name = "api" } | count() > 50                 # traces with > 50 api spans (fan-out)
{ span.db.system = "postgresql" } | avg(duration) > 100ms
{ name = "retry" } | count() >= 3                                 # retry storms
{ resource.service.name = "api" } | max(span.http.request_content_length) > 5e6
{ status = error } | select(span.http.route, resource.k8s.pod.name)    # return extra attributes in results table
```
Aggregates: `count`, `avg`, `min`, `max`, `sum` over the spanset per trace.

## 4. TraceQL metrics (no metrics-generator configuration was needed on Tempo 3.1.1; for 2.x confirm the `local-blocks` requirement in that release's docs)
```traceql
{ resource.service.name = "api" && kind = server } | rate()
{ resource.service.name = "api" && status = error } | rate() by (span.http.route)
{ resource.service.name = "api" && kind = server } | quantile_over_time(duration, 0.99, 0.5) by (span.http.route)
{ span.db.system = "postgresql" } | histogram_over_time(duration)
{ resource.service.name = "api" } | count_over_time() by (resource.k8s.pod.name)
{ name = "checkout" } | avg_over_time(span.cart.items)
{ resource.service.name = "api" } | compare({ status = error })          # attribute distribution: errors vs baseline
```
Use in Grafana as *Metrics query* type in the Tempo data source; exemplars link each point
to traces (gated: unconfirmed, source is paywalled or blocked): Grafana was not driven here (the API returns `exemplars` with trace ids). Range limit: `query_frontend.metrics.max_duration` (default 24h in Tempo 3.1.1).

## 5. API and CLI
```bash
curl -G 'http://tempo:3200/api/search' --data-urlencode 'q={ status = error && resource.service.name = "api" }' \
  --data-urlencode 'start=1760518800' --data-urlencode 'end=1760522400' --data-urlencode 'limit=20' --data-urlencode 'spss=3'
curl 'http://tempo:3200/api/traces/4bf92f3577b34da6a3ce929d0e0e4736' -H 'Accept: application/json'   # or /api/v2/traces
curl -G 'http://tempo:3200/api/v2/search/tag/span.http.route/values' --data-urlencode 'q={ resource.service.name = "api" }'   # v2 takes the scoped name; the v1 path returned an empty list
curl -G 'http://tempo:3200/api/metrics/query_range' --data-urlencode 'q={ kind = server } | rate() by (resource.service.name)' --data-urlencode 'step=60s'
tempo-cli query api search tempo:3200 '{ status = error }' now-1h now   # host:port without a scheme; time as now-1h or RFC3339; tempo-cli ships in the release tarball
```

## 6. Keep searches fast
- Always include a **time range as narrow as possible** and `resource.service.name`;
  Tempo prunes blocks by time and uses the Parquet column for service name.
- Scoped attributes (`span.`/`resource.`) avoid double column scans; intrinsics are cheapest.
- Avoid regex on high-cardinality attributes across days; filter by service/status first.
- Grafana's *Search* builder maps to the same TraceQL; the TraceQL editor shows the query it generates.
- Watch `tempo_query_frontend_queries_within_slo_total` (labels `op`, `result`, `tenant`; there is no `_per_tenant` series in 3.1.1); recurring slow queries →
  shard more (`query_frontend.search.concurrent_jobs`, `target_bytes_per_job`) or shorten retention of hot tenants.

## Gotchas
- Attribute names are exact and case-sensitive, and OTel semconv renames (`http.status_code`
  → `http.response.status_code`) mean old and new spans need `||` during migrations.
- Numbers vs strings: `span.http.status_code = "500"` matches nothing if instrumented as int.
- `status = error` is the span status, not HTTP 5xx; many instrumentations set both, some only the code.
- `duration` is per span; for whole-trace latency use `traceDuration`.
- Results are capped by `limit` (default 20) and `spss` (spans per spanset, default 3); dashboards
  listing "all errors" are not what traces are for—use the metrics-generator metrics.

## Verify
- [ ] A query with `resource.service.name` + `status = error` over 1 h returns in < 3 s with matching spans highlighted.
- [ ] `| rate() by (span.http.route)` plots lines that agree (within sampling) with `traces_spanmetrics_calls_total` (gated: unconfirmed, source is paywalled or blocked): the metrics-generator was not run.
- [ ] Clicking an exemplar from a metrics panel opens the exact trace (gated: unconfirmed, source is paywalled or blocked): Grafana was not driven.

## Checked
Ran Tempo 3.1.1 (windows-amd64, single binary, local backend, OTLP/HTTP receiver) and pushed 12 synthetic traces through `/v1/traces` (frontend root span, payments child with an `exception` event on 4 error traces, checkout database spans, instrumentation scope names, int and string attributes), then queried `/api/search`, `/api/metrics/query_range` and `tempo-cli` 3.1.1. Ran every TraceQL example (scopes, intrinsics incl. `nestedSetParent`, `&&` across spansets, `>>`, `>`, `~`, `<<`, `<`, `!<`, aggregates `count/avg/min/max/sum`, `select`, `= nil`) and each metrics function; `curl` calls for `/api/search`, `/api/traces/<id>` (JSON and `/api/v2/traces`), tag values (v1 returned an empty list, v2 returned `/cart`), `/api/metrics/query_range`; `tempo-cli query api search` with and without a scheme (a scheme breaks the URL, `1h` is not a valid time). Config values from `/status/config` (search `default_result_limit` 20, `default_spans_per_span_set` 3, metrics `max_duration` 24h) and the metric names from `/metrics`. Corrections: regex is anchored, `!>>` semantics, 24h default, `_total` metric name, `link`/`instrumentation` forms. Gated as marked: Grafana UI, exemplars, spanmetrics comparison.
