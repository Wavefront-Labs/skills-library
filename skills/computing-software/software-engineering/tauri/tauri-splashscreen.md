---
id: computing-software.software-engineering.tauri.tauri-splashscreen
name: tauri-splashscreen
category: computing-software
field: software-engineering
product: tauri
tags: [splashscreen, tauri, windows, setup]
level: practitioner
status: docs-checked
description: "Implement a Tauri splashscreen as a second window that is closed, and the hidden main window shown, once frontend and backend setup tasks finish."
sources:
  - "https://v2.tauri.app/learn/splashscreen/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri splashscreen

Goal: show a window while heavy setup runs, then close it and reveal the main window.

## Method

1. Register two windows in `tauri.conf.json`: `main` created hidden, and `splashscreen` shown directly.

```json
{
    "windows": [
        { "label": "main", "visible": false },
        { "label": "splashscreen", "url": "/splashscreen" }
    ]
}
```

2. Create a page reachable at `/splashscreen` (the lab uses a `splashscreen.html` file at the project root).
3. Track setup in Rust. Add Tokio with `cargo add tokio -F time` (run in `src-tauri`). Do not write code before Tauri starts; use the `setup` hook and spawn the work as a non-blocking task:

```rust
struct SetupState { frontend_task: bool, backend_task: bool }

tauri::Builder::default()
    .manage(Mutex::new(SetupState { frontend_task: false, backend_task: false }))
    .invoke_handler(tauri::generate_handler![greet, set_complete])
    .setup(|app| {
        spawn(setup(app.handle().clone()));
        Ok(())
    })
```

4. A `set_complete(app, state, task)` command sets `frontend_task` or `backend_task`; when both are true it closes the splash and shows the main window:

```rust
let splash_window = app.get_webview_window("splashscreen").unwrap();
let main_window = app.get_webview_window("main").unwrap();
splash_window.close().unwrap();
main_window.show().unwrap();
```

The backend `setup` fn does its work (the lab fakes it with `sleep(Duration::from_secs(3)).await`) and then calls `set_complete(..., "backend")`.
5. The frontend finishes its own work on `DOMContentLoaded` and calls `invoke('set_complete', {task: 'frontend'})`.

Do not use `std::thread::sleep` in async functions: it blocks every task on that thread and freezes the app. Use the Tokio sleep.

## Whether to use one

The page calls a splashscreen an admittance of defeat that the app could not load fast enough. Often better: go straight to the main window and show a small spinner while background setup continues. A splashscreen is fine as a stylistic choice or when tasks truly must finish before the app can start.

## Checked
2026-11-08. Read the Tauri v2 splashscreen lab page (tauri-docs, v2 branch) in full; claims match.
Method: documentation only; no commands were run.
