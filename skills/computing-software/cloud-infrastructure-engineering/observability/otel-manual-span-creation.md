---
id: computing-software.cloud-infrastructure-engineering.observability.otel-manual-span-creation
name: otel-manual-span-creation
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [manual-span-creation, start-as-current-span, otel-traces, manual-instrumentation, tracer-provider, opentelemetry]
level: practitioner
status: draft
description: "Create manual OpenTelemetry spans correctly in Python, Go, Java and Node: current-context nesting, ending spans, attributes at start, errors and async work."
sources: ["https://opentelemetry.io/docs/languages/python/instrumentation/", "https://opentelemetry.io/docs/languages/go/instrumentation/", "https://opentelemetry.io/docs/languages/java/api/", "https://opentelemetry.io/docs/languages/js/instrumentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Manual span creation

Add manual spans for meaningful units of work that auto-instrumentation cannot see (business steps, batches, CPU-heavy functions). Always nest under the current context and always end the span.

## Python
```python
tracer = trace.get_tracer("checkout")
with tracer.start_as_current_span("charge_card", attributes={"app.payment.provider": provider}) as span:
    try:
        charge()
    except Exception as e:
        span.record_exception(e)
        span.set_status(Status(StatusCode.ERROR, str(e)))
        raise
```
Decorator form: `@tracer.start_as_current_span("charge_card")`.

## Go (context must be passed explicitly)
```go
ctx, span := otel.Tracer("checkout").Start(ctx, "charge_card", trace.WithAttributes(attribute.String("app.payment.provider", p)))
defer span.End()
if err := charge(ctx); err != nil { span.RecordError(err); span.SetStatus(codes.Error, err.Error()) }
```

## Java
```java
Span span = tracer.spanBuilder("charge_card").setAttribute("app.payment.provider", p).startSpan();
try (Scope scope = span.makeCurrent()) { charge(); }
catch (Exception e) { span.recordException(e); span.setStatus(StatusCode.ERROR); throw e; }
finally { span.end(); }
```
With the Java agent, `@WithSpan` on methods is simpler.

## Node
```js
tracer.startActiveSpan('charge_card', { attributes: { 'app.payment.provider': p } }, async (span) => {
  try { await charge(); } catch (e) { span.recordException(e); span.setStatus({ code: SpanStatusCode.ERROR }); throw e; }
  finally { span.end(); }
});
```

## Rules
- Set attributes needed by samplers at span start (samplers only see start-time attributes).
- Low-cardinality span names; ids as attributes.
- Spans for work started in background tasks must carry the parent context into the task (or use links if it outlives the request).

## Gotchas
- Forgetting `end()` leaks spans; they are never exported.
- Go: using `context.Background()` instead of the incoming `ctx` creates a new root trace.

## Verify
- [ ] In the trace view the manual span appears under the auto-instrumented server span with correct duration.
