---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-query-api-ports
name: jaeger-query-api-ports
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, api-v3, query-service-grpc, port-16685, internal-http-json]
level: practitioner
status: docs-checked
description: "Retrieve traces via jaeger.api_v3.QueryService on 16685 or the v3 HTTP JSON API on 16686 instead of the internal API."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/apis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick a supported read API.

Read ports:
- 16685 gRPC: `jaeger.api_v3.QueryService` (OTLP-based Protobuf) and the legacy `jaeger.api_v2.QueryService`
- 16686 HTTP: `/api/v3/*` (OTLP-based JSON over HTTP) and `/api/*` (internal, unofficial JSON)

The recommended way to retrieve traces programmatically is the gRPC `jaeger.api_v3.QueryService`, defined in api_v3/query_service.proto (default `:16685`). The JSON over HTTP version (Stable) mirrors it; an OpenAPI file exists.

The internal HTTP JSON API (Status: Internal) is what the UI uses, for example GET `https://jaeger-query:16686/api/traces/{trace-id-hex-string}`. It is intentionally undocumented and subject to change.

Dependencies graph (Internal): GET `/api/dependencies` with `endTs` (milliseconds since epoch, end of the interval) and `lookback` (milliseconds). It returns edges as tuples (caller, callee, count). For programmatic access, use gRPC/Protobuf.

gRPC introspection: servers enable reflection, but only the list command works properly:
`grpc_cli ls localhost:16685`
which prints services including `jaeger.api_v3.QueryService`, `jaeger.api_v2.QueryService` and `jaeger.api_v2.metrics.MetricsQueryService`.

## Checked

2026-11-03. Confirmed against the APIs page: read ports and endpoints, api_v3 as the recommended API, the internal and undocumented JSON API, /api/dependencies parameters and result, and the gRPC reflection list output. Removed: a closing summary paragraph that went beyond the page.
Method: documentation only; no commands were run.
