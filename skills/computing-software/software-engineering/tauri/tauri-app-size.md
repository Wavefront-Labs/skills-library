---
id: computing-software.software-engineering.tauri.tauri-app-size
name: tauri-app-size
category: computing-software
field: software-engineering
product: tauri
tags: [app-size, tauri, cargo-profile, optimization]
level: practitioner
status: docs-checked
description: "Shrink a Tauri binary with Cargo release profile settings and the removeUnusedCommands build option."
sources:
  - "https://v2.tauri.app/concept/size/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri app size optimization

Goal: push binary size lower than the already small default.

## Cargo profile (src-tauri/Cargo.toml)

Stable toolchain (recommended unless you are an advanced user):

```toml
[profile.dev]
incremental = true # Compile your binary in smaller steps.

[profile.release]
codegen-units = 1 # Allows LLVM to perform better optimization.
lto = true # Enables link-time-optimizations.
opt-level = "s" # Prioritizes small binary size. Use `3` if you prefer speed.
panic = "abort" # Higher performance by disabling panic handlers.
strip = true # Ensures debug symbols are removed.
```

Nightly adds these (dev profile also gets `rustflags = ["-Zthreads=8"]`):

```toml
trim-paths = "all" # Removes potentially privileged information from your binaries.
rustflags = ["-Cdebuginfo=0", "-Zthreads=8"] # Better compile performance.
```

`opt-level`: `3` optimizes performance, `z` size, `s` something in-between. `panic` removes panic unwinding. `strip` strips symbols or debuginfo. `rpath` hard-codes where to find dynamic libraries. `-Cdebuginfo=0` controls whether debuginfo symbols are included; `-Zthreads=8` raises compile threads.

## Remove unused commands

Set in `tauri.conf.json`:

```json
{
  "build": {
    "removeUnusedCommands": true
  }
}
```

This removes commands that are never allowed in your capability files (ACL).

- Include only the commands you use in the ACL rather than `defaults`, to maximize the benefit.
- Requires `tauri@2.4`, `tauri-build@2.1`, `tauri-plugin@2.1` and `tauri-cli@2.4`.
- It does not account for ACLs added dynamically at runtime.

How it works: `tauri-cli` tells `tauri-build` and the build scripts of `tauri` and `tauri-plugin`, through an environment variable, to generate the list of allowed commands from the ACL; the `generate_handler` macro then drops the rest. The variable is currently `REMOVE_UNUSED_COMMANDS`, set to the project directory (usually `src-tauri`). It is an implementation detail with no stability guarantee.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/concept/size/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
