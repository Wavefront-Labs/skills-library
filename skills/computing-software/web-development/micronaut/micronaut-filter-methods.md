---
id: computing-software.web-development.micronaut.micronaut-filter-methods
name: micronaut-filter-methods
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, filter-methods, server-filter, request-filter, response-filter, filters]
level: practitioner
status: docs-checked
description: "Write Micronaut HTTP server filters with @ServerFilter, @RequestFilter and @ResponseFilter methods, including URL patterns, ordering, error handling and continuations."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/filters.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/filters/filtermethods.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/filters/filtermethods/filtermethodsexample.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/filters/filtermethods/filtermethodproceed.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/filters/filtermethods/continuations.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/filters/filtermethods/order.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/filters/filtermethods/errorStates.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/filters/filterPatterns.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/filters/responseHeaderPopulator.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Micronaut filter methods

Goal: intercept requests and responses in the Micronaut HTTP server. The docs recommend filter methods (since 4.0) over implementing `HttpServerFilter`.

## Declare a filter
A bean annotated `@ServerFilter` (or `@ClientFilter` for the HTTP client) holds methods annotated `@RequestFilter` (before processing) or `@ResponseFilter` (after). `@PreMatching` on a request filter runs it before the route is matched.

```java
@ServerFilter("/hello/**")
public class TraceFilter {
    private final TraceService traceService;
    public TraceFilter(TraceService traceService) { this.traceService = traceService; }

    @RequestFilter
    @ExecuteOn(TaskExecutors.BLOCKING)
    public void filterRequest(HttpRequest<?> request) { traceService.trace(request); }

    @ResponseFilter
    public void filterResponse(MutableHttpResponse<?> res) {
        res.getHeaders().add("X-Trace-Enabled", "true");
    }
}
```

Return `void` or `null` to continue; return an updated request (request filters only) or a response to replace or short-circuit. To decide asynchronously, return `CompletableFuture<@Nullable HttpResponse<?>>`: completed with `null` proceeds, completed with a response (e.g. `HttpResponse.unauthorized()`) stops.

## Gotchas
- Filter methods run on the event loop by default. Put `@ExecuteOn` on the filter for blocking work.
- Patterns go in the class annotation or in `@RequestFilter`/`@ResponseFilter`. The default style is Ant: `?` one character, `*` zero or more characters, `**` zero or more subdirectories (e.g. `customer/**/*.html`). Set `patternStyle = FilterPatternStyle.REGEX` for a regex that must match the whole URL; Ant is preferred for speed.
- Order: `@Order`/`@Priority` on the method, then on the class, then `Ordered` on the class. Request filters run from the smallest number (highest precedence) upward; response filters run in reverse.
- A request filter can take a `FilterContinuation<MutableHttpResponse<?>>` parameter and call `continuation.proceed()` (blocking, so use `@ExecuteOn`), then edit the response. Declaring the continuation as `Publisher<HttpResponse<?>>`, `CompletionStage` or `CompletableFuture` makes it non-blocking; with the stage types call `proceed()` only once and never block in its callbacks.
- A response filter is only called for failures if it declares them: `responseFilter(HttpResponse<?> response, @Nullable Throwable failure)` is always called. However the server maps exceptions to error responses before each filter, so a server filter never actually sees an exception; the cause is in the `HttpAttributes.EXCEPTION` attribute.
- Request filters may bind `@Body`, which forces full buffering (Netty server only).

## Adding headers without a filter
Register a `@Singleton` implementing `ResponseHeaderPopulator` and return a `List<HttpHeaderEntry>` from `findHttpHeaders(request, response)`, e.g. `List.of(new HttpHeaderEntry("X-Content-Type-Options", "nosniff"))`, or `null` for none. A header already on the response keeps its value. Implement `getOrder()` to order several populators.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.
