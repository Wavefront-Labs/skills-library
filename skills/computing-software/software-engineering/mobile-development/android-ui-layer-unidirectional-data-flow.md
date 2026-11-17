---
id: computing-software.software-engineering.mobile-development.android-ui-layer-unidirectional-data-flow
name: android-ui-layer-unidirectional-data-flow
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, unidirectional-data-flow, ui-state, ui-layer, mvvm, mvi, state-holder, architecture]
level: practitioner
status: docs-checked
description: "Apply Android's recommended UI layer: immutable UI state exposed by a ViewModel, events flowing up, one-off effects as state, and testing the state holder."
sources: ["https://developer.android.com/topic/architecture/ui-layer", "https://developer.android.com/topic/architecture/ui-layer/state-production", "https://developer.android.com/topic/architecture/ui-layer/events"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UI layer and unidirectional data flow (UDF)

State flows down from the state holder (ViewModel) to the UI; events flow up from the UI to the state holder. The UI renders state and never mutates it.

```kotlin
data class LoginUiState(
    val email: String = "",
    val isLoading: Boolean = false,
    val errorMessage: String? = null,
    val loggedIn: Boolean = false
)

class LoginViewModel(private val auth: AuthRepository) : ViewModel() {
    private val _ui = MutableStateFlow(LoginUiState())
    val ui: StateFlow<LoginUiState> = _ui.asStateFlow()

    fun onEmailChanged(v: String) = _ui.update { it.copy(email = v, errorMessage = null) }
    fun onSubmit() = viewModelScope.launch {
        _ui.update { it.copy(isLoading = true) }
        auth.login(ui.value.email)
            .onSuccess { _ui.update { s -> s.copy(isLoading = false, loggedIn = true) } }
            .onFailure { e -> _ui.update { s -> s.copy(isLoading = false, errorMessage = e.message) } }
    }
}

@Composable fun LoginScreen(vm: LoginViewModel = viewModel()) {
    val state by vm.ui.collectAsStateWithLifecycle()
    LoginContent(state, onEmailChanged = vm::onEmailChanged, onSubmit = vm::onSubmit)
}
```

## Guidance (from the architecture guide)
- UI state is an immutable snapshot of what the UI needs to render; wrapping even simple data in a UI state type (one class per screen) is usually worthwhile and easy to extend. A single stream gives consistency; use separate streams only when the emitted items are unrelated. Paging's `PagingData` is not immutable, so expose it in its own stream.
- Handle UI events: events that need business logic (refresh, login) go to the ViewModel through functions it exposes, named with a verb (`login()`); UI behaviour logic (expand a card, navigation, showing a Snackbar) stays in the UI. Name handler parameters `on` + verb + target (`onItemClick`).
- Pass events down as lambdas rather than handing the ViewModel to child composables such as a list item.
- ViewModel events (navigate after login, show a message) should always result in a UI state update, which keeps them reproducible after configuration changes and not lost. For a transient message hold a `userMessage` in the state and have the UI call back (`userMessageShown()`) to clear it. Do not use `Channel`s or other streams for one-off events: delivery is not guaranteed when the producer outlives the consumer.
- Expose state with an observable holder: `mutableStateOf` or a private `MutableStateFlow` behind a public read-only `StateFlow` (`asStateFlow()`). For flows built from several sources, `stateIn(..., SharingStarted.WhileSubscribed(5_000), ...)` keeps the pipeline active only while the UI is visible.
- In Compose, consume flows with `collectAsStateWithLifecycle()` so observation stops when the UI is not shown.

## Gotchas
- `MutableStateFlow.update {}` makes the read-modify-write atomic; prefer it over assigning `_ui.value = _ui.value.copy(...)` from several coroutines.
- Keep UI logic that needs UI types such as `Context` out of the ViewModel (it outlives the UI). If the UI logic grows, put it in a plain state holder class created in the UI.
- Launch state-producing coroutines on the main dispatcher where possible and use `withContext` for background work.

Verify: write a JVM unit test that calls `onEmailChanged`/`onSubmit` with a fake repository and asserts the sequence of `ui.value` states (loading, then logged in or error); the guide notes the source of state is testable independently of the UI.

## Checked
Date: 2026-11-08. Confirmed against the Android Developers UI layer, UI state production and UI events guides: UDF definition, immutable UI state, event handling split, naming convention, state-as-event rule and `userMessageShown` pattern, channel warning, StateFlow exposure, `update`, `stateIn` with `WhileSubscribed(5_000)`, `collectAsStateWithLifecycle`, Context guidance and testability. Removed the unsupported sealed-interface advice, "previewable" claim and the lost-events-during-recreation wording.
Method: documentation only; no commands were run.
