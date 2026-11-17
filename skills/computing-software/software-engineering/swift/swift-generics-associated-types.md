---
id: computing-software.software-engineering.swift.swift-generics-associated-types
name: swift-generics-associated-types
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-protocols, generics-associated-types]
level: advanced
status: docs-checked
description: "Write generic functions and protocols with type constraints, where clauses and associated types."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generics constraints and associated types
- Constrain a type parameter with a protocol (`<T: Comparable>`) and add `where` clauses, for example `protocol ComparableContainer: Container where Item: Comparable { }`.
- A protocol with an associated type (`associatedtype Item`) can't be used as a plain type: write `any Container`, or return `some Container`.
- An existing type can adopt such a protocol with `extension Array: Container {}` when it already satisfies the requirements.
Verify: compile with a violating type to see constraint diagnostics.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): Generics chapter (constraints, where clauses, associated types) and OpaqueTypes chapter (any Container versus some Container).
Removed: primary associated types, Swift 5.7 note and performance advice.
Method: documentation only; no commands were run.
