---
id: computing-software.web-development.vapor.vapor-testing-vaportesting-xctvapor
name: vapor-testing-vaportesting-xctvapor
category: computing-software
field: web-development
product: vapor
tags: [vapor, vaportesting, xctvapor, testing, swift-testing, xctest, withapp, swift]
level: practitioner
status: docs-checked
description: "Test Vapor apps with VaporTesting (Swift Testing, withApp) or XCTVapor (XCTest): send requests, in-memory vs running, DB tests."
sources:
  - https://docs.vapor.codes/advanced/testing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: send test requests to a Vapor app and assert on responses. The docs recommend Swift Testing over XCTest for newer projects.

## VaporTesting (Swift Testing)
Add the product to the test target (the page's example uses vapor `from: "4.110.1"`):

```swift
.testTarget(name: "AppTests", dependencies: [
    .target(name: "App"),
    .product(name: "VaporTesting", package: "vapor"),
])
```

Warning from the page: use the matching testing module, or Vapor test failures may not be reported properly.

```swift
@testable import App
import VaporTesting
import Testing

@Suite("App Tests")
struct AppTests {
    @Test("Test Hello World Route")
    func helloWorld() async throws {
        try await withApp(configure: configure) { app in
            try await app.testing().test(.GET, "hello") { res async in
                #expect(res.status == .ok)
                #expect(res.body.string == "Hello, world!")
            }
        }
    }
}
```

`withApp` handles creating, configuring and shutting down the `Application`. Use `@Suite("...", .serialized)` to serialize tests, e.g. with a database.

Complex requests: pass `beforeRequest:` (set headers, `try req.content.encode(dto)`) and `afterResponse:`. The Content API works on both request and response.

Testing method: `app.testing(method: .inMemory)` (default), `.running` (live HTTP server, port 8080 by default) or `.running(port: 8123)`.

## Database tests
Use a test-only database in `configure`:

```swift
if app.environment == .testing {
    app.databases.use(.sqlite(.memory), as: .sqlite)
} else {
    app.databases.use(.sqlite(.file("db.sqlite")), as: .sqlite)
}
```

Warning: make sure tests run against the right database so data is not overwritten. Write your own helper (the page calls it `withAppIncludingDB`) that does `Application.make(.testing)`, `configure`, `autoMigrate()`, runs the test, then `autoRevert()` and `asyncShutdown()` (also on error), so each test starts from a fresh schema.

## XCTVapor (XCTest)
Add `.product(name: "XCTVapor", package: "vapor")` to the test target, `import XCTVapor`, subclass `XCTestCase`.

```swift
let app = Application(.testing)
defer { app.shutdown() }
try configure(app)

try app.test(.GET, "hello") { res in
    XCTAssertEqual(res.status, .ok)
    XCTAssertEqual(res.body.string, "Hello, world!")
}
```

You must call `app.shutdown()` before the app deinitializes; skipping it can crash the suite with a precondition failure when threads are allocated for the next `Application`. Method selection is `app.testable(method: .inMemory)` or `.running` / `.running(port: 8123)`.

## Checked

2026-11-08: read in full the Testing page at docs.vapor.codes/advanced/testing/ (VaporTesting and XCTVapor setup, withApp, testing method and default port 8080, database test helper). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08
