---
id: computing-software.software-engineering.kotlin.kt-coroutine-exceptions
name: kt-coroutine-exceptions
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-coroutines, coroutine-exceptions]
level: advanced
status: docs-checked
description: "Handle exceptions from launch and async, SupervisorJob and CoroutineExceptionHandler correctly."
sources: ["https://kotlinlang.org/docs/exception-handling.html", "https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-supervisor-job.html", "https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/supervisor-scope.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exception handling in coroutines
- Builders come in two flavours: `launch` propagates exceptions automatically, while `async` exposes them to the user through `await()`.
- A coroutine that fails with an exception other than `CancellationException` cancels its parent with that exception.
- `CoroutineExceptionHandler` is installed on a root coroutine (and is used for its children); it has no effect for `async`, whose exception is delivered at `await()`.
- try/catch inside the coroutine around `await`/suspend calls is the usual approach.
- `SupervisorJob` (or `supervisorScope`) makes failure propagate downward only: a failed child does not cancel the supervisor or its other children.
Verify: test a failing child with and without a supervisor.

## Checked
2026-11-03. Confirmed on the coroutines exception handling page and the SupervisorJob and supervisorScope API pages: launch vs async propagation, parent cancellation, root-coroutine handler, supervisor semantics.
Removed: "(but also cancel the parent unless supervised)" for async was folded into the general parent-cancellation rule.
Method: documentation only; no commands were run.
