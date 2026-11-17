---
id: computing-software.software-engineering.mobile-development.kotlin-coroutines-and-flow-on-android
name: kotlin-coroutines-and-flow-on-android
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, kotlin, kotlin-flow, coroutines, stateflow, sharedflow, viewmodelscope, dispatchers]
level: practitioner
status: docs-checked
description: "Use coroutines and Flow on Android: viewModelScope, main-safe suspend functions, StateFlow versus SharedFlow, stateIn/WhileSubscribed and lifecycle-aware collection."
sources:
  - https://developer.android.com/kotlin/coroutines
  - https://developer.android.com/kotlin/flow/stateflow-and-sharedflow
  - https://developer.android.com/topic/libraries/architecture/coroutines
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coroutines and Flow on Android

```kotlin
class FeedViewModel(private val repo: FeedRepository) : ViewModel() {
    val uiState: StateFlow<FeedUiState> = flow { emit(FeedUiState.Success(repo.fetch())) }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = FeedUiState.Loading
        )

    fun refresh() = viewModelScope.launch { repo.refresh() }   // repo.refresh() is main-safe
}

// Activity/Fragment
lifecycleScope.launch {
    repeatOnLifecycle(Lifecycle.State.STARTED) {
        viewModel.uiState.collect { render(it) }
    }
}
// Compose
val state by viewModel.uiState.collectAsStateWithLifecycle()
```

## Rules
- A function is main-safe when it does not block UI updates on the main thread. Make a repository `suspend` function main-safe by switching inside it with `withContext(Dispatchers.IO)`; callers launched from `viewModelScope` (main thread by default) then need no dispatcher argument.
- Scopes: coroutines in `viewModelScope` are cancelled when the ViewModel is cleared. In Compose, `LaunchedEffect` is tied to the composable's presence in the composition and is cancelled when it leaves; relaunched when its key changes. It can run for composables that are composed but not visible (for example neighbouring pager pages), so use lifecycle-aware APIs such as `LifecycleEventEffect` for effects that need the screen to be seen (an analytics event).
- `StateFlow` is a hot, state-holding flow: it needs an initial value, exposes the current value through `value`, and a new collector receives the latest state then later updates. Use it for UI state, with a private `MutableStateFlow` backing property.
- `SharedFlow` generalises StateFlow: `replay` resends previous values to new subscribers and `onBufferOverflow` sets the full-buffer policy (default `BufferOverflow.SUSPEND`; others `DROP_LATEST`, `DROP_OLDEST`). The docs example uses `MutableSharedFlow<Unit>(replay = 0)` for periodic ticks.
- `stateIn` converts any flow to a StateFlow; `shareIn` turns a cold flow into a SharedFlow (scope, replay count, start policy). `SharingStarted.WhileSubscribed()` keeps upstream active while there are subscribers; `Eagerly` starts immediately; `Lazily` starts at the first subscriber and stays active. `WhileSubscribed(5000)` keeps the subscription alive for five seconds after the UI disappears, to ride out configuration changes.
- Inject dispatchers (for example into repositories) rather than hard-coding them, for easier testing.
- Never collect a UI flow directly in `launch` or `launchIn`: they keep processing events when the view is not visible, which can crash the app. Use `repeatOnLifecycle(Lifecycle.State.STARTED)` (needs `lifecycle-runtime-ktx` 2.4.0 or higher) or, in Compose, `collectAsStateWithLifecycle()`, which by default collects from STARTED to STOPPED (override with `minActiveState`).
- Unlike `LiveData.observe()`, collecting a flow does not stop automatically when the view is STOPPED.

## Checked
Confirmed on 2026-11-08 against the three cited Android developer pages (coroutines, StateFlow and SharedFlow, lifecycle-aware coroutine scopes): main-safety and `withContext`, `viewModelScope` cancellation, `LaunchedEffect` behaviour, StateFlow and SharedFlow semantics and parameters, `shareIn` start policies, `repeatOnLifecycle` and its 2.4.0 version note, `collectAsStateWithLifecycle`, WhileSubscribed(5000). Removed because the pages do not state them: StateFlow conflating equal updates, preferring state over SharedFlow for events, swallowing `CancellationException`, `GlobalScope` and `flowOn` gotchas, and the runTest/Turbine testing note.
Method: docs-only read of cited pages, 2026-11-08
