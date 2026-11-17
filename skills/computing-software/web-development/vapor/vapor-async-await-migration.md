---
id: computing-software.web-development.vapor.vapor-async-await-migration
name: vapor-async-await-migration
category: computing-software
field: web-development
product: vapor
tags: [vapor,async-await,swift-concurrency,migration,eventloopfuture,package-swift,swift]
level: practitioner
status: docs-checked
description: "Migrate Vapor routes from EventLoopFuture to async/await: tools version, platforms, executableTarget, Dockerfile, and bridging with get() and promises."
sources:
  - https://docs.vapor.codes/basics/async/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move a Vapor app to async/await and bridge old APIs.

Most Vapor APIs offer both futures and async/await. Use one model per route handler, not a mix. Stay on `EventLoopFuture` for apps needing explicit event-loop control or very high performance (until custom executors exist); everyone else should prefer async/await.

## Prerequisites and Package.swift
macOS needs macOS 12+ and Xcode 13.1+; elsewhere Swift 5.5+. Update dependencies. Then:
```swift
// swift-tools-version:5.5
```
```swift
platforms: [ .macOS(.v12) ],
```
```swift
.executableTarget(name: "Run", dependencies: [.target(name: "App")]),
```
On Linux deploys also bump Swift (e.g. Heroku, Dockerfile): `FROM swift:5.5-focal as build` and `FROM swift:5.5-focal-slim`.

## Convert code
Functions returning `EventLoopFuture` generally become `async`:
```swift
routes.get("firstUser") { req async throws -> String in
    guard let user = try await User.query(on: req.db).first() else {
        throw Abort(.notFound)
    }
    user.lastAccessed = Date()
    try await user.update(on: req.db)
    return user.name
}
```

## Bridging
Future to async (APIs lacking an async version): `let v = try await someMethodThatReturnsAFuture().get()`.
Async to future:
```swift
let promise = request.eventLoop.makePromise(of: String.self)
promise.completeWithTask {
    try await someAsyncFunctionThatGetsAString()
}
let futureString: EventLoopFuture<String> = promise.futureResult
```

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) basics/async, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
