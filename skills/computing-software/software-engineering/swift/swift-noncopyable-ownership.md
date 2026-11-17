---
id: computing-software.software-engineering.swift.swift-noncopyable-ownership
name: swift-noncopyable-ownership
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-memory, noncopyable-ownership]
level: advanced
status: docs-checked
description: "Understand ~Copyable and the borrowing, consuming and inout parameter modifiers."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Noncopyable types and ownership modifiers
- `~Copyable` suppresses the implicit `Copyable` constraint (read it as "maybe copyable"); generic code under it can't copy the value, and assignment consumes it, so using it twice is an error.
- Noncopyable values must be passed as `inout`, `borrowing` or `consuming` parameters.
- Initialisers and property setters are consuming by default; everything else is borrowing.
Verify: assign a `~Copyable`-generic value twice and confirm the compiler rejects it.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): Generics chapter (implicit constraints, ~Copyable) and Declarations reference (borrowing and consuming parameters).
Removed: File example, consume operator, Swift version range and evolution proposal numbers.
Method: documentation only; no commands were run.
