---
id: computing-software.software-engineering.kotlin.kt-stateflow-sharedflow
name: kt-stateflow-sharedflow
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-coroutines, stateflow-sharedflow]
level: advanced
status: docs-checked
description: "Use StateFlow, SharedFlow and Channel for hot streams and event delivery with correct replay semantics."
sources: ["https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-state-flow/", "https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-shared-flow/", "https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/state-in.html", "https://github.com/Kotlin/kotlinx.coroutines/blob/master/docs/topics/channels.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# StateFlow SharedFlow and Channels
- `StateFlow<T>` is a hot, read-only state holder with a current `value`; it never completes and updates are always conflated, so a slow collector skips intermediate values but sees the latest. Create `MutableStateFlow(initial)` privately and expose `asStateFlow()`.
- `SharedFlow` has a replay cache (`replay`) plus optional `extraBufferCapacity`; a value emitted when there are no subscribers is lost unless replayed.
- `stateIn(scope, started, initialValue)` turns a cold flow into a StateFlow; `SharingStarted.WhileSubscribed` stops the upstream when there are no subscribers.
- A `Channel` hands each element to one receiver and its send/receive operations are fair.
Verify: test late-subscriber behaviour for each type.

## Checked
2026-11-03. Confirmed on the StateFlow, SharedFlow and stateIn API pages and the channels guide: hot read-only state, conflation, asStateFlow, replay cache, extraBufferCapacity, lost emissions without subscribers, WhileSubscribed, channel fairness.
Removed: `WhileSubscribed(5_000)` literal, the Android `repeatOnLifecycle` advice and "conflates equal values" (not on the pages).
Method: documentation only; no commands were run.
