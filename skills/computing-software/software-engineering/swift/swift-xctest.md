---
id: computing-software.software-engineering.swift.swift-xctest
name: swift-xctest
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-testing, xctest]
level: intro
status: draft
description: "Write XCTest cases, async tests, expectations and measure blocks."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# XCTest unit tests and async tests
- Subclass `XCTestCase`; methods named `test...`; `XCTAssertEqual`, `XCTAssertThrowsError`, `XCTUnwrap`.
- Async: `func testFetch() async throws { let r = try await sut.load(); XCTAssertEqual(...) }`; older callback code uses `XCTestExpectation` and `wait(for:timeout:)`.
- `setUpWithError`/`tearDown`; use `@MainActor` on test classes touching UI types.
Verify: `swift test` or `xcodebuild test -scheme X -destination ...`.
