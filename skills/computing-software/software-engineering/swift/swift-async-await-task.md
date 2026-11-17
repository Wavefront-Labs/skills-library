---
id: computing-software.software-engineering.swift.swift-async-await-task
name: swift-async-await-task
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-concurrency, async-await-task]
level: practitioner
status: docs-checked
description: "Write async functions and start work with Task, async let and task groups."
sources: ["https://docs.swift.org/swift-book/", "https://www.swift.org/documentation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# async await and Task
- `func fetch() async throws -> Data`; call with `try await`. Suspension points are where other work may interleave.
- `Task { }` defaults to the current actor isolation, priority and task-local state; `Task.detached { }` does not inherit them. `async let a = f(); let r = try await a` for fixed parallelism; `withThrowingTaskGroup` for dynamic counts.
- An unstructured task has no parent task; you are responsible for waiting on it or cancelling it through the task value it returns.
Verify: cancel a parent task and confirm its child tasks are cancelled.

## Checked
2026-11-03. Confirmed against the Swift Programming Language book (swiftlang/swift-book source): Concurrency chapter (await marks suspension points, async let, task groups and withThrowingTaskGroup, Task initializer versus Task.detached, parent cancellation reaches children).
Removed: async test functions advice.
Method: documentation only; no commands were run.
