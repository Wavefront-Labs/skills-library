---
id: computing-software.software-engineering.mobile-development.configuration-changes-and-viewmodel-scoping
name: configuration-changes-and-viewmodel-scoping
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, app-lifecycle, configuration-changes, viewmodel, android, rotation, viewmodelscope, savedstatehandle, compose, navigation-scoping]
level: practitioner
status: docs-checked
description: "Survive Android configuration changes with state held in ViewModel, rememberSaveable and SavedStateHandle, scope ViewModels correctly, and avoid opting out of recreation."
sources: ["https://developer.android.com/guide/topics/resources/runtime-changes", "https://developer.android.com/topic/libraries/architecture/viewmodel", "https://developer.android.com/topic/libraries/architecture/viewmodel/viewmodel-apis", "https://developer.android.com/topic/libraries/architecture/viewmodel/viewmodel-savedstate"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration changes and ViewModel scoping

**Goal:** rotation, theme or locale changes and window resizing do not lose user input,
restart network calls or leak the old Activity.

## What the platform guidance says
- Use `ViewModel` for data and business logic and `rememberSaveable` for UI-level state: both
  survive Activity recreation.
- Local persistence (a database or DataStore) handles process death for complex or large
  data. `rememberSaveable` also preserves transient UI state (user input, scroll position,
  navigation) across process death; `SavedStateHandle` does the same for ViewModel state.
  ViewModels handle configuration changes by themselves; add `SavedStateHandle` as a backup for
  system-initiated process death.
- A ViewModel stays in memory until the `ViewModelStoreOwner` it is scoped to disappears: an
  activity finishing, a navigation entry leaving the back stack, or a composable leaving the
  composition.

## Rules
1. Keep screen state and in-flight work in a `ViewModel`, expose it as `StateFlow`. The
   documented pattern combines `SavedStateHandle` with Flow:
   ```kotlin
   class SavedStateViewModel(private val savedStateHandle: SavedStateHandle) : ViewModel() {
       private val _query = savedStateHandle.getMutableStateFlow("query", "")
       val query: StateFlow<String> = _query.asStateFlow()

       val filteredData: StateFlow<List<Item>> = query
           .flatMapLatest { repository.getFilteredData(it) }
           .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

       fun setQuery(newQuery: String) { _query.value = newQuery }
   }
   ```
   `getStateFlow()` gives a read-only stream; `getMutableStateFlow()` reads and writes.
2. Use `viewModelScope` (a built-in `CoroutineScope` that follows the ViewModel lifecycle) for
   work that must outlive recreation. A custom scope can be injected for testing; cancel it in
   `onCleared()`.
3. ViewModels can outlive their owner, so they should not hold lifecycle-related APIs such as
   `Context` or `Resources`, to prevent memory leaks.

## Scoping
- `viewModel()` in a composable is scoped to the closest `ViewModelStoreOwner` from
  `LocalViewModelStoreOwner`: in order of proximity a Navigation destination or the host
  Activity. With Hilt use `hiltViewModel()` instead.
- Pass `viewModelStoreOwner` to scope to another owner. Navigation graphs are owners too, so
  `navController.getBackStackEntry("parentNavigationRoute")` gives a ViewModel shared by the
  destinations of that graph.
- `rememberViewModelStoreOwner` scopes a ViewModel to an arbitrary part of the UI (such as a
  Pager or LazyList).

## Handling changes yourself
Adding the configuration type to `android:configChanges` on the `<activity>` disables recreation
for that change; the app then must handle the change itself. The guidance: do not opt out as a
quick fix for state loss. State can still be lost through other configuration changes, process
death or closing the app, and it is impossible to disable recreation entirely. Consider
`rememberSaveable`, `ViewModel` and `LocalConfiguration` first. For Compose locale changes,
opting out means setting `locale|layoutDirection`; size-based changes use
`screenSize|smallestScreenSize|orientation|screenLayout`.

## Checked
Confirmed in the four cited Android pages: state mechanisms and process-death guidance,
ViewModel lifetime, `SavedStateHandle` flow APIs and the sample, `viewModelScope` and
`onCleared`, the context-leak warning, `viewModel()` scoping, nav-graph scoping with
`getBackStackEntry`, and the `configChanges` guidance. Removed as not stated: reasoning
for `WhileSubscribed(5000)`, the LeakCanary/developer-option checks, and activity-wide ViewModel
advice.
Method: docs-only read of cited pages, 2026-11-08
