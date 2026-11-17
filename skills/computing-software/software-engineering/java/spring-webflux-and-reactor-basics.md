---
id: computing-software.software-engineering.java.spring-webflux-and-reactor-basics
name: spring-webflux-and-reactor-basics
category: computing-software
field: software-engineering
product: java
tags: [java, spring-web, spring-webflux, reactor, mono-flux, backpressure, webtestclient]
level: advanced
status: docs-checked
description: "Use Spring WebFlux and Project Reactor safely: wrap blocking calls, empty and retry handling, context propagation, debugging and testing with StepVerifier."
sources: ["https://docs.spring.io/spring-framework/reference/web/webflux.html", "https://github.com/reactor/reactor-core/tree/main/docs/modules/ROOT/pages", "https://docs.spring.io/spring-framework/reference/testing/webtestclient.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebFlux and Reactor basics

Spring WebFlux is the reactive-stack web framework (added in Spring Framework 5.0). It is fully non-blocking, supports Reactive Streams back pressure, and runs on Netty and on Servlet containers. It lives in the `spring-webflux` module beside `spring-webmvc`; an application can use one or both (for example Spring MVC controllers calling the reactive `WebClient`).

```java
@GetMapping("/users/{id}")
Mono<UserDto> get(@PathVariable String id) {
    return repo.findById(id)                                   // Mono<User>
        .switchIfEmpty(Mono.error(new ResponseStatusException(NOT_FOUND)))
        .map(UserDto::from);
}
```
Nothing happens until something subscribes; the framework subscribes for you. Use `defaultIfEmpty(T)` or `switchIfEmpty(Publisher)` to handle an empty source.

## Rules
1. **Never block** event-loop threads. Wrap an unavoidable synchronous, blocking call as `Mono.fromCallable(() -> ...)` followed by `.subscribeOn(Schedulers.boundedElastic())`. The Reactor FAQ gives the reason: `boundedElastic` waits on the blocking resource without disturbing non-blocking work and caps the number of threads and queued blocking tasks during a spike. `subscribeOn` does not subscribe; it only picks the scheduler, and should immediately follow the source.
2. Use a `Mono` when the source returns one value.
3. Retry with backoff using `Flux#retryWhen(Retry.backoff(...))`; the builder exists since Reactor 3.3.4.
4. Thread-locals do not follow reactive signals on their own. Put values in the Reactor `Context`; since reactor-core 3.5.0 the automatic mode, enabled once at application start with `Hooks.enableAutomaticContextPropagation()`, restores registered `ThreadLocal` state (via `ThreadLocalAccessor` instances in the `ContextRegistry`).
5. Return the publisher from handlers rather than subscribing inside them.

## Debugging
- `Hooks.onOperatorDebug()` activates a global debug mode at application start, giving assembly-site stack traces (it has a cost).
- `checkpoint()` and `checkpoint(String)` are finer-grained alternatives that mark a specific place in the chain; the String variant imposes less processing than the default.

## Verify
- `StepVerifier.create(publisher)` with expectations ending in `verifyComplete()` or `verifyError()`; the terminal `verify*` methods have no timeout by default, so set one to avoid hanging tests.
- `WebTestClient` wraps `WebClient` for HTTP tests: bind to a controller or application context without a server, or to a live server.

## Checked
Read the WebFlux overview, WebTestClient page, and the Reactor FAQ, context-propagation, debugging and testing pages (from the reactor-core docs sources on GitHub; the projectreactor.io page is a JS shell). Removed as unconfirmed: BlockHound, the flatMap default concurrency of 256, claims about exceptions thrown in assembly methods, R2DBC and reactive-driver advice, the MVC-with-virtual-threads comparison, the SSE snippet and the operator ordering descriptions.
Method: docs-checked 2026-11-09 against the Spring WebFlux and WebTestClient pages and the reactor-core FAQ, debugging, testing and context propagation docs.
