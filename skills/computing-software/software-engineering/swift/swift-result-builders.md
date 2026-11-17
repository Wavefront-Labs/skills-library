---
id: computing-software.software-engineering.swift.swift-result-builders
name: swift-result-builders
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-closures, result-builders]
level: advanced
status: docs-checked
description: "Understand @resultBuilder as used by SwiftUI and write small builders for DSLs."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Result builders and function builders
- A `@resultBuilder` type is never instantiated; it implements static methods. It must implement `buildBlock(_:)` or both `buildPartialBlock(first:)` and `buildPartialBlock(accumulated:next:)`.
- Optional methods add DSL features: `buildOptional`, `buildEither(first:)` with `buildEither(second:)`, `buildArray`, `buildExpression`, `buildFinalResult`, `buildLimitedAvailability`.
Verify: unit-test builder output on empty, single, conditional bodies.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): Attributes reference, resultBuilder section.
Removed: SwiftUI ViewBuilder remark and the tuple arity and parameter pack limit (not in the book).
Method: documentation only; no commands were run.
