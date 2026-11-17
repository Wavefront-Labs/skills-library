---
id: computing-software.software-engineering.swift.swift-optional-chaining
name: swift-optional-chaining
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-optionals, optional-chaining]
level: intro
status: docs-checked
description: "Use ?. and ?? on optionals to access values without nested ifs."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Optional chaining and nil coalescing
- `a?.b?.c` short-circuits to nil; the result type of a chain is optional.
- `a ?? b` unwraps `a` if it has a value and otherwise returns `b`; `b` is evaluated only when `a` is nil (short-circuit evaluation).
Verify: unit-test nil and non-nil inputs for each chain.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): OptionalChaining chapter (?. short-circuits to nil, optional result) and BasicOperators chapter (nil-coalescing operator, short-circuit evaluation).
Removed: map, flatMap and optional Equatable comparison claims, and the autoclosure wording (not in the chapters).
Method: documentation only; no commands were run.
