---
id: computing-software.software-engineering.kotlin.kt-flow
name: kt-flow
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-coroutines, flow]
level: practitioner
status: gated
description: "Build cold asynchronous streams with Flow and use operators, context rules and collection safely."
sources: ["https://kotlinlang.org/docs/home.html", "https://kotlinlang.org/spec/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flow cold streams and operators
- `flow { emit(x) }` is cold: runs per collector. Operators: `map`, `filter`, `transform`, `buffer`, `conflate`, `flatMapLatest`, `debounce`, `catch`, `onEach`.
- Context preservation: do not `emit` from another context inside `flow {}`; use `flowOn(dispatcher)` to change upstream context.
- Exceptions: `catch` handles upstream errors only; downstream errors in `collect` propagate.
- Terminal operators: `collect`, `toList`, `first`, `single`. (gated: unconfirmed, source is paywalled or blocked)
Verify: test flows with Turbine or `toList()` under `runTest`.

## Checked
2026-11-02. Confirmed: Nothing: the Flow guide page returned an empty page to the fetcher, and the GitHub source path moved.
Gated: whole skill; kotlinlang.org/docs/flow.html unreadable by script, verify operators and context rules there.
Method: documentation only; no commands were run.
