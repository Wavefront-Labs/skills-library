---
id: computing-software.software-engineering.kotlin.kt-coroutine-context-job
name: kt-coroutine-context-job
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-coroutines, coroutine-context-job]
level: practitioner
status: docs-checked
description: "Compose CoroutineContext elements (Job, dispatcher, name), use SupervisorJob, and understand parent-child Job relationships and states."
sources: ["https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html", "https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CoroutineContext and Job
A `CoroutineContext` holds elements such as `Job`, `CoroutineDispatcher` and `CoroutineName`. Combine several with the `+` operator.

```kotlin
val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default + CoroutineName("sync"))

val job = scope.launch {
    println(coroutineContext[CoroutineName])   // CoroutineName(sync)
    println(coroutineContext[Job]?.parent)     // the SupervisorJob
}
job.join()
scope.cancel()                                 // cancels all children
```

- A coroutine launched in another coroutine's scope inherits its context, and its `Job` becomes a child of the parent's job. Cancelling the parent recursively cancels all children; a parent always waits for its children to complete.
- Regular `Job`: failure of a child with an exception other than `CancellationException` immediately cancels its parent and so all other children. `SupervisorJob` customises this behaviour.
- `cancel()` on a job only takes a `CancellationException` cause, so it is a normal cancellation that does not cancel the parent; `join()` waits for completion.
- Job states: New, Active, Completing (transient), Cancelling (transient), Cancelled, Completed; query with `isActive`, `isCancelled`, `isCompleted`. `parent` is null if the job has no parent or completed successfully.
- Passing a different `Job` object as the context of a new coroutine (for example `launch(Job())`) overrides the parent scope's Job, and so does launching in another scope such as `GlobalScope`. The work is then not cancelled with the original scope. Avoid it.

Verify: launch two children in a `SupervisorJob` scope, throw in one, and confirm the other completes; repeat with a plain `Job()` and confirm both are cancelled.

## Checked
2026-11-09. Confirmed against the coroutine context and dispatchers guide and the Job API page: the + operator for contexts, child Job inheritance, recursive cancellation, parent waiting for children, parent/child override by passing a Job or another scope, failure propagation and SupervisorJob customisation, the cancel() CancellationException rule, the state table and parent property.
Removed: the "right side wins" rule, the claims about SupervisorJob applying only to direct children and async grandchildren, the exception-handler routing, and `cancelAndJoin` (not on the cited pages).
Method: documentation only; no commands were run.
