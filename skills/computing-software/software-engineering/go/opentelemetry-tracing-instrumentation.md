---
id: computing-software.software-engineering.go.opentelemetry-tracing-instrumentation
name: opentelemetry-tracing-instrumentation
category: computing-software
field: software-engineering
product: go
tags: [go, go-logging-observability, go-opentelemetry, opentelemetry, otel, tracing]
level: practitioner
status: draft
description: "Instrument Go services with the OpenTelemetry SDK: tracer provider, OTLP exporter, spans, otelhttp and context propagation."
sources:
  - https://opentelemetry.io/docs/languages/go/
  - https://pkg.go.dev/go.opentelemetry.io/otel
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# OpenTelemetry tracing in Go

**Goal:** distributed traces with correct parent/child links across HTTP calls.

```go
exp, _ := otlptracehttp.New(ctx)                       // endpoint from OTEL_EXPORTER_OTLP_ENDPOINT
tp := sdktrace.NewTracerProvider(
    sdktrace.WithBatcher(exp),
    sdktrace.WithResource(resource.NewWithAttributes(semconv.SchemaURL,
        semconv.ServiceName("checkout"))),
    sdktrace.WithSampler(sdktrace.ParentBased(sdktrace.TraceIDRatioBased(0.1))),
)
otel.SetTracerProvider(tp)
otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
    propagation.TraceContext{}, propagation.Baggage{}))
defer tp.Shutdown(ctx)                                  // flush spans on exit

h := otelhttp.NewHandler(mux, "http.server")            // incoming
c := http.Client{Transport: otelhttp.NewTransport(http.DefaultTransport)} // outgoing

ctx, span := otel.Tracer("checkout").Start(ctx, "charge-card")
defer span.End()
span.SetAttributes(attribute.String("payment.provider", "x"))
if err != nil { span.RecordError(err); span.SetStatus(codes.Error, "charge failed") }
```

Always pass the returned `ctx` downwards; that is how children link to parents. Configure by environment (`OTEL_SERVICE_NAME`, `OTEL_TRACES_SAMPLER`, `OTEL_EXPORTER_OTLP_ENDPOINT`). Semantic-convention names change between versions, so pin module versions together.

## Gotchas
- Missing `tp.Shutdown` loses the last batch.
- High-cardinality attributes (user IDs in span names) explode storage; keep names low-cardinality.
- Mixing instrumentation package versions with different semconv produces duplicated attributes.

## Verify
Run a local collector or Jaeger, send one request through two services and confirm a single trace with a parent/child chain.
