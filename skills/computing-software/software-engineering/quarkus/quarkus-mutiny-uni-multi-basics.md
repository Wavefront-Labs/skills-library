---
id: computing-software.software-engineering.quarkus.quarkus-mutiny-uni-multi-basics
name: quarkus-mutiny-uni-multi-basics
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, mutiny, uni, multi, reactive, async, event-driven]
level: intro
status: docs-checked
description: "Write Mutiny pipelines in Quarkus: pick Uni or Multi, transform, chain and recover with onItem/onFailure, subscribe, and avoid blocking I/O threads."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/mutiny-primer.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus Mutiny: Uni and Multi basics

Mutiny is the primary reactive API in Quarkus. Everything is an event you observe and react to, written as `onX().action()` ("on item X do action"). Both types are lazy.

## Pick the type
- `Uni<T>`: emits one event, an item or a failure. Use for asynchronous actions that return 0 or 1 result (for example sending a message to a broker queue).
- `Multi<T>`: emits n items, then 1 failure or 1 completion. Use for streams, possibly unbounded.

## Core operators
- Observe, synchronous: `onItem().invoke(item -> ...)`, `onFailure().invoke(f -> ...)`.
- Observe, asynchronous: `onItem().call(item -> someAsyncAction(item))`. It does not change the item; the original item is emitted downstream once the async action completes.
- Transform with a sync function: `onItem().transform(item -> ...)`.
- Chain a dependent async step: `onItem().transformToUni(item -> anotherAsynchronousAction(item))` (the function returns a `Uni`).
- Recover: `onFailure().recoverWithItem(fallback)`; retry: `onFailure().retry().atMost(5)`.

## Uni shortcuts
`map` = `onItem().transform`; `flatMap` and `chain` = `onItem().transformToUni`; `invoke`/`call` = the `onItem()` versions; `replaceWith(x)` = transform to a constant; `replaceIfNullWith(x)` = `onItem().ifNull().continueWith(x)`; `eventually(...)` = `onItemOrFailure().invoke/call` ignoring both values.

## Subscribe or nothing happens
Subscribing triggers the operation:
```java
collection.insertOne(element)
    .onItem().transform(r -> r.getInsertedId().asString())
    .subscribe().with(
        result -> System.out.println("inserted " + result),
        failure -> System.out.println("failed " + failure));
```
For a `Multi`, `subscribe().with(item, failure, completion)` also takes a completion handler. In Quarkus some extensions deal with the subscription for you, and Quarkus REST and Reactive Messaging understand methods that return a `Uni` or `Multi`.

## Rules and gotchas
- Code runs on a few I/O threads; never block them. Schedule the I/O and express the continuation with the operators above.
- Quarkus integration: calling `await` or `toIterable` fails on an I/O thread (to protect it); `log()` uses the Quarkus logger; the default Mutiny pool is the Quarkus worker pool; context propagation is on by default for Uni and Multi.
- `Multi` implements `Publisher` and honours back-pressure; for sources you cannot throttle (time, sensors) use `onOverflow()`. `Uni` does not implement `Publisher`.
- The Vert.x API has Mutiny variants (`io.vertx.mutiny...`) returning `Uni` and `Multi`.

## Checked

2026-11-07. Matched against the text (with includes) of: mutiny-primer.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: two statements not on the page: the Uni use-case wording and the sentence on who handles subscription; both now follow the page (0 or 1 result, for example sending a message to a broker queue; some extensions deal with the subscription, and Quarkus REST and Reactive Messaging understand `Uni`/`Multi` return types).

Method: documentation only; no commands were run.
