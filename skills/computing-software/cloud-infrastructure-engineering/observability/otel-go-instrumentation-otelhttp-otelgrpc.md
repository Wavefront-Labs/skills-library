---
id: computing-software.cloud-infrastructure-engineering.observability.otel-go-instrumentation-otelhttp-otelgrpc
name: otel-go-instrumentation-otelhttp-otelgrpc
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [go-otel-setup, otelhttp, otelgrpc, language-instrumentation, go]
level: practitioner
status: docs-checked
description: "Instrument Go services with OpenTelemetry: TracerProvider and MeterProvider setup, otelhttp handlers and transports, otelgrpc stats handlers and shutdown."
sources: ["https://opentelemetry.io/docs/languages/go/getting-started/", "https://pkg.go.dev/go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp", "https://pkg.go.dev/go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Go instrumentation (otelhttp, otelgrpc)

Wire the SDK once at start-up, then wrap libraries with the contrib instrumentation packages.

## SDK setup
Follow the Go getting-started guide: create a TracerProvider (`trace.NewTracerProvider`) and a MeterProvider
(`metric.NewMeterProvider`), register them with `otel.SetTracerProvider` and `otel.SetMeterProvider`, and set a
propagator with `otel.SetTextMapPropagator` built from `propagation.TraceContext{}` and `propagation.Baggage{}`.
Collect each provider's `Shutdown` into a shutdown function and call it before the process exits, so the last batch
is flushed.

## HTTP
```go
srv := &http.Server{Handler: otelhttp.NewHandler(mux, "server",
    otelhttp.WithFilter(func(r *http.Request) bool { return r.URL.Path != "/healthz" }))}
client := &http.Client{Transport: otelhttp.NewTransport(http.DefaultTransport)}
```
- `otelhttp.NewHandler` wraps a server handler; `NewTransport` wraps an `http.RoundTripper`, starts a span and injects
  the span context into outbound headers.
- `WithFilter`: if any filter excludes a request it is not traced; keep filters simple and fast.
- `WithSpanNameFormatter` sets the span name. With `http.ServeMux` (or any middleware that sets `Pattern` on the
  request) the formatter runs twice: once at span creation and again after the middleware, so the pattern is usable.

## gRPC
```go
s := grpc.NewServer(grpc.StatsHandler(otelgrpc.NewServerHandler()))
conn, _ := grpc.NewClient(addr, grpc.WithStatsHandler(otelgrpc.NewClientHandler()), grpc.WithTransportCredentials(creds))
```
The interceptor API in otelgrpc is marked deprecated ("Use stats handlers instead"); use the stats handlers.

## Gotchas
- Context must flow: use `r.Context()` and pass `ctx` into every call; `context.Background()` breaks the trace.
- Keep `go.opentelemetry.io/otel` and contrib module versions aligned.

## Checked
2026-11-01. Confirmed on the Go getting-started page, otelhttp and otelgrpc package docs: NewHandler, NewTransport,
WithFilter, WithSpanNameFormatter behaviour with Pattern, NewServerHandler and NewClientHandler, interceptor
deprecation, provider and propagator setup calls, Shutdown. Removed (no fetched page states them): autoexport
usage, resource options, WithRouteTag and `http.route` from `r.Pattern` claims, otelsql, redisotel, otelaws and
runtime-instrumentation lines, the claim that Go has no agent.
Method: documentation only; no commands were run.
