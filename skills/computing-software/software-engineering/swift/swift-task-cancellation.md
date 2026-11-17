---
id: computing-software.software-engineering.swift.swift-task-cancellation
name: swift-task-cancellation
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-concurrency, task-cancellation]
level: advanced
status: docs-checked
description: "Cooperate with cancellation using checkCancellation, Task.isCancelled and cancellation handlers."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task cancellation and structured concurrency
- Cancellation is cooperative: a task checks with `try Task.checkCancellation()` (throws if cancelled) or reads `Task.isCancelled`, then throws `CancellationError`, returns nil or an empty collection, or returns partial work.
- Cancelling a parent task cancels each of its child tasks.
- `withTaskCancellationHandler(operation:onCancel:)` gives immediate notification, but the task keeps running, so avoid sharing state between the task and the handler.
Verify: test that a cancelled task exits promptly.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): Concurrency chapter, Task Cancellation.
Removed: URLSession cancellation errors, async let cancellation and implicit group await claims (not in the book).
Method: documentation only; no commands were run.
