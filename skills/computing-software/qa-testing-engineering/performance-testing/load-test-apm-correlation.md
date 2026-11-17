---
id: computing-software.qa-testing-engineering.performance-testing.load-test-apm-correlation
name: load-test-apm-correlation
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [load-test-correlation, apm-correlation, test-run-id, trace-tagging, observability]
level: practitioner
status: verified
description: "Correlate load-test traffic with APM traces, logs and metrics via run-id headers and baggage, dashboard annotations and slow-trace lookup for failing steps."
sources:
  - https://www.w3.org/TR/trace-context/
  - https://opentelemetry.io/docs/concepts/signals/baggage/
  - https://grafana.com/docs/k6/latest/javascript-api/jslib/http-instrumentation-tempo/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Correlating load tests with APM traces

**Goal:** from a slow endpoint in the k6/JMeter report, jump to the backend traces and logs of exactly those requests.

## Tag every request
- Header with run id: `X-Load-Test-Run: checkout-2024-06-01-1` and test step name.
- W3C Trace Context: generators can send `traceparent` so traces start at the load generator; APM links child spans.
- OpenTelemetry baggage: `baggage: loadtest.run=checkout-1,loadtest.step=pay` propagates through services that forward baggage.

k6 (Tempo instrumentation jslib):
```js
import http from 'k6/http';
import tempo from 'https://jslib.k6.io/http-instrumentation-tempo/1.0.1/index.js';
tempo.instrumentHTTP({ propagator: 'w3c' });   // adds traceparent to every request
// plus your own header
http.get(url, { headers: { 'X-Load-Test-Run': __ENV.RUN_ID }, tags: { name: 'GET /orders' } });
```
A request to a header-echo server received `traceparent: 00-<trace id>-<span id>-01`, `x-load-test-run: run-1` and the `baggage` header exactly as set (k6 v1.4.0, tempo jslib 1.0.1). JMeter: HTTP Header Manager with `${__P(runId)}`; Locust: `self.client.headers.update(...)` (requests session headers).

## Backend side
- Log the run id header (MDC/log context) and add it as a span attribute: the OpenTelemetry Collector `attributes` processor can read a value with `from_context` (keys prefixed `metadata.` look in gRPC metadata or HTTP headers, and the receiver needs `include_metadata: true`), or use app middleware. Baggage is not the same as attributes in OpenTelemetry, so copy the baggage values you want to filter on onto spans explicitly.
- Exclude test traffic from business analytics using the same header.

## Dashboards
- Annotate Grafana with test start/stop (`POST /api/annotations`) from the pipeline.
- Filter APM by `loadtest.run` to see service maps, slowest spans, DB queries only for this run.

## Workflow when a step breaches its threshold
1. Note endpoint and time window from the load report.
2. Query traces: run id + endpoint + duration > p95.
3. Inspect span breakdown (DB, downstream calls, lock waits), then logs for those trace ids.

## Gotchas
- Sampling: head sampling decides before the trace is complete (the OpenTelemetry docs example is 5% of all traces), so it can miss the slow ones; use tail sampling in the Collector, whose `latency` policy samples traces longer than `threshold_ms` and whose `string_attribute` policy can keep traces whose attribute (for example the run id copied onto the span) matches.
- High-cardinality attributes (per-iteration ids) as metric labels explode metrics storage; keep them on traces/logs only.

## Verify
Pick one failed request from the generator log (by timestamp and run id) and find its trace within a minute.

## Checked
k6 v1.4.0 on Windows with a local header-echo HTTP server; fetched docs.
- Run: the `instrumentHTTP({ propagator: 'w3c' })` script loaded the jslib 1.0.1 module from jslib.k6.io and the echo server saw a `traceparent` header (version 00, 32-hex trace id, 16-hex span id, flags 01) plus the custom `X-Load-Test-Run` header and the `baggage` header.
- Fetched: k6 Tempo instrumentation page (import path and version 1.0.1, w3c propagator), W3C Trace Context page (traceparent), OpenTelemetry baggage page (baggage is not attributes), Collector attributes processor README (`from_context`, `metadata.` prefix, `include_metadata`), tail sampling processor README (latency and string_attribute policies), OpenTelemetry sampling page (head vs tail), Grafana annotations HTTP API page (`POST /api/annotations`).
- Grafana annotation and Collector behaviour is as stated on those fetched pages.
