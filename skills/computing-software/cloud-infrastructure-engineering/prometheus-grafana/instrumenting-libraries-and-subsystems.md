---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.instrumenting-libraries-and-subsystems
name: instrumenting-libraries-and-subsystems
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [library-instrumentation, instrumenting-libraries, instrumentation, client-libraries, prometheus-best-practices]
level: advanced
status: docs-checked
description: "Add metrics to a shared library or subsystem: what to track, distinguishing uses with labels, Go registration handling, and OpenTelemetry API-only instrumentation guidance."
sources: ["https://prometheus.io/docs/practices/instrumentation/", "https://prometheus.io/docs/practices/naming/", "https://opentelemetry.io/docs/concepts/instrumentation/libraries/", "https://pkg.go.dev/github.com/prometheus/client_golang/prometheus"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instrumenting libraries and subsystems

## Prometheus guidance
From the Prometheus instrumentation page:
- Libraries should provide instrumentation with no additional configuration required by users.
- A library that accesses a resource outside the process (network, disk, IPC) should track at minimum the overall query count,
  errors (if possible) and latency. Heavier libraries can also track internal errors and latency and other useful statistics.
- A library may be used by independent parts of an application against different resources, so distinguish uses with labels
  where appropriate: a database connection pool should distinguish the databases it talks to, while a DNS client library need
  not distinguish its users.
- Do not overuse labels: every labelset is another time series with RAM, CPU, disk and network cost. The page suggests keeping
  metric cardinality below 10 for most metrics and investigating alternatives for anything over 100.
- No part of a metric name should be procedurally generated; use labels.
- Thread pools: queued requests, threads in use, total threads, tasks processed, how long they took, and time spent waiting
  in the queue. Caches: total queries, hits, overall latency, and the query count, errors and latency of the system the cache
  fronts.
- Counters for log lines and failures; report failures alongside an attempts metric so a failure ratio is easy to calculate.

Naming page: metric names should have a single-word application prefix relevant to the domain (client libraries call it the
namespace) and should use base units (seconds, bytes).

## Go client (client_golang)
- Collectors are registered with a `Registerer`; `MustRegister` on the package is a shortcut for `DefaultRegisterer.MustRegister`.
  A library can let callers pass their own `prometheus.Registerer`.
- `AlreadyRegisteredError` is returned by `Register` when the same, or a different collector collecting the same metrics, is
  already registered; it carries the `ExistingCollector` and `NewCollector`, so you can switch to the existing one.
- For several instances of the same metric in one process, the package example uses `ConstLabels` (for example
  `prometheus.Labels{"worker_id": "42"}`) so each instance is a distinct metric.

## OpenTelemetry libraries (from the OpenTelemetry libraries page, which is written mainly for traces)
- Libraries should use only the OpenTelemetry API, not the SDK: the API is abstractions and non-operational implementations, so
  unless the application imports the SDK the instrumentation does nothing and does not affect performance.
- Obtain the tracer with the library name and version. Libraries may accept a `TracerProvider` for dependency injection and
  testing or use the global one.
- Follow semantic conventions for span names and attributes; only instrument your library at its own level, and when in
  doubt do not instrument (for example a thin proxy over an already instrumented client).

## Verify
- [ ] Two instances of the library in one process do not fail registration.
- [ ] Every label value comes from a small bounded set.

## Checked
Checked 2026-11-07. Read in full: the Prometheus instrumentation practices page, and the OpenTelemetry "Libraries" page up to its
Java example (about the first 95 lines; the rest of the nested-spans and metrics-related sections was not read). Naming page: opening
rules only. Go client page (171k characters): the Registerer, MustRegister, AlreadyRegisteredError and ConstLabels example text found by search, not read in full.
Removed as not stated on these pages: the Go `Opts` constructor example, the `duplicate metrics collector registration attempted` error string, example
prefixes such as `grpc_client_` and `hikaricp_`, "provide a way to disable metrics", `go.opentelemetry.io/otel/metric` and the `otel.Meter(...)` call with `WithInstrumentationVersion`,
the optional `MeterProvider` option, and the `testutil` and `ManualReader` testing advice (the OTel page covers tracers, not meters).
Method: documentation only; no commands were run.
