---
id: computing-software.software-engineering.tauri.tauri-state-management
name: tauri-state-management
category: computing-software
field: software-engineering
product: tauri
tags: [state-management, tauri]
level: practitioner
status: docs-checked
description: "Manage shared Tauri app state with Manager::manage, wrap mutable state in a Mutex, and read it in commands or through AppHandle."
sources:
  - "https://v2.tauri.app/develop/state-management/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri state management

Goal: keep app-wide state and read or mutate it safely.

## Register state

Use the `Manager` API, for example in `setup`:

```rust
Builder::default()
  .setup(|app| {
    app.manage(AppData { welcome_message: "Welcome to Tauri!" });
    Ok(())
  })
```

Read it from any `Manager` (such as `App`): `let data = app.state::<AppData>();`

## Mutability

State is shared between threads, so wrap mutable data in interior mutability such as the standard library `Mutex`:

```rust
app.manage(Mutex::new(AppState::default()));
// later
let state = app.state::<Mutex<AppState>>();
let mut state = state.lock().unwrap();
state.counter += 1;
```

The lock is released when the `MutexGuard` is dropped.

- The standard `Mutex` is often fine, and preferred, in async code. Use an async mutex (Tokio's) mainly when you must hold the guard across await points, or for shared IO resources like a database connection.
- You do not need `Arc` for things stored in `State`; Tauri does this for you. If lifetimes stop you moving state into a thread, move a cloned `AppHandle` instead (cheap to clone) and call `state()` on it.

## Access in commands

```rust
#[tauri::command]
fn increase_counter(state: State<'_, Mutex<AppState>>) -> u32 {
  let mut state = state.lock().unwrap();
  state.counter += 1;
  state.counter
}
```

With Tokio's `Mutex`, an `async` command is written `async fn ... -> Result<u32, ()>` and uses `state.lock().await`. It must return `Result` because it takes a borrowed argument (`State<'_, T>`).

Outside commands (other threads, `on_window_event`), get an `AppHandle` (for example `window.app_handle()`) and call `app_handle.state::<Mutex<AppState>>()`.

## Mismatched types

Using the wrong type in `State<...>` (for example `State<'_, AppState>` instead of `State<'_, Mutex<AppState>>`) is not a compile error. The command fails at runtime and `invoke` rejects with a `state not managed for field ...` error; `Manager::state()` on an unmanaged type panics. A type alias such as `type AppState = Mutex<AppStateInner>;` helps, but do not wrap the alias in a `Mutex` again.

## Checked
2026-11-08. Read the Tauri v2 state-management page (tauri-docs, v2 branch) in full; claims match.
Method: documentation only; no commands were run.
