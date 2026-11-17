---
id: computing-software.software-engineering.swift.swift-task-groups
name: swift-task-groups
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-concurrency, task-groups]
level: practitioner
status: docs-checked
description: "Run child tasks in parallel with async let and withTaskGroup / withThrowingTaskGroup, collect results and handle errors."
sources: ["https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task groups and async let
`async let` implicitly creates a child task and suits a fixed set of calls. A task group (`TaskGroup`) lets you add child tasks explicitly, gives more control over priority and cancellation, and allows a dynamic number of tasks. Child tasks form a hierarchy, which is why it is called structured concurrency.

```swift
// Fixed number of calls: async let
async let a = fetch(1)
async let b = fetch(2)
let pair = try await (a, b)

// Dynamic number of calls: task group
func fetchAll(_ ids: [Int]) async throws -> [Int: Data] {
    try await withThrowingTaskGroup(of: (Int, Data).self) { group in
        for id in ids { group.addTask { (id, try await fetch(id)) } }
        var out: [Int: Data] = [:]
        for try await (id, data) in group { out[id] = data }
        return out
    }
}
```

- There is no guarantee about the order in which child tasks complete; key results (as above) if order matters.
- If a child could throw, use `withThrowingTaskGroup(of:returning:body:)` instead of `withTaskGroup(of:returning:body:)`.
- With `async let`, write `await` where you use the result; the calls themselves are not awaited at the declaration, so they can run at the same time if resources allow.
- Advantages of structured tasks: a parent cannot forget to wait for its children; raising a child's priority escalates the parent's; cancelling a parent cancels each child; task-local values propagate to children.
- Use `group.addTaskUnlessCancelled` and check its returned `Bool` to stop adding work once the group is cancelled; children can check `Task.isCancelled` and return nil so the group returns a partial result.

Verify: add `try Task.checkCancellation()` in the children, cancel the parent, and confirm the children stop with `CancellationError` rather than running to completion.

## Checked
2026-11-08: read the whole Concurrency chapter of The Swift Programming Language (swift-book source on GitHub). Confirmed all statements above against Defining and Calling Asynchronous Functions, Calling Asynchronous Functions in Parallel, Tasks and Task Groups and Task Cancellation. Removed: the claims that a throwing child cancels remaining children, that child closures are `@Sendable`, the windowed concurrency limit with `next()`, the unawaited `async let` gotcha and the thousands-of-tasks warning (none on the page), and the SE-0317 source (not read).
Method: documentation only; no commands were run.
