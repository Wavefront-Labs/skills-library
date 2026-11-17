---
id: computing-software.software-engineering.desktop-ui-frameworks.tauri-external-binary-sidecar
name: tauri-external-binary-sidecar
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [tauri-external-binary-sidecar, tauri-sidecar, tauri, tauri2, sidecar, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Bundle a sidecar with bundle.externalBin using target-triple suffixed files and spawn it through the shell plugin."
sources:
  - https://v2.tauri.app/develop/sidecar/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tauri sidecar external binaries

**Goal:** ship helper binaries.

```json
// src-tauri/tauri.conf.json
{ "bundle": { "externalBin": ["binaries/my-sidecar"] } }
// a file per target must exist, e.g. src-tauri/binaries/my-sidecar-x86_64-pc-windows-msvc.exe
// get the triple: rustc --print host-tuple   (Rust 1.84+; older: rustc -Vv and read the host line)
```

```rust
// needs the shell plugin set up first
use tauri_plugin_shell::ShellExt;
let sidecar_command = app.shell().sidecar("my-sidecar").unwrap().args(["arg1"]);
let (mut rx, child) = sidecar_command.spawn().expect("Failed to spawn sidecar");
```

**Gotcha:** `sidecar()` in Rust takes just the file name ("my-sidecar"), not the `externalBin` path. From JavaScript, `Command.sidecar('binaries/my-sidecar')` must match the `externalBin` string. The shell plugin needs a capability such as `{ "identifier": "shell:allow-execute", "allow": [{ "name": "binaries/my-sidecar", "sidecar": true }] }`; use `shell:allow-spawn` for `spawn()`. Arguments must also be listed in the capability (static strings, `{ "validator": "\\S+" }` regex, or `true` to allow any).

## Verify
- The bundled app runs the sidecar.

## Checked
2026-11-03. Confirmed in the Tauri sidecar page: `bundle.externalBin`, the `-$TARGET_TRIPLE` suffix requirement, `rustc --print host-tuple` (Rust 1.84) and the older `rustc -Vv` fallback, `ShellExt` with `shell().sidecar()` and `spawn()`, the name-only rule in Rust, the `Command.sidecar` string matching, the `shell:allow-execute` / `shell:allow-spawn` permissions with `name` and `sidecar: true`, and argument validators. Removed: the `grep host` line (the page gives it only as a fallback with `cut`), the "at build time" wording, and the claim that the app runs the sidecar "from the install directory" (not stated).
Method: documentation only; no commands were run.
