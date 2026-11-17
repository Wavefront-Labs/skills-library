---
id: computing-software.software-engineering.tauri.tauri-calling-rust-commands
name: tauri-calling-rust-commands
category: computing-software
field: software-engineering
product: tauri
tags: [calling-rust-commands, tauri]
level: practitioner
status: docs-checked
description: "Define Tauri commands with #[tauri::command], register them, pass arguments, return data and errors, and emit events from the frontend."
sources:
  - "https://v2.tauri.app/develop/calling-rust/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calling Rust from the frontend

Goal: expose Rust functions to JavaScript with commands, or send dynamic messages with events.

## Define and register

Annotate a function with `#[tauri::command]` in `src-tauri/src/lib.rs`, then pass it to the builder:

```rust
tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![my_custom_command])
    .run(tauri::generate_context!())
```

Call it with `import { invoke } from '@tauri-apps/api/core'; invoke('my_custom_command');` (without the npm package, set `app.withGlobalTauri` to true and use `window.__TAURI__.core.invoke`).

- Command names must be unique, even across modules. In `lib.rs` commands cannot be `pub`; in a separate module they must be `pub` and listed with the module path, e.g. `commands::my_custom_command`.
- Register all commands in a single `generate_handler!` call; only the last `invoke_handler` call is used.

## Arguments, results, errors

- Arguments are a JSON object with camelCase keys: `invoke('my_custom_command', { invokeMessage: 'Hello!' })` for a Rust parameter `invoke_message`. Use `#[tauri::command(rename_all = "snake_case")]` to use snake_case keys. Argument types must implement `serde::Deserialize`; returned types must implement `serde::Serialize`.
- `invoke` returns a promise resolving to the return value. Return `Result<T, E>` to reject on `Err`; `E` must also implement `Serialize` (use `map_err(|err| err.to_string())` or a custom `thiserror` enum with a manual `serde::Serialize` impl).
- For large binary data return `tauri::ipc::Response::new(data)` to avoid JSON serialization.

## Async commands

Declare `async fn` to avoid blocking the UI. Without `async`, commands run on the main thread unless marked `#[tauri::command(async)]`. Async commands cannot take borrowed arguments such as `&str` or `State<'_, T>` directly: use an owned type (`String`), or return a `Result`.

## Injected parameters

Commands can take `tauri::WebviewWindow`, `tauri::AppHandle`, `tauri::State<T>` (state set with `.manage(...)`), `tauri::ipc::Channel<T>` for streaming, or `tauri::ipc::Request` for the raw body and headers.

## Events

Events are not type safe, always async, return nothing and carry JSON payloads. `emit('file-selected', '/path/to/file')` reaches all listeners; `emitTo('settings', 'settings-update-requested', {...})` targets one webview. Webview-targeted events do not reach normal global listeners; to hear any event pass `{ target: { kind: 'Any' } }` to `listen`.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/develop/calling-rust/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
