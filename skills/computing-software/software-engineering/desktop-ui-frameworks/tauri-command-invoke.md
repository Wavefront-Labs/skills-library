---
id: computing-software.software-engineering.desktop-ui-frameworks.tauri-command-invoke
name: tauri-command-invoke
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [tauri-command-invoke, tauri-commands, tauri, tauri2, rust, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Define #[tauri::command] functions, register them with generate_handler and call them from the frontend with invoke."
sources:
  - https://v2.tauri.app/develop/calling-rust/
  - https://v2.tauri.app/concept/inter-process-communication/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tauri commands with invoke

**Goal:** typed Rust calls from JS.

```rust
// AppState is your own type; State<'_, AppState> reads what .manage() registered
#[tauri::command]
async fn read_note(name: String, state: tauri::State<'_, AppState>) -> Result<String, String> {
    state.read(&name).await.map_err(|e| e.to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .manage(AppState::default())
        .invoke_handler(tauri::generate_handler![read_note])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
// JS: import { invoke } from '@tauri-apps/api/core'; await invoke('read_note', { name: 'a' });
```

**Gotcha:** JS argument keys are camelCase by default (`invokeMessage` for `invoke_message`); `#[tauri::command(rename_all = "snake_case")]` switches to snake_case. Arguments must implement `serde::Deserialize`, return values and errors `serde::Serialize`. Commands in `lib.rs` must not be `pub`; commands in a separate module must be `pub` and are listed with their path, e.g. `commands::read_note`. Async commands cannot take borrowed arguments like `&str` or `State<'_, T>` unless they return a `Result`.

## Verify
- The call returns data and an `Err` arrives as a rejected promise.

## Checked
2026-11-03. Confirmed in the Tauri Calling Rust page: `#[tauri::command]`, `generate_handler!`, `.manage` with `tauri::State`, `generate_context!()` with `.expect(...)`, `invoke` from `@tauri-apps/api/core`, camelCase keys and `rename_all`, Serialize/Deserialize requirements, `Result` rejecting the promise, the `pub` rules, and the borrowed-argument limitation for async commands. `AppState` and its `read` method are the user's own code and not from the docs. Removed: nothing beyond the original gotcha being extended.
Method: documentation only; no commands were run.
