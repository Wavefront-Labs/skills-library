---
id: computing-software.cloud-infrastructure-engineering.observability.otel-rpc-and-grpc-semantic-conventions
name: otel-rpc-and-grpc-semantic-conventions
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [opentelemetry, rpc-semantic-conventions, grpc-semconv, semantic-conventions, rpc-metrics]
level: advanced
status: docs-checked
description: "Apply OpenTelemetry RPC and gRPC semantic conventions for span names, kinds, attributes, status mapping and rpc.server/client duration metrics."
sources: ["https://opentelemetry.io/docs/specs/semconv/rpc/rpc-spans/", "https://opentelemetry.io/docs/specs/semconv/rpc/grpc/", "https://opentelemetry.io/docs/specs/semconv/rpc/rpc-metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RPC and gRPC semantic conventions

**Goal:** RPC telemetry that dashboards, service graphs and vendors understand without custom mapping. The semconv RPC and gRPC pages state "Release Candidate, unless otherwise specified": confirm the status of each attribute on the page for your semconv version.

## Spans
- **Name**: `{rpc.method}` when available and not `_OTHER`, else `{rpc.system.name}`.
- **Kind**: `CLIENT` on the caller, `SERVER` on the callee.
- Attributes:
| Attribute | Example | Notes |
|---|---|---|
| `rpc.system.name` | `grpc`, `dubbo`, `connectrpc` | Required |
| `rpc.method` | `com.example.ExampleService/exampleMethod` | Fully-qualified logical method name; `_OTHER` when unknown |
| `rpc.method_original` | | Only if different from `rpc.method` |
| `rpc.response.status_code` | `OK`, `DEADLINE_EXCEEDED` | String form of the status code |
| `error.type` | `DEADLINE_EXCEEDED` | Required if the operation failed |
| `server.address`, `server.port` | `example.com`, `50051` | |
| `network.peer.address`, `network.peer.port` | IP | Recommended |
| `rpc.request.metadata.<key>` / `rpc.response.metadata.<key>` | | Opt-in; lowercase key |

Older instrumentation may emit different names (`rpc.system`, `rpc.service`, `rpc.grpc.status_code`). The RPC pages describe `OTEL_SEMCONV_STABILITY_OPT_IN` values `rpc` (emit the new conventions only) and `rpc/dup` (emit both) for a phased rollout. Check what your library emits and pin a version.

## Status mapping (gRPC)
The gRPC page lists `UNKNOWN`, `DEADLINE_EXCEEDED`, `UNIMPLEMENTED`, `INTERNAL`, `UNAVAILABLE` and `DATA_LOSS` as the status codes that classify a server span as an error. For client spans follow the gRPC page and the Recording Errors document.

## Metrics
- `rpc.server.call.duration` and `rpc.client.call.duration` histograms, unit `s`.
- Common dimensions: `rpc.system.name`, `rpc.method`, `rpc.response.status_code`, `server.address`.

## Verify
- [ ] Span names are `rpc.method` values; RED dashboard by `rpc.method` works; migrate dashboards that query the old names.

## Checked
- 2026-10-28. Checked against the OpenTelemetry semantic conventions RPC spans, gRPC and RPC metrics pages (semconv docs as served 2026-10; status Release Candidate) and the gRPC status codes doc.
- Confirmed: span name rule, `rpc.system.name` values, `rpc.method`, `rpc.method_original`, `rpc.response.status_code`, `error.type`, server/network attributes, request/response metadata attributes, server error code list, `rpc.server.call.duration` and `rpc.client.call.duration` (unit s), `OTEL_SEMCONV_STABILITY_OPT_IN` with `rpc` and `rpc/dup`.
- Fixed: the draft used the old attribute names (`rpc.system`, `rpc.service`, `rpc.grpc.status_code`) and metric names `rpc.server.duration`; replaced with the current ones. Removed (unconfirmed): message events, client any-non-OK rule, the unconfirmed example values and the claim that older names are "development".
Method: documentation only; no commands were run.
