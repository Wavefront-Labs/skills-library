---
id: computing-software.web-development.vapor.vapor-upgrading-3-to-4
name: vapor-upgrading-3-to-4
category: computing-software
field: web-development
product: vapor
tags: [vapor, upgrading, migration, vapor-3, vapor-4, eventloopfuture, fluent, package-swift]
level: advanced
status: docs-checked
description: "Migrate a Vapor 3 project to Vapor 4: Package.swift, main.swift, configure/routes, services, NIO renames, routing, middleware and Fluent changes."
sources:
  - https://docs.vapor.codes/upgrading/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: port a Vapor 3 app to 4. The guide assumes Xcode 11.4 and macOS 10.15+.

## Package.swift
Tools version 5.2, add `platforms: [.macOS(.v10_15)]`, bump package majors (vapor from 4.3.0, jwt 4.0.0, `fluent` 4.0.0 as a separate dependency plus a `-driver` package, e.g. fluent-postgres-driver 2.0.0). Targets use `.product(name:package:)`. Deprecated: auth, core, crypto (now SwiftCrypto), multipart, url-encoded-form, vapor-ext (all in Vapor), pagination (in Fluent), LoggerAPI (SwiftLog). After updating, delete `Package.resolved`, `.build`, `.swiftpm`, `*.xcodeproj`; open with `vapor xcode` or `open Package.swift`.

## Run / App
`main.swift` in Run replaces app.swift:
```swift
var env = try Environment.detect()
try LoggingSystem.bootstrap(from: &env)
let app = Application(env)
defer { app.shutdown() }
try configure(app)
try app.run()
```
Signatures become `configure(_ app: Application)` and `routes(_ app: Application)`; boot.swift contents move into configure.

## Services
Container/Service/Config are gone; services are properties of `Application` and `Request`.
- Port: `app.http.server.configuration.port = 8281`
- Middleware: `app.middleware.use(corsMiddleware)` (instances only, not type names, e.g. `ErrorMiddleware.default(environment: app.environment)`); remove all defaults with `app.middleware = .init()`
- Client: `req.client.get("https://vapor.codes")`
- Providers: `app.views.use(.leaf)`, `app.leaf.cache.isEnabled = false`
- Custom services: extend `Request`/`Application`. Lifecycle hooks via a `LifecycleHandler` and `app.lifecycle.use(...)`; stored values via `StorageKey` and `app.storage`.

## NIO
- `Future` alias removed (use `EventLoopFuture`); drop `to:` labels; `newPromise` becomes `eventLoop.makePromise(of:)`; `catchMap` becomes `mapError`/`flatMapErrorThrowing`; global `flatMap(a, b)` becomes `futureA.and(futureB).flatMap { (a, b) in ... }`.
- `Data` often becomes `ByteBuffer`; convert back with `Data(buffer.readableBytesView)`.
- `map`/`flatMap` can no longer throw: a throwing map becomes `flatMapThrowing`; inside flatMap return `eventLoop.makeFailedFuture(error)`, or chain `flatMapThrowing { a in try (a, doSomething()) }.flatMap { (a, result) in ... }`.

## Routing
Register on `app.get(...)`. Content decoding is synchronous (`try req.content.decode(T.self)`); use `body: .stream` for async bodies. Paths are comma separated with no `/` (`app.get("v1","users","posts")`). `Parameter` is removed: `app.get("planets", ":id")` plus `req.parameters.get("id")`.

## Fluent
`import Fluent` only. Models: `final class X: Model`, `static let schema`, empty `init()`, `@ID(key: .id)`, `@Field(key:)`, `@OptionalField(key:)`, `@Timestamp(key:on:)`; custom IDs use `@ID(custom:)`; `Model.ID` is now `IDValue`. `save/update/create` no longer return the model. Relations: `@Parent(key:)`, `@Children(for: \.$server)`, `@Siblings(through:from:to:)`; pivots are normal models. Queries: `Planet.query(on: req.db)`, key paths `\.$foo`. Models can't be route parameters: `Model.find(req.parameters.get("x"), on: req.db)`. Migrations are written manually (no auto migration), non-static `prepare/revert(on database: Database)`, e.g. `database.schema("Galaxy").id().field("name", .string, .required).create()`. Config: `app.databases.use(.postgres(url: "postgres://..."), as: .psql)`, `app.migrations.use(CreatePlanet(), on: .psql)`.

## Repositories
Make repositories structs and drop `ServiceType`; store a factory on `Application` via a `StorageKey`, expose it as `req.users`, set it in configure.swift (`app.users.use { req in DatabaseUserRepository(database: req.db) }`) and swap in a test repository in tests.

## Checked

2026-11-08: read in full the Upgrading to 4.0 page at docs.vapor.codes/upgrading/ (Package.swift changes, deprecated packages, Run/App, services, NIO renames, routing, Fluent, repositories). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08
