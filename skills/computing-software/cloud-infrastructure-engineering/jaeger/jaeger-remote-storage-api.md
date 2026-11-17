---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-remote-storage-api
name: jaeger-remote-storage-api
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, remote-storage, grpc-storage, trace-reader, trace-service]
level: advanced
status: docs-checked
description: "Plug a custom storage backend into Jaeger by implementing the gRPC Remote Storage API and using the grpc storage type."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/apis/
  - https://www.jaegertracing.io/docs/2.22/storage/
  - https://www.jaegertracing.io/docs/2.22/features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use a database Jaeger does not support directly.

Jaeger supports a gRPC-based Remote Storage API v2 (Status: Stable). Deploy a gRPC server implementing:
- `TraceReader`: lets Jaeger read traces from the storage backend.
- `DependencyReader`: loads service dependency graphs.
- `TraceService`: lets trace data be pushed to storage; it can run on a separate port.

Then use `grpc` as the storage type in Jaeger and give the remote gRPC server address. The reference code is jaeger/internal/storage/v2/grpc, and the repository holds an example configuration.

The storage page lists one known remote backend: PostgreSQL by robbert229. The features page also says certified-compliant databases such as ClickHouse can be reached via the Remote Storage API, although the 2.22 storage page treats ClickHouse as an experimental built-in backend behind a feature gate.

The `jaeger-remote-storage` component is a ready-made server for this API that proxies into a regular Jaeger backend; see the tools skill.

## Checked

Method: docs-checked 2026-11-09 against the Jaeger 2.22 APIs, storage and features pages (read in full).
