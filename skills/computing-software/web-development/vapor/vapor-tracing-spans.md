---
id: computing-software.web-development.vapor.vapor-tracing-spans
name: vapor-tracing-spans
category: computing-software
field: web-development
product: vapor
tags: [vapor, tracingmiddleware, tracing, spans, distributed-tracing, opentelemetry, swift]
level: advanced
status: docs-checked
description: "Add request tracing to Vapor with TracingMiddleware, span propagation (automatic or manual), and the NIO future caveat."
sources:
  - https://docs.vapor.codes/advanced/tracing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get a span per request and nest your own spans under it. Built on swift-distributed-tracing, so any of its backends (e.g. OpenTelemetry) work.

## Enable
```swift
app.middleware.use(TracingMiddleware())
```
Add it before other middlewares for accurate timings and correct identifier propagation to other services.

## Propagation to route handlers
Automatic: set during configuration.

```swift
app.traceAutoPropagation = true
```
Then use `withSpan("name") { _ in ... }` normally inside routes. Trade-off from the page: request span metadata is restored for every handler, which may hurt high-throughput APIs with minimal tracing needs.

Manual: `TracingMiddleware` sets `Request.serviceContext`; pass it as the context.

```swift
return try await withSpan("getNameParameter", context: req.serviceContext) { _ in
    try await process(result)
}
```

To restore metadata without making a span (so spans from downstream async libraries nest under the request span), wrap the work in `ServiceContext.withValue(req.serviceContext) { ... }`.

## NIO EventLoopFuture code
Tracing uses TaskLocal values, so you must re-restore context at every `EventLoopFuture` boundary, with or without auto-propagation:

```swift
withSpan("fetch", context: req.serviceContext) { span in
    fetchSomething().map { result in
        withSpan("process", context: span.context) { _ in
            process(result)
        }
    }
}
```

## Checked

2026-11-08: read in full the Tracing page at docs.vapor.codes/advanced/tracing/ (TracingMiddleware, traceAutoPropagation, serviceContext, ServiceContext.withValue, NIO caveat). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08
