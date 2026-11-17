---
id: computing-software.software-engineering.swift.swift-preconditions-assertions
name: swift-preconditions-assertions
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-errors, preconditions-assertions]
level: practitioner
status: docs-checked
description: "Use assert, precondition and fatalError correctly and know build-configuration differences."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preconditions assertions and fatalError
- `assert` is checked in debug builds only; `precondition` also in -O builds (removed in -Ounchecked); `fatalError` always terminates.
- Use `precondition` for programmer errors in API contracts, throws for recoverable runtime failure.
- `Never` return type for functions that don't return.
Verify: build Release and confirm which checks remain.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): The Basics chapter, Assertions and Preconditions (assert debug only, precondition in debug and production, not checked under -Ounchecked, fatalError always halts).
Not checked as a book claim: the advice to prefer throws for recoverable failures is guidance.
Method: documentation only; no commands were run.
