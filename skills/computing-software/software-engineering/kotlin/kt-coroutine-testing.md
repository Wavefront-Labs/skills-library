---
id: computing-software.software-engineering.kotlin.kt-coroutine-testing
name: kt-coroutine-testing
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-testing, coroutine-testing]
level: advanced
status: docs-checked
description: "Test suspend code with runTest, TestDispatcher and virtual time."
sources: ["https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-test/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing coroutines with runTest
- `runTest { }` from kotlinx-coroutines-test executes under a `TestCoroutineScheduler`, a virtual-time scheduler that skips delays. Control it with `advanceTimeBy(delta)`, `advanceUntilIdle()`, `runCurrent()` and read `currentTime`.
- `StandardTestDispatcher` is linked to the scheduler; inject dispatchers into the code under test.
- `Dispatchers.setMain(dispatcher)` overrides `Main` for tests and takes effect globally; call `Dispatchers.resetMain()` afterwards.
- `runTest` waits for coroutines launched from the test body, so use `backgroundScope` for never-ending background work: coroutines launched there are cancelled at the end of the test.
Verify: a test with a long `delay` completes instantly.

## Checked
2026-11-03. Confirmed on the kotlinx-coroutines-test README: virtual time scheduler and its methods, StandardTestDispatcher, setMain/resetMain global effect, runTest waiting for children, backgroundScope cancellation.
Removed: Android-specific rule advice and "unfinished children fail the test" (not stated).
Method: documentation only; no commands were run.
