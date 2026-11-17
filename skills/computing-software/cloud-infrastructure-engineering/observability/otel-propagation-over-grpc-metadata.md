---
id: computing-software.cloud-infrastructure-engineering.observability.otel-propagation-over-grpc-metadata
name: otel-propagation-over-grpc-metadata
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [opentelemetry, grpc-metadata-propagation, context-propagation, grpc, traceparent, baggage]
level: advanced
status: docs-checked
description: "Propagate trace context and baggage over gRPC metadata with OpenTelemetry instrumentation or manual inject/extract, including streaming RPCs and proxies."
sources: ["https://opentelemetry.io/docs/concepts/context-propagation/", "https://pkg.go.dev/go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc", "https://opentelemetry.io/docs/specs/otel/context/api-propagators/", "https://grpc.io/docs/guides/metadata/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Context propagation over gRPC metadata

**Goal:** unbroken traces across gRPC services in any language.

## How it works
gRPC metadata is HTTP/2 headers, so the W3C propagator writes `traceparent`, `tracestate` and `baggage` keys (lowercase) into outgoing metadata and reads them on the server.

## Use instrumentation (preferred)
Go:
```go
conn, _ := grpc.NewClient(addr, grpc.WithStatsHandler(otelgrpc.NewClientHandler()))
srv := grpc.NewServer(grpc.StatsHandler(otelgrpc.NewServerHandler()))
```
(The otelgrpc package documents stats handlers as the way to instrument clients and servers.) Java agent, Python `opentelemetry-instrumentation-grpc` (`GrpcInstrumentorClient().instrument()`, `GrpcInstrumentorServer().instrument()`), .NET `AddGrpcClientInstrumentation()` and ASP.NET Core server instrumentation, Node `@opentelemetry/instrumentation-grpc` handle it automatically.

## Manual inject/extract (custom transports or missing instrumentation)
Go client:
```go
md := metadata.MD{}
otel.GetTextMapPropagator().Inject(ctx, metadataCarrier(md))   // carrier implementing Get/Set/Keys over metadata.MD
ctx = metadata.NewOutgoingContext(ctx, md)
```
Python server:
```python
from opentelemetry.propagate import extract
def Handle(self, request, context):
    carrier = {k: v for k, v in context.invocation_metadata()}
    ctx = extract(carrier)
    with tracer.start_as_current_span("Handle", context=ctx, kind=SpanKind.SERVER): ...
```

## Gotchas
- Global propagator must be set (`otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(propagation.TraceContext{}, propagation.Baggage{}))` in Go); otherwise inject is a no-op.
- Proxies and meshes must forward the trace headers, and every hop must use the same propagators.
- gRPC header names use only `0-9 a-z _ - .`; binary metadata keys end with `-bin` and carry base64 values (gRPC HTTP/2 protocol).
- `traceparent` is the W3C header name; `tracestate` and `baggage` are the companion headers (Go propagators).
- Baggage travels to every downstream service, including third parties: never put secrets in it.

## Verify
- [ ] Client and server spans share a trace ID with server parent = client span; `rpc.system.name=grpc` (the current semantic convention attribute; older instrumentation emits `rpc.system`) is present.

## Checked

2026-10-24. opentelemetry-go-contrib otelgrpc (doc.go, stats_handler.go, metadata_supplier.go), opentelemetry-python-contrib grpc instrumentation classes, opentelemetry-js experimental packages and opentelemetry-dotnet repository listings, gRPC HTTP/2 protocol document, OpenTelemetry semantic conventions rpc/grpc.md (main branch). Confirmed: Go stats handler constructors, metadata carrier with Get/Set/Keys, `traceparent`/`tracestate`/`baggage` header names, Python `GrpcInstrumentorClient`/`GrpcInstrumentorServer`, the Node `instrumentation-grpc` package, the .NET GrpcNetClient package, metadata key character set and `-bin` suffix, and `rpc.system.name`. Removed unconfirmed claims about Envoy defaults and streaming span structure.

Method: documentation only; no commands were run.
