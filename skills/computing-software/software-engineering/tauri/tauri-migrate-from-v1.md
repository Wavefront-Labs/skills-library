---
id: computing-software.software-engineering.tauri.tauri-migrate-from-v1
name: tauri-migrate-from-v1
category: computing-software
field: software-engineering
product: tauri
tags: [migrate-from-v1, tauri]
level: advanced
status: docs-checked
description: "Upgrade a Tauri 1.0 app to 2.0: mobile-ready lib.rs, the migrate command, config key moves, module renames and the move to plugins."
sources:
  - "https://v2.tauri.app/start/migrate/from-tauri-1/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrate from Tauri 1.0 to 2.0

Goal: upgrade a v1 app. Read the whole guide even if you use the automated command.

## Prepare for mobile

1. Add to `src-tauri/Cargo.toml`: `[lib]`, `name = "app_lib"`, `crate-type = ["staticlib", "cdylib", "rlib"]`.
2. Rename `src-tauri/src/main.rs` to `lib.rs`.
3. Make the entry function `#[cfg_attr(mobile, tauri::mobile_entry_point)] pub fn run() { ... }`.
4. Recreate `main.rs` with `#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]` and `fn main() { app_lib::run(); }`.

## Automated migration

Run `npm install @tauri-apps/cli@latest` then `npm run tauri migrate` (pnpm: `pnpm update @tauri-apps/cli@latest`, `pnpm tauri migrate`; cargo: `cargo install tauri-cli --version "^2.0.0" --locked`, `cargo tauri migrate`). It is not a substitute for the guide. It also converts the v1 allowlist into a capability file.

## Key changes

- Config: `package > productName` and `version` move to the top level; add `mainBinaryName` matching `productName`; `tauri` is renamed `app`; `allowlist` is removed (use capabilities in `src-tauri/capabilities`); `build > devPath` becomes `devUrl`, `distDir` becomes `frontendDist`; `tauri > systemTray` becomes `app > trayIcon`; `tauri > updater` moves to `plugins > updater` and `bundle > createUpdaterArtifacts` must be set.
- JavaScript: `@tauri-apps/api/tauri` becomes `@tauri-apps/api/core`; the cli, clipboard, dialog, fs, global-shortcut, http, os, notification, process, shell and updater modules move to `@tauri-apps/plugin-<name>` packages; `api/window` becomes `api/webviewWindow`.
- Rust: the `api` module is removed (use plugins such as `tauri-plugin-dialog`, `tauri-plugin-shell`, `tauri-plugin-updater`; use `std::fs` for files); `Window` becomes `WebviewWindow` and `get_window` becomes `get_webview_window`; menus move to `tauri::menu` and system tray to `tauri::tray::TrayIconBuilder`; path functions move to `Manager::path`.
- Events: `emit` reaches all listeners, `emit_to`/`emitTo` targets one, `listen_global` is renamed `listen_any`.
- Environment variables: for example `TAURI_PRIVATE_KEY` becomes `TAURI_SIGNING_PRIVATE_KEY`, `TAURI_PLATFORM` becomes `TAURI_ENV_PLATFORM`, `TAURI_DEBUG` becomes `TAURI_ENV_DEBUG`.
- Windows origin: production frontends are served from `http://tauri.localhost` rather than `https`; set `app > windows > useHttpsScheme` to `true` to keep https and avoid resetting IndexedDB, LocalStorage and cookies.
- The updater's built-in dialog is gone; check and install updates with the Rust or JS APIs.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/start/migrate/from-tauri-1/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
