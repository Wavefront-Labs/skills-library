---
id: computing-software.software-engineering.kotlin.kt-result-runcatching
name: kt-result-runcatching
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-errors, result-runcatching]
level: practitioner
status: docs-checked
description: "Use Result and runCatching knowing that every Throwable is caught, including cancellation."
sources: ["https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-result/", "https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/run-catching.html", "https://kotlinlang.org/docs/exception-handling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Result and runCatching
- `runCatching { }` returns a `Result<R>`: the block's value, or a failure that encapsulates any `Throwable` it threw. Consume it with `getOrElse`, `onFailure`, `map` and `recover`.
- Because it catches every Throwable, in suspend code it also captures the `CancellationException` that coroutines use to signal cancellation; rethrow it or use a targeted try/catch there.
- For domain errors a sealed class is usually more expressive than `Result`.
Verify: test that a cancelled coroutine is not turned into a `Result.failure`.

## Checked
2026-11-03. Confirmed on the Result and runCatching API pages (catches any Throwable; getOrElse, onFailure, map, recover exist) and the coroutines exception handling page (cancellation uses CancellationException).
Removed: the OutOfMemoryError example and code snippets using unverified signatures.
Method: documentation only; no commands were run.
