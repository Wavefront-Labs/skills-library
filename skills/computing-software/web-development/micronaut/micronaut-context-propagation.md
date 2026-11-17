---
id: computing-software.web-development.micronaut.micronaut-context-propagation
name: micronaut-context-propagation
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, context-propagation, propagated-context, mdc, reactor, http-filter, thread-local]
level: advanced
status: docs-checked
description: "Propagate request context in Micronaut: add elements from HTTP filters with MutablePropagatedContext and carry PropagatedContext through Reactor chains."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/contextPropagation/httpFilterContextPropagation.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/contextPropagation/reactorContextPropagation.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: make request-related values (such as an MDC entry) available to later filters, controllers and reactive code.

## In an HTTP filter

With the non-reactive filter API, add a `MutablePropagatedContext` parameter and add or remove elements:

```java
@ServerFilter(MATCH_ALL_PATTERN)
public class MdcFilter {
    @RequestFilter
    public void myRequestFilter(HttpRequest<?> request, MutablePropagatedContext mutablePropagatedContext) {
        try {
            String trackingId = request.getHeaders().get("X-TrackingId");
            MDC.put("trackingId", trackingId);
            mutablePropagatedContext.add(new MdcPropagationContext());
        } finally {
            MDC.remove("trackingId");
        }
    }
}
```

The next filter in the chain (and the controller call) sees the new context, and its thread-local elements are set.

For legacy reactive `HttpServerFilter`s, propagate the modified context around the chain call:

```java
return PropagatedContext.get().plus(new MdcPropagationContext())
    .propagate(() -> chain.proceed(request));
```

(`MdcPropagationContext` is `io.micronaut.context.propagation.slf4j.MdcPropagationContext`.)

Caveat: the context only covers work after the filter runs. Framework log lines emitted earlier (e.g. on request receipt) do not see it, and an ordinary server filter runs after route matching. To have it during route matching use a filter annotated `@PreMatching`.

## With Project Reactor

Since Micronaut 4, Reactor state is not captured automatically; you extend the propagated context manually. The framework adds `PropagatedContext` to Reactor's context for interceptors and HTTP filters; read it via `ReactorPropagation` (experimental, may change).

To restore thread-local values through Reactor, add the Micrometer Context Propagation dependency (`io.micrometer:context-propagation`, compile scope). Thread-local values are read-only: to change them, modify the `PropagatedContext` and put it into Reactor's context. Mid-chain:

```java
@Get("/hello")
Mono<String> hello(@QueryValue("name") String name) {
    PropagatedContext propagatedContext = PropagatedContext.get().plus(new MyContextElement(name));
    return Mono.just("Hello, " + name)
        .contextWrite(ctx -> ReactorPropagation.addPropagatedContext(ctx, propagatedContext));
}

record MyContextElement(String value) implements PropagatedContextElement { }
```

To keep Micrometer Context Propagation on the classpath but unused:

```yaml
reactor:
    enable-automatic-context-propagation: false
```

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.
