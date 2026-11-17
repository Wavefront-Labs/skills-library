---
id: computing-software.software-engineering.tauri.tauri-architecture
name: tauri-architecture
category: computing-software
field: software-engineering
product: tauri
tags: [architecture, tauri, crates, wry]
level: intro
status: docs-checked
description: "Map the Tauri crate ecosystem, tooling and upstream crates (TAO, WRY) to know which component does what."
sources:
  - "https://v2.tauri.app/concept/architecture/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri architecture

Goal: know which Tauri component owns which job. Tauri builds desktop apps from Rust plus HTML rendered in a Webview, uses the OS webview, and ships no runtime because the binary is compiled from Rust. It is not a lightweight kernel wrapper and not a VM: it uses WRY and TAO directly for OS calls.

## Core crates

- `tauri`: holds everything together. Reads `tauri.conf.json` (and the project `Cargo.toml`) at compile time, injects scripts at runtime, hosts the system-interaction API, manages updating.
- `tauri-runtime`: glue layer between Tauri and lower-level webview libraries.
- `tauri-macros`: macros for context, handler and commands, using `tauri-codegen`.
- `tauri-utils`: shared code: config parsing, platform triples, CSP injection, asset management.
- `tauri-build`: applies macros at build time for special `cargo` features.
- `tauri-codegen`: embeds, hashes and compresses assets (including icons); parses `tauri.conf.json` and generates the Config struct.
- `tauri-runtime-wry`: system-level interactions for WRY (printing, monitor detection, windowing tasks).

## Tooling

- API (JS/TS): produces `cjs` and `esm` endpoints so the Webview can call and listen to backend activity via webview message passing.
- Bundler: builds the app for the detected or given platform (macOS, Windows, Linux); usable outside Tauri projects.
- `cli.rs`: Rust CLI executable (macOS, Windows, Linux). `cli.js`: wrapper around it using `napi-rs`.
- `create-tauri-app`: scaffolds a new project with your chosen frontend framework.
- `tauri-action`: GitHub workflow that builds binaries for all platforms.
- `tauri-vscode`: Visual Studio Code enhancements.

## Upstream crates

- TAO: cross-platform window creation (Windows, macOS, Linux, iOS, Android); a fork of winit extended with menu bar and system tray.
- WRY: cross-platform WebView rendering for desktop platforms; the abstraction that decides which webview is used.

## Plugins

A plugin generally (1) enables Rust code to do something, (2) provides interface glue for integrating into an app, (3) provides a JavaScript API for the Rust code. Examples: `tauri-plugin-fs`, `tauri-plugin-sql`, `tauri-plugin-stronghold`.

Tauri is licensed MIT or Apache-2.0.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/concept/architecture/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
