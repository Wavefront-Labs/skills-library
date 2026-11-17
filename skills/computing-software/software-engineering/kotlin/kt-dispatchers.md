---
id: computing-software.software-engineering.kotlin.kt-dispatchers
name: kt-dispatchers
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-coroutines, dispatchers]
level: practitioner
status: docs-checked
description: "Pick Default, IO, Main and limited-parallelism dispatchers and switch with withContext."
sources: ["https://kotlinlang.org/docs/home.html", "https://kotlinlang.org/spec/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dispatchers and withContext
- `Dispatchers.Default` is the default when no dispatcher is given and uses a shared background pool of threads; `Dispatchers.Main` is the dispatcher `MainScope()` uses for UI applications.
- `withContext(dispatcher) { ... }` may suspend and switches to the new dispatcher, then returns to the original one when the block finishes.
- For `Dispatchers.IO` pool size and `limitedParallelism`, read the kotlinx.coroutines API reference.
Verify: use a TestDispatcher in tests rather than real ones.

## Checked
2026-11-02. Confirmed: kotlinlang.org/docs/coroutine-context-and-dispatchers.html: Default dispatcher and shared pool, MainScope uses Dispatchers.Main, withContext switching.
Removed: Default pool-size rule, IO 64-thread figure, limitedParallelism and the Android artifact name (not in the page).
Method: documentation only; no commands were run.
