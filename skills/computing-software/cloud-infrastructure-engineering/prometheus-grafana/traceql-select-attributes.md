---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.traceql-select-attributes
name: traceql-select-attributes
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [traceql-select, traceql, tempo, trace-search-grafana]
level: practitioner
status: gated
description: "Return extra span and resource attributes in TraceQL search results with select(), to inspect values across matching spans without opening each trace."
sources: ["https://grafana.com/docs/tempo/latest/traceql/construct-traceql-queries/#selecting-attributes", "https://grafana.com/docs/tempo/latest/traceql/", "https://grafana.com/docs/grafana/latest/datasources/tempo/query-editor/traceql-editor/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TraceQL select()

Search results normally show span name, service and duration. `select()` adds attributes to each returned span.

```traceql
{ resource.service.name = "checkout" && status = error } | select(span.http.route, span.http.response.status_code, resource.service.version)
{ span.db.system = "postgresql" && duration > 500ms } | select(span.db.query.text, span.db.operation.name)
```
- Selected attributes come back in each matching span's `attributes` in the search response (tested: `status`, `service.name` and the selected ones). Grafana shows them as columns in its trace table (gated: unconfirmed, source is paywalled or blocked): Grafana was not driven here.
- `select()` ran both after the filter and before or after an aggregate (`| select(name) | count() > 0` and `| count() > 50 | select(name)` both worked), so order is flexible.

## Uses
- See which versions produce errors: select `resource.service.version` on error spans.
- Audit attribute values (route templates vs raw paths) without opening traces.
- Collect slow query texts.

## Performance
Select only what you need, and keep the filter selective (time range, service); the Tempo tuning page recommends scoped attributes over unscoped ones.

## Gotchas
- Attribute scope matters: `span.` vs `resource.`; an unscoped `.http.route` searches both but costs more.
- Results are limited by the search limit (`default_result_limit` 20 traces) and spans per span set (`default_spans_per_span_set` 3, `max_spans_per_span_set` 100 in Tempo 3.1.1); raise `limit` and `spss` in the request (or Grafana's query options) for broader samples.

## Verify
- [ ] The search response (or Grafana's trace table) shows the selected attributes for matching spans.

## Checked
Ran Tempo 3.1.1 (windows-amd64, single binary, local backend, OTLP/HTTP receiver) and pushed 12 synthetic traces through `/v1/traces` (frontend root span, payments child with an `exception` event on 4 error traces, checkout database spans, instrumentation scope names, int and string attributes), then queried `/api/search`, `/api/metrics/query_range` and `tempo-cli` 3.1.1. Ran both example queries from the page (an absent `span.db.query.text` simply returns no value), `select()` with scoped attributes, and read the returned span `attributes`; the limits come from `/status/config` on the running node. Docs read: Tempo traceql/tune-traceql-queries (scoped attributes). The Grafana table claim is gated as marked.
