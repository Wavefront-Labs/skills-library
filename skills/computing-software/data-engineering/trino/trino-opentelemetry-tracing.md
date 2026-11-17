---
id: computing-software.data-engineering.trino.trino-opentelemetry-tracing
name: trino-opentelemetry-tracing
category: computing-software
field: data-engineering
product: trino
tags: [opentelemetry, tracing, otel-exporter-endpoint, sampling-ratio, jaeger]
level: practitioner
status: docs-checked
description: "Export Trino distributed traces via OpenTelemetry, with endpoint, protocol and sampling ratio properties and a Jaeger demo."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/opentelemetry.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino opentelemetry tracing

Trino emits traces from the coordinator and workers, covering the planner, optimizer, many connectors and plugins. It uses trace identifiers supplied by client tools, or creates one per query, and propagates them to data sources and metastores so you can follow a query end to end. Those systems only contribute spans if they support OpenTelemetry and have tracing enabled separately.

Tracing is off by default. Enable it in `config.properties`:

```properties
tracing.enabled=true
otel.exporter.endpoint=http://observe.example.com:4317
```

The endpoint must be reachable from the coordinator and all workers.
- `otel.exporter.protocol`: `grpc` by default; `http/protobuf` for protobuf over HTTP.
- `otel.tracing.sampling-ratio`: between `0` and `1`, default `1`. Use `0.1` to export 10% on high-traffic clusters. The sampler is parent-based, with trace-ID-ratio sampling for root spans, so child spans inherit the parent's decision.

Demo: create a Docker network `platform`, run `jaegertracing/all-in-one:latest` with `COLLECTOR_OTLP_ENABLED=true` and ports 16686 and 4317, and run the Trino image with a mounted `config.properties` that includes:

```properties
node-scheduler.include-coordinator=true
http-server.http.port=8080
discovery.uri=http://localhost:8080
tracing.enabled=true
otel.exporter.endpoint=http://jaeger:4317
```

Run a query such as `SHOW CATALOGS;`, open the Jaeger UI at port 16686, select service `trino` and press Find traces.

## Checked

2026-11-09. Pages read in full against this skill:
- https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/opentelemetry.md

Confirmed (page read as raw markdown): tracing off by default, endpoint and protocol properties, sampling ratio range, default and parent-based sampler, and the Jaeger demo settings.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
