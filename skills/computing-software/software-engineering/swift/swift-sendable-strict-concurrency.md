---
id: computing-software.software-engineering.swift.swift-sendable-strict-concurrency
name: swift-sendable-strict-concurrency
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-concurrency, sendable-strict-concurrency]
level: advanced
status: docs-checked
description: "Mark types Sendable so they can cross concurrency domains, and know what @unchecked Sendable means."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sendable and strict concurrency checking
- A `Sendable` type can be passed between concurrency domains, for example as an argument to an actor method. Ways to qualify: a value type whose mutable state is sendable data; a type with no mutable state; a type that protects its mutable state (a `@MainActor` class, or serialised access on a thread or queue). Closures can be marked `@Sendable`.
- Unsafe sharing of a class with unsynchronised mutable properties can give unpredictable results.
- `@unchecked` is an attribute for a conformance, and `Sendable` is its only supported protocol: it tells the compiler to skip the check, so you must guarantee safety yourself.
Verify: declare `struct TemperatureReading: Sendable` with sendable stored properties and pass it to an actor method.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): Concurrency chapter, Sendable Types, and Attributes reference (unchecked).
Removed: strict concurrency build settings, Swift 6 language mode flags and Package.swift setting (not in the book).
Method: documentation only; no commands were run.
