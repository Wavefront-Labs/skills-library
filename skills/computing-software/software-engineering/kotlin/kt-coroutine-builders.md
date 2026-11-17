---
id: computing-software.software-engineering.kotlin.kt-coroutine-builders
name: kt-coroutine-builders
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-coroutines, coroutine-builders]
level: practitioner
status: gated
description: "Start coroutines with launch, async and runBlocking and know what each returns and where to use it."
sources: ["https://kotlinlang.org/docs/home.html", "https://kotlinlang.org/spec/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Suspend functions and coroutine builders
- `suspend fun` can only be called from another suspend function or a coroutine; it does not itself create concurrency.
- `launch { }` returns a Job (fire and forget); `async { }` returns Deferred<T> whose `await()` surfaces exceptions; `runBlocking` bridges blocking code (main/tests), never inside coroutine code or UI threads.
- Parallel decomposition: `coroutineScope { val a = async { f() }; val b = async { g() }; a.await() + b.await() }`.
Verify: log thread names (`-Dkotlinx.coroutines.debug`) to confirm where code runs.

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; kotlinlang.org pages returned empty stubs (JavaScript only); nothing readable. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
