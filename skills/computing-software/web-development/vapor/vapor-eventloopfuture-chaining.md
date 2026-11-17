---
id: computing-software.web-development.vapor.vapor-eventloopfuture-chaining
name: vapor-eventloopfuture-chaining
category: computing-software
field: web-development
product: vapor
tags: [vapor,eventloopfuture,eventloop,promises,flatmap,futures,swift,swift-nio]
level: advanced
status: docs-checked
description: "Transform and chain Vapor EventLoopFutures with map, flatMap, flatMapThrowing and transform; create pre-completed futures, promises, whenComplete, get and wait."
sources:
  - https://docs.vapor.codes/basics/async/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: work with `EventLoopFuture` and promises where async/await is not an option.

A future is a read-only reference to a value that may arrive later; a promise (`EventLoopPromise`) is read/write and creates futures. Usually you only transform futures returned by Vapor.

## Transforming
| method | closure | result |
|-|-|-|
| `map` | `(T) -> U` | future of a different value |
| `flatMapThrowing` | `(T) throws -> U` | different value or error |
| `flatMap` | `(T) -> EventLoopFuture<U>` | avoids nested futures |
| `transform` | value `U` | ignore existing value, e.g. `userDidSave.transform(to: HTTPStatus.ok)` |

`flatMapThrowing` has the `flatMap` prefix because throwing creates a new future internally. Using `map` where `flatMap` is needed yields `EventLoopFuture<EventLoopFuture<...>>`.

Throwing call inside `flatMap`: use do/catch and `eventLoop.makeFailedFuture(error)`.

Chain:
```swift
let futureResponse = futureString.flatMapThrowing { string in
    guard let url = URL(string: string) else {
        throw Abort(.badRequest, reason: "Invalid URL string: \(string)")
    }
    return url
}.flatMap { url in
    client.get(url)
}
```

## Other APIs
- `eventLoop.makeSucceededFuture("hello")`, `eventLoop.makeFailedFuture(error)`.
- `futureString.whenComplete { result in ... }` with `.success` / `.failure`; many callbacks allowed.
- `try await future.get()` when no async alternative exists.
- `wait()` is obsolete: it blocks, works only on a background or main thread (e.g. configure.swift), never on an event loop thread (assertion failure).

## Promises
```swift
let promiseString = eventLoop.makePromise(of: String.self)
promiseString.succeed("Hello")   // or promiseString.fail(...)
```
Use `promiseString.futureResult`. A promise completes once; later completions are ignored. Event loops come from `req.eventLoop` or `app.eventLoopGroup.next()`.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) basics/async, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
