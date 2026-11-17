---
id: computing-software.software-engineering.swift.swift-async-sequence
name: swift-async-sequence
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-concurrency, async-sequence]
level: advanced
status: docs-checked
description: "Iterate an asynchronous sequence with for-await-in."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Asynchronous sequences
- An asynchronous sequence yields one element at a time instead of returning the whole collection at once: `for try await line in handle.bytes.lines { print(line) }` (the book's example uses Foundation's `FileHandle.standardInput`).
- Synchronous code can't call asynchronous code, so the loop must sit in an async context.
Verify: run the loop on small input and confirm elements arrive one at a time.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): Concurrency chapter, Asynchronous Sequences section.
Removed: AsyncStream, continuation, withCheckedThrowingContinuation and onTermination claims (not in the book).
Method: documentation only; no commands were run.
