---
id: computing-software.software-engineering.concurrency.reactive-streams-and-backpressure
name: reactive-streams-and-backpressure
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, reactive-streams, project-reactor, rxjava, backpressure, flux]
level: advanced
status: draft
description: "Build with Reactive Streams (Project Reactor, RxJava, Flow API): publisher/subscriber demand, backpressure strategies, schedulers, error handling, and avoiding blocking calls."
sources: ["https://www.reactive-streams.org/", "https://projectreactor.io/docs/core/release/reference/", "https://github.com/ReactiveX/RxJava/wiki/Backpressure-(2.0)", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Flow.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reactive streams and backpressure

## The spec
Reactive Streams (also `java.util.concurrent.Flow`): `Publisher`, `Subscriber`, `Subscription`,
`Processor`. The subscriber signals **demand** with `request(n)`; the publisher must not emit more
than requested. That's backpressure: slow consumers throttle fast producers instead of buffering
unboundedly.

## Project Reactor (Spring WebFlux)
```java
Flux.fromIterable(orderIds)
    .flatMap(id -> client.fetchOrder(id), 16)         // max 16 concurrent inner requests
    .filter(Order::isPaid)
    .bufferTimeout(100, Duration.ofSeconds(1))
    .concatMap(batch -> repo.saveAll(batch))          // sequential, preserves order
    .timeout(Duration.ofSeconds(30))
    .retryWhen(Retry.backoff(3, Duration.ofMillis(200)))
    .onErrorResume(e -> { log.error("sync failed", e); return Mono.empty(); })
    .subscribe();
```
- `flatMap` (concurrent, unordered) vs `concatMap` (sequential, ordered) vs `flatMapSequential`.
- Nothing happens until subscribe (cold publishers).

## Backpressure strategies when the source can't slow down
Reactor `onBackpressureBuffer(max, BufferOverflowStrategy.DROP_OLDEST)`, `onBackpressureDrop()`,
`onBackpressureLatest()`, `onBackpressureError()`; RxJava `Flowable` with the same operators
(`Observable` has no backpressure). Choose per data: drop for telemetry, latest for UI state, buffer
with bound for bursts, error to surface overload.

## Schedulers and blocking
- Reactor event loops (Netty) must never block: wrap blocking calls with
  `Mono.fromCallable(() -> jdbcCall()).subscribeOn(Schedulers.boundedElastic())`.
- `publishOn` switches downstream execution; `subscribeOn` affects where the source subscribes.
- Detect accidental blocking with BlockHound in tests.

## Debugging
Stack traces are unhelpful by default: `Hooks.onOperatorDebug()` in dev, `.checkpoint("desc")`, or
the `reactor-tools` agent (`ReactorDebugAgent.init()`) in production. `.log()` prints signals.

## When not to
With Java 21 virtual threads, plain blocking code often gives similar scalability with simpler
debugging. Keep reactive for streaming data, backpressure-aware pipelines, and existing reactive
stacks.
