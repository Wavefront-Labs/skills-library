---
id: computing-software.software-engineering.swift.swift-exclusivity-enforcement
name: swift-exclusivity-enforcement
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-memory, exclusivity-enforcement]
level: advanced
status: docs-checked
description: "Avoid overlapping memory accesses, such as aliasing inout arguments, that the compiler or runtime rejects."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exclusive access and value semantics safety
- A modification needs exclusive access to the memory; conflicting overlapping accesses give a compile-time or runtime error.
- Passing the same variable as two inout arguments is an error (`inout arguments are not allowed to alias each other`).
- Conflicts can happen on a single thread with no concurrency involved; for multithreaded code use Thread Sanitizer.
Verify: read the compiler or runtime error text for the overlapping access.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): MemorySafety chapter.
Removed: swap and swapAt claim, claim that runtime traps occur in both debug and release builds, Exclusive Access Enforcement settings.
Method: documentation only; no commands were run.
