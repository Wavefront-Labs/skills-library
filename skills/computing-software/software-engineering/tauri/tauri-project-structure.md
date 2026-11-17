---
id: computing-software.software-engineering.tauri.tauri-project-structure
name: tauri-project-structure
category: computing-software
field: software-engineering
product: tauri
tags: [project-structure, tauri]
level: intro
status: docs-checked
description: "Understand the layout of a Tauri project: what lives in src-tauri, and why app code goes in lib.rs rather than main.rs."
sources:
  - "https://v2.tauri.app/start/project-structure/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri project structure

Goal: know which file does what, so changes go in the right place.

A Tauri project has a Rust project and an optional JavaScript project. Typically the JavaScript project is at the top level (`package.json`, `index.html`, `src/main.js`) and the Rust project is inside `src-tauri/`, a normal Cargo project with extra files:

```
src-tauri/
  Cargo.toml  Cargo.lock  build.rs  tauri.conf.json
  src/        main.rs  lib.rs
  icons/      icon.png  icon.icns  icon.ico
  capabilities/  default.json
```

- `tauri.conf.json`: main Tauri configuration, from the application identifier to the dev server URL. It also marks the Rust project for the Tauri CLI to find.
- `capabilities/`: default folder Tauri reads capability files from. You need to allow commands here to use them from JavaScript.
- `icons/`: default output directory of the `tauri icon` command, usually referenced in `tauri.conf.json > bundle > icon`.
- `build.rs`: contains `tauri_build::build()` for Tauri's build system.
- `src/lib.rs`: your Rust code and the mobile entry point, the function marked `#[cfg_attr(mobile, tauri::mobile_entry_point)]`. Code lives here because mobile builds compile the app to a library loaded through platform frameworks.
- `src/main.rs`: the desktop entry point. It runs `app_lib::run()` so desktop and mobile share one entry point. Do not modify it; modify `lib.rs`. `app_lib` corresponds to `[lib.name]` in `Cargo.toml`.

Tauri works like a static web host: compile the JavaScript project to static files first, then compile the Rust project, which bundles those files in. The JavaScript setup is therefore the same as for a static website.

For Rust-only work, remove everything else and use `src-tauri/` as the top-level project or as a member of your Rust workspace.

## Checked
2026-11-08. Read the Tauri v2 project-structure page (tauri-docs, v2 branch) in full; claims match.
Method: documentation only; no commands were run.
