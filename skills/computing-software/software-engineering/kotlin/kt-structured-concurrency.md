---
id: computing-software.software-engineering.kotlin.kt-structured-concurrency
name: kt-structured-concurrency
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-coroutines, structured-concurrency]
level: advanced
status: docs-checked
description: "Tie coroutine lifetimes to a scope so children are cancelled and errors propagate."
sources: ["https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/coroutine-scope.html", "https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/supervisor-scope.html", "https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-global-scope/", "https://kotlinlang.org/docs/exception-handling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structured concurrency and CoroutineScope
- A scope's children are tied to it: cancelling the scope cancels all its children, and `coroutineScope { }` treats every child as crucial, so a failing child cancels the others and the scope.
- `supervisorScope { }` lets child failures stay isolated: a failing child does not affect its siblings; choose it when some failures are acceptable.
- Avoid `GlobalScope`: it has no `Job`, so launched coroutines cannot be cancelled together or awaited, and it is marked a delicate API. Inject a scope instead.
- A function that launches work should take a `CoroutineScope` or be a `suspend` function that waits for it.
Verify: test that cancelling the scope cancels all children (use `runTest`).

## Checked
2026-11-03. Confirmed on the coroutineScope, supervisorScope and GlobalScope API pages and the exception handling guide.
Removed: Android scopes `viewModelScope`/`lifecycleScope` (not on the pages).
Method: documentation only; no commands were run.
