---
id: computing-software.cloud-infrastructure-engineering.observability.request-scoped-log-context
name: request-scoped-log-context
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [mdc-logging, request-scoped-log-context, structured-logging, contextvars, log-correlation-config, logging]
level: practitioner
status: draft
description: "Attach request-scoped fields (trace_id, user tier, tenant) to every log line via MDC, contextvars or child loggers, including across threads and async tasks."
sources: ["https://logback.qos.ch/manual/mdc.html", "https://docs.python.org/3/library/contextvars.html", "https://www.structlog.org/en/stable/contextvars.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Request-scoped log context

Goal: every log line inside a request carries the same context fields without passing them through every function.

## Java (SLF4J MDC)
```java
try (MDC.MDCCloseable c = MDC.putCloseable("tenant", tenantId)) {
    log.info("charging card");   // JSON encoder emits "tenant" field
}
```
- MDC is thread-local: executors lose it. Wrap tasks: `MDC.getCopyOfContextMap()` captured at submit, `MDC.setContextMap()` in the task, or use the OTel Java agent which injects `trace_id`/`span_id` into MDC automatically (logback/log4j instrumentation).
- Reactor/WebFlux: use context propagation (`Hooks.enableAutomaticContextPropagation()` with micrometer context-propagation).

## Python (contextvars + structlog)
```python
import structlog
structlog.configure(processors=[structlog.contextvars.merge_contextvars, structlog.processors.JSONRenderer()])
structlog.contextvars.bind_contextvars(tenant=tenant_id, request_id=rid)   # in middleware
log = structlog.get_logger(); log.info("charging card")
structlog.contextvars.clear_contextvars()  # at request end
```
contextvars follow asyncio tasks automatically; thread pools need `contextvars.copy_context().run(fn)`.

## Go
Pass `context.Context`; use `slog` with a handler that reads values from ctx, or create a child logger per request: `l := logger.With("tenant", t)` stored in ctx.

## Node
`AsyncLocalStorage` with pino `mixin()` returning the store's fields.

## What to put in context
trace_id, span_id (from OTel), request route, tenant/customer tier, deployment version. Not secrets or full user objects.

## Gotchas
- Forgetting to clear context in pooled threads leaks one request's fields into the next.
- Duplicated keys (MDC and explicit field) produce two JSON keys; pick one.

## Verify
- [ ] A log line from a background task spawned by a request carries the request's trace_id.
- [ ] Load test shows no cross-request field leakage.
