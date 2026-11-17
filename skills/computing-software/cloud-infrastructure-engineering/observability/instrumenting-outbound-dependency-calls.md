---
id: computing-software.cloud-infrastructure-engineering.observability.instrumenting-outbound-dependency-calls
name: instrumenting-outbound-dependency-calls
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [outbound-call-instrumentation, dependency-call-metrics, instrumentation, client-spans, red-method, opentelemetry]
level: practitioner
status: docs-checked
description: "Instrument outbound calls (HTTP clients, DB) with client-side RED metrics using OTel semantic-convention names so dependency problems show from the caller."
sources: ["https://prometheus.io/docs/practices/instrumentation/#online-serving-systems", "https://opentelemetry.io/docs/specs/semconv/http/http-metrics/", "https://opentelemetry.io/docs/specs/semconv/database/database-metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instrumenting outbound dependency calls

The Prometheus instrumentation guide says online-serving systems should be monitored on both the client and server side. Differences between the two point at the network, pooling or queueing in between.

## What to record per dependency
- HTTP clients: `http.client.request.duration` (histogram) with `http.request.method`, `http.response.status_code` (when a response was received), `error.type` (when the request ended in an error) and `server.address` (required on the client metric).
- Databases: `db.client.operation.duration` (histogram, unit `s`) with `db.system.name`, `db.operation.name`, `db.collection.name` and `error.type`. Use the operation and collection names, not the full query text.
- Pool metrics from the database conventions: `db.client.connection.count`, `.limit`, `.idle.max`, `.idle.min`, `.pending_requests`, `.timeouts`, `.wait_time`, `.create_time`, `.use_time`.
- `error.type` takes values such as `timeout`, an exception class name, or the status code as a string, so timeouts do not need a separate metric.
- When you count failures, also keep a total-attempts metric so the failure ratio is easy to compute (Prometheus guide). Count retries as attempts.

## Implementation
- Prefer your language's OpenTelemetry instrumentation library over hand-written wrappers.
- If you write a wrapper, wrap the client once (transport or interceptor), never at each call site.
- Keep dependency labels bounded: `server.address` or a route template, never the full URL with variable path parts.

## Gotchas
- Client latency includes pool wait and name resolution; if server-side latency is flat but client p99 grows, check the pool wait time and pending requests.
- Measure each attempt and the overall call separately when retries exist, or retries hide in averages.
- A URL path as a label explodes cardinality.

## Verify
- [ ] Every dependency appears in a dashboard row with rate, errors, p99.
- [ ] Injected latency on a dependency is visible in client metrics within one scrape.

## Checked
Date: 2026-11-09. Confirmed in the Prometheus instrumentation practices page (client and server side monitoring, failures plus total attempts), the OpenTelemetry HTTP metrics convention (http.client.request.duration, attribute names, error.type behaviour, server.address required on client metrics) and the database metrics convention (db.client.operation.duration, attribute names, connection metric names). Removed: peer.service, a client_retries_total metric, specific library names (otelhttp and others), the Go snippet and the PromQL examples (Prometheus-translated metric names were not confirmed on the cited pages).
Method: docs-checked 2026-11-09 against the Prometheus instrumentation practices page and the OpenTelemetry HTTP and database metrics semantic-convention pages.
