---
id: computing-software.software-engineering.tauri.tauri-debug-application
name: tauri-debug-application
category: computing-software
field: software-engineering
product: tauri
tags: [debug-application, tauri, debugging, devtools]
level: practitioner
status: docs-checked
description: "Debug a Tauri app using dev-only code checks, the Rust console, the WebView inspector, debug builds and the devtools Cargo feature."
sources:
  - "https://v2.tauri.app/develop/debug/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debug a Tauri application

Goal: find errors across the Rust core and the WebView, and keep debug code out of production.

## Development-only code (Rust)

- `tauri::is_dev()` returns a bool: whether the instance was started with `tauri dev`. `cfg!(dev)` and `#[cfg(dev)]` do the same at compile time.
- `cfg!(debug_assertions)` / `#[cfg(debug_assertions)]` is true for `tauri dev` and `tauri build --debug`.

## Rust console

Errors and `println!` output appear in the terminal where you ran `tauri dev`. If it crashes, rerun with a backtrace:

- Linux/macOS: `RUST_BACKTRACE=1 tauri dev`
- Windows PowerShell: `$env:RUST_BACKTRACE=1` then `tauri dev`

## WebView console

Right-click and choose `Inspect Element`, or press `Ctrl + Shift + i` (Linux, Windows) or `Command + Option + i` (macOS). The inspector is platform-specific: WebKitGTK WebInspector on Linux, Safari's inspector on macOS, Microsoft Edge DevTools on Windows.

Open or close it from Rust with `WebviewWindow::open_devtools` and `close_devtools`, e.g. inside `.setup(|app| ...)` under `#[cfg(debug_assertions)]`, using `app.get_webview_window("main")`.

## Inspector in production

By default the inspector is only enabled in development and debug builds.

1. Build a debug bundle: `tauri build --debug` (for example `npm run tauri build -- --debug`). Output goes to `src-tauri/target/debug/bundle`.
2. To get devtools in production builds, enable the `devtools` Cargo feature in `src-tauri/Cargo.toml`: `tauri = { version = "...", features = ["...", "devtools"] }`.

The devtools API is private on macOS, and using private APIs prevents App Store acceptance.

You can also run the built executable from `src-tauri/target/(release|debug)/[app name]` in a terminal to see compiler notes and `println` messages; double-clicking it closes the console on errors.

## Core process

The Core process is Rust, so GDB or LLDB can debug it; the "Debugging in VS Code" guide covers the LLDB extension.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/develop/debug/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
