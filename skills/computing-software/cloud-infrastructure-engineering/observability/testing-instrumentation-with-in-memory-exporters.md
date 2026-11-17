---
id: computing-software.cloud-infrastructure-engineering.observability.testing-instrumentation-with-in-memory-exporters
name: testing-instrumentation-with-in-memory-exporters
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [instrumentation-testing, in-memory-exporter, language-instrumentation, otel-sdk, unit-testing]
level: practitioner
status: draft
description: "Unit-test OpenTelemetry instrumentation with in-memory span, metric and log exporters in Java, Python, Go, Node and .NET: assert names, attributes, status and parentage."
sources: ["https://github.com/open-telemetry/opentelemetry-java/tree/main/sdk/testing", "https://pkg.go.dev/go.opentelemetry.io/otel/sdk/trace/tracetest", "https://opentelemetry-python.readthedocs.io/en/latest/sdk/trace.export.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing instrumentation with in-memory exporters

Instrumentation is code; test that spans/metrics have the names and attributes your dashboards and alerts depend on.

## Java (JUnit 5, `opentelemetry-sdk-testing`)
```java
@RegisterExtension static final OpenTelemetryExtension otel = OpenTelemetryExtension.create();
@Test void chargeCreatesSpan() {
  new Billing(otel.getOpenTelemetry()).charge("o-1");
  otel.assertTraces().hasTracesSatisfyingExactly(trace -> trace.hasSpansSatisfyingExactly(
      span -> span.hasName("charge").hasKind(SpanKind.INTERNAL)
                  .hasAttribute(AttributeKey.stringKey("acme.order.id"), "o-1")
                  .hasStatus(StatusData.unset())));
  assertThat(otel.getMetrics()).anySatisfy(m -> assertThat(m).hasName("acme.charges"));
}
```
Inject `OpenTelemetry` into the class under test instead of using `GlobalOpenTelemetry`.

## Python
```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
exp = InMemorySpanExporter(); tp = TracerProvider(); tp.add_span_processor(SimpleSpanProcessor(exp))
charge("o-1", tracer=tp.get_tracer("t"))
(span,) = exp.get_finished_spans()
assert span.name == "charge" and span.attributes["acme.order.id"] == "o-1"
```
Metrics: `InMemoryMetricReader()` -> `reader.get_metrics_data()`. The global provider can only be set once per
process - pass providers explicitly or use `opentelemetry.test.TestBase`.

## Go
```go
sr := tracetest.NewSpanRecorder()
tp := sdktrace.NewTracerProvider(sdktrace.WithSpanProcessor(sr))
charge(ctx, tp.Tracer("t"), "o-1")
spans := sr.Ended(); require.Len(t, spans, 1); require.Equal(t, "charge", spans[0].Name())
reader := sdkmetric.NewManualReader(); mp := sdkmetric.NewMeterProvider(sdkmetric.WithReader(reader))
var rm metricdata.ResourceMetrics; _ = reader.Collect(ctx, &rm)
// metricdatatest.AssertEqual(t, want, got, metricdatatest.IgnoreTimestamp())
```

## Node / .NET
Node: `InMemorySpanExporter` + `SimpleSpanProcessor` from `@opentelemetry/sdk-trace-base`; reset with `exporter.reset()`.
.NET: `services.AddOpenTelemetry().WithTracing(b => b.AddSource("Acme").AddInMemoryExporter(exportedActivities))`.

## What to assert
Span name (low cardinality), kind, parent/child relation (`span.parent.span_id`), status on failure, required
attributes, exceptions recorded, metric names/units/attribute keys. Use Simple (sync) processors in tests so spans
are available immediately.
