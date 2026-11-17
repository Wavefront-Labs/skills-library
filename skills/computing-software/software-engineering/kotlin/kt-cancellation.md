---
id: computing-software.software-engineering.kotlin.kt-cancellation
name: kt-cancellation
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-coroutines, cancellation]
level: advanced
status: gated
description: "Make coroutines cancellable cooperatively and handle CancellationException and timeouts."
sources: ["https://kotlinlang.org/docs/home.html", "https://kotlinlang.org/spec/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cancellation and timeouts
- Cancellation is cooperative: suspend functions from kotlinx.coroutines check it; tight CPU loops need `ensureActive()` or `yield()`.
- Do not swallow `CancellationException`; when catching `Exception` rethrow it. `runCatching` around suspend code catches it too, so rethrow.
- Cleanup in `finally`; suspending cleanup needs `withContext(NonCancellable)`.
- `withTimeout(ms)` throws TimeoutCancellationException; `withTimeoutOrNull` returns null. (gated: unconfirmed, source is paywalled or blocked)
Verify: test a long loop is cancelled within a bounded time.

## Checked
2026-11-02. Confirmed: Nothing: kotlinlang.org/docs/cancellation-and-timeouts.html returned an empty page to the fetcher.
Gated: whole skill; verify on that page.
Method: documentation only; no commands were run.
