---
id: computing-software.software-engineering.tauri.tauri-sidecar-binaries
name: tauri-sidecar-binaries
category: computing-software
field: software-engineering
product: tauri
tags: [sidecar-binaries, tauri]
level: advanced
status: docs-checked
description: "Embed an external binary in a Tauri app with bundle.externalBin, name it per target triple, run it from Rust or JavaScript and pass arguments."
sources:
  - "https://v2.tauri.app/develop/sidecar/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embedding external binaries (sidecar)

Goal: ship an executable (for example a Python CLI built with `pyinstaller`) so users need not install dependencies.

## Configure

Add paths to `bundle.externalBin` in `src-tauri/tauri.conf.json`: `["/absolute/path/to/sidecar", "../relative/path/to/binary", "binaries/my-sidecar"]`. Relative paths are relative to `tauri.conf.json`.

Each entry needs a file with a `-$TARGET_TRIPLE` suffix at that path, for example `src-tauri/binaries/my-sidecar-x86_64-unknown-linux-gnu` or `my-sidecar-aarch64-apple-darwin`. Find your host triple with `rustc --print host-tuple` (Rust 1.84.0+; older: `rustc -Vv | grep host | cut -f2 -d' '`).

## Run from Rust

Set up the shell plugin first. Then:

```rust
use tauri_plugin_shell::ShellExt;
let sidecar_command = app.shell().sidecar("my-sidecar").unwrap();
let (mut rx, mut child) = sidecar_command.spawn().expect("Failed to spawn sidecar");
```

Read events from `rx` (for example `CommandEvent::Stdout`) and write with `child.write(...)`. `sidecar()` takes only the file name (`"my-sidecar"`), not the configured path (`binaries/my-sidecar`).

## Run from JavaScript

Grant permission in `src-tauri/capabilities/default.json`:

```json
{ "identifier": "shell:allow-execute", "allow": [{ "name": "binaries/app", "sidecar": true }] }
```

Use `shell:allow-spawn` instead (or as well) to run with `command.spawn()`. Then:

```javascript
import { Command } from '@tauri-apps/plugin-shell';
const output = await Command.sidecar('binaries/my-sidecar').execute();
```

The string must match an `externalBin` entry.

## Arguments

In the capability entry, `args` can be `true` (allow any), `false` (none), or an ordered list mixing static strings and dynamic validators:

```json
"args": ["arg1", "-a", "--arg2", { "validator": "\\S+" }]
```

Callers then pass all arguments in that exact order, in Rust with `.args([...])` or in JavaScript as the second parameter of `Command.sidecar(name, [...])`. The `migrate` command handles this for v1 apps.

## Checked

Checked 2026-11-08 against the Tauri v2 sidecar page: externalBin paths and relativity, target-triple suffix naming, rustc --print host-tuple (Rust 1.84.0) and fallback, Rust sidecar() name rule, shell:allow-execute versus shell:allow-spawn, Command.sidecar, args true/false/list with validator, and the migrate note. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
