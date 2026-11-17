---
id: computing-software.software-engineering.swift.swift-actors-isolation
name: swift-actors-isolation
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-concurrency, actors-isolation]
level: advanced
status: docs-checked
description: "Protect mutable state with actors, await actor access and use the main actor for UI work."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Actors and isolation
- An `actor` is a reference type that allows only one task at a time to access its mutable state; code outside the actor accesses its properties and methods with `await`, a possible suspension point, while code inside the actor needs no `await`.
- The main actor protects the data used to show the UI; mark a function or type `@MainActor` to isolate it there.
Verify: call an actor method from outside and confirm the compiler requires `await`.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): Concurrency chapter, Actors and Isolation sections.
Removed: reentrancy claim, general nonisolated bullet, Thread Sanitizer and strict checking advice (not in the chapter).

Method: documentation only; no commands were run.
