---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-query-extension-config
name: jaeger-query-extension-config
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, jaeger-query, query-extension, grpc-16685, http-16686]
level: practitioner
status: docs-checked
description: "Configure jaeger_query to serve the gRPC and HTTP APIs and UI, referencing named trace and metrics backends."
sources:
  - https://www.jaegertracing.io/docs/2.22/deployment/configuration/
  - https://www.jaegertracing.io/docs/2.22/architecture/
  - https://www.jaegertracing.io/docs/2.22/operations/tools/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run the query role with UI.

The `jaeger_query` extension runs the HTTP and gRPC servers that expose the trace query APIs and the UI:
```
jaeger_query:
  storage:
    traces: some_trace_storage
    metrics: some_metrics_storage
  base_path: /
  ui:
    config_file: /etc/jaeger/ui-config.json
    log_access: true
  grpc:
    endpoint: 0.0.0.0:16685
  http:
    endpoint: 0.0.0.0:16686
```
The `storage` section references backends by the names defined in the `jaeger_storage` extension. `ui.config_file` points to the UI configuration (see the UI skills). `config.go` in the repository is the authoritative property list.

A standalone query deployment that does not need an ingestion pipeline can use the no-op receiver and no-op exporter; the repository example is `config-query.yaml`.

With an external storage backend, both all-in-one and collector/query configurations are horizontally scalable; the collector/query split lets you separate read and write traffic, scale them independently and apply different access and security policies.

Failure mode: single-node backends such as memory or Badger cannot be shared between multiple processes, so they only work with all-in-one; for a split deployment the docs point to the jaeger-remote-storage component.

## Checked

2026-11-03. Confirmed against the Configuration page (jaeger_query example, storage references, config.go), the Architecture page (no-op receiver and exporter for query deployments, horizontal scaling and read/write separation of collector/query) and the Tools page (single-node backends cannot be shared between processes). Removed: the claim that query is stateless and the wording about Badger or memory storage unreachable from query, replaced by what the pages state.
Method: documentation only; no commands were run.
