---
id: computing-software.cloud-infrastructure-engineering.observability.java-manual-instrumentation-and-withspan
name: java-manual-instrumentation-and-withspan
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [opentelemetry, java-manual-instrumentation, withspan-annotation, java-agent, spanattribute]
level: practitioner
status: docs-checked
description: "Add custom spans to an agent-instrumented Java app: @WithSpan and @SpanAttribute parameters, exclude and include settings, GlobalOpenTelemetry tracer and meter, context wrapping."
sources: ["https://opentelemetry.io/docs/zero-code/java/agent/annotations/", "https://opentelemetry.io/docs/languages/java/api/", "https://opentelemetry.io/docs/zero-code/java/agent/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Java manual instrumentation and @WithSpan

**Goal:** add spans, attributes and metrics for your own code to a Java app that already runs the OpenTelemetry
Java agent, with minimal code change. For most users the out-of-the-box instrumentation is sufficient.

## @WithSpan (annotations page)
Add the `opentelemetry-instrumentation-annotations` library (group `io.opentelemetry.instrumentation`), then
annotate the method.
```java
@WithSpan(kind = SpanKind.CLIENT, inheritContext = false, value = "my span name")
public void myMethod() { }
```
- Each call creates a span with the method's duration and any thrown exceptions.
- Default span name is `<className>.<methodName>` unless `value` is set.
- Parameters: `value` (String, default empty), `kind` (SpanKind, default INTERNAL), `inheritContext` (boolean,
  default true, since 2.14.0; false creates a new context instead of parenting the span in the current one).
- If the method returns a future- or promise-like type (CompletableFuture, CompletionStage, Guava
  ListenableFuture, reactive-streams Publisher, Reactor Mono and Flux, RxJava Completable, Maybe, Single,
  Observable, Flowable, ParallelFlowable), the span does not end until the future completes.

## @SpanAttribute
Annotate method parameters to record their values as attributes on the span, for example
`@SpanAttribute("parameter1") String parameter1`. Without an explicit name, the attribute name derives from the
formal parameter name only if parameter names are compiled into the class files (javac `-parameters`).

## Suppress or add without code changes
- `otel.instrumentation.opentelemetry-instrumentation-annotations.exclude-methods` suppresses `@WithSpan` on
  chosen methods. Format: `my.package.MyClass1[method1,method2];my.package.MyClass2[method3]`.
- `otel.instrumentation.methods.include` adds spans for chosen methods when you cannot modify the code, same format.
  All overloads of an included method are instrumented.

## Using the API with the agent
Add `opentelemetry-api` (group `io.opentelemetry`). The agent sets `GlobalOpenTelemetry`, so call
`GlobalOpenTelemetry.getOrNoop()` for the instance, or `GlobalOpenTelemetry.getTracer("application")` and
`GlobalOpenTelemetry.getMeter("application")`. Use the tracer and meter as described in the Java API page. The
agent page recommends `@WithSpan` over manual spans for the common cases.

## Spans and context (Java API page)
- `spanBuilder("name").startSpan()` creates a span; `span.makeCurrent()` returns a Scope (AutoCloseable) that
  sets the current context until closed; end the span with `span.end()`.
- `span.recordException(...)` records an exception; `span.setStatus(StatusCode.OK, "description")` sets status.
- Spans take the parent from `Context.current()` unless you call `setParent` explicitly.
- For handing work to other threads, `context.wrap(...)` wraps a Runnable, Callable or ExecutorService (and
  ScheduledExecutorService) so the context is made current before it runs.

## Verify
- [ ] The trace shows the annotated method's span with its `@SpanAttribute` attributes.
- [ ] Methods that you excluded no longer produce spans.

## Checked
2026-11-09. Confirmed against the markdown sources of the opentelemetry.io Java agent Annotations and
Extend-with-the-API pages (read in full) and the Java API page (searched for context, span and wrap sections; not
read end to end). Removed unconfirmed claims: BOM advice, the Spring Boot starter remark, automatic recording of
exceptions as Error status, agent context propagation across executors, `Context.taskWrapping`, the metrics
counter example, the "second SDK pipeline" gotcha and annotation behaviour on private methods.
Method: docs-checked 2026-11-09 against the opentelemetry.io docs source files for those three pages (raw.githubusercontent.com); documentation only, no commands run.
