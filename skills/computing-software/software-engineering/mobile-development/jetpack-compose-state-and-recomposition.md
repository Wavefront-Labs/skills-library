---
id: computing-software.software-engineering.mobile-development.jetpack-compose-state-and-recomposition
name: jetpack-compose-state-and-recomposition
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-ui, android, jetpack-compose, recomposition, state-hoisting, compose-performance]
level: practitioner
status: docs-checked
description: "Manage state in Jetpack Compose: remember vs rememberSaveable, state hoisting, ViewModel StateFlow collection, stability and skipping, and finding excess recompositions."
sources:
  - https://developer.android.com/develop/ui/compose/state
  - https://developer.android.com/develop/ui/compose/lifecycle
  - https://developer.android.com/develop/ui/compose/performance/stability
  - https://developer.android.com/develop/ui/compose/performance/bestpractices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jetpack Compose state and recomposition

**Goal:** UI that is a pure function of state, recomposes only what changed, and survives configuration changes and process death.

## 1. State holders
```kotlin
@Composable
fun SearchBar(onSearch: (String) -> Unit) {
    var query by rememberSaveable { mutableStateOf("") }      // survives rotation and process death (Bundle-able types)
    var expanded by remember { mutableStateOf(false) }         // survives recomposition only
    TextField(value = query, onValueChange = { query = it })
    Button(onClick = { onSearch(query) }) { Text("Search") }
}
```
- `remember` without keys caches across recompositions; `remember(key) { ... }` recomputes when the key changes.
- Reading a `State` inside a composable subscribes that scope to changes.
- `derivedStateOf { list.size > 10 }` when a frequently changing input should trigger fewer recompositions.

## 2. State hoisting and unidirectional data flow
Stateless composables take `value` and `onValueChange` parameters; the caller owns state. Screen-level state lives in a ViewModel:
```kotlin
class OrdersViewModel(private val repo: OrdersRepository) : ViewModel() {
    val uiState: StateFlow<OrdersUiState> = repo.orders()
        .map { OrdersUiState.Loaded(it) }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), OrdersUiState.Loading)
}

@Composable
fun OrdersRoute(vm: OrdersViewModel = hiltViewModel()) {
    val state by vm.uiState.collectAsStateWithLifecycle()   // stops collecting when not STARTED
    OrdersScreen(state, onRetry = vm::retry)
}
```
Pass state and lambdas down, events up. Do not pass the ViewModel into deep composables (hard to preview/test).

## 3. Stability and skipping
Compose skips a composable whose parameters are all **stable** and unchanged.
- Immutable: primitives such as `String`, `Int`, `Float`, and classes whose properties are all `val`s of immutable types. Types whose changes Compose is notified of (`MutableState`, `SnapshotStateList`, `SnapshotStateMap`) are stable.
- Unstable: classes with `var` properties, and classes from modules where the Compose compiler does not run.
- Fixes: **strong skipping** (default from Kotlin 2.0.20) compares unstable params by instance equality (`===`); for small flat models from other modules use a stability configuration file, or `@Stable` / `@Immutable` where `.equals()` is cheap.

## 4. Finding excess recomposition
- Defer reads: pass `() -> Float` lambdas or use the lambda versions of modifiers (`Modifier.offset { }`, `drawBehind { }`) so frequently changing state is read in layout or draw, not composition.
- `LazyColumn` items with stable `key = { it.id }`, and `contentType` for heterogeneous lists.

## Gotchas
- `mutableStateOf(list)` then `list.add(x)` does not trigger recomposition; replace the value or use `mutableStateListOf`.
- Running heavy work inside composition (sorting, formatting) repeats on every recomposition; move to the ViewModel or `remember`.
- `collectAsState()` keeps collecting in the background; prefer `collectAsStateWithLifecycle()`.

## Verify
- Rotation keeps form input, and list items are not recomposed while an unrelated field changes.

## Checked
2026-11-01. Confirmed against the Compose state, stability and performance best-practices pages: remember vs rememberSaveable (survives rotation and process death, Bundle types), collectAsStateWithLifecycle, strong skipping default from Kotlin 2.0.20 with === comparison, stability configuration file, lambda modifiers, list keys and contentType. Removed: kotlinx ImmutableList advice, stability_config.conf filename, compiler report path, Layout Inspector and effect-API sections, createComposeRule.
Method: documentation only; no commands were run.
