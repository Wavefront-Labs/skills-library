---
id: computing-software.software-engineering.rust.cargo-config-toml-aliases-and-target-dir
name: cargo-config-toml-aliases-and-target-dir
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-cargo-build, rust-cargo-config, cargo-config, aliases, target-dir, rustflags]
level: practitioner
status: docs-checked
description: "Configure Cargo per user and per project with .cargo/config.toml: aliases, rustflags, linker, target-dir, env and the config hierarchy."
sources:
  - https://doc.rust-lang.org/cargo/reference/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# .cargo/config.toml, aliases and target-dir

**Goal:** share build settings without polluting `Cargo.toml` or CI scripts.

Cargo merges config files from the current directory upward, then `$CARGO_HOME/config.toml`. For a key in several files, numbers, strings and booleans take the value from the deeper directory (the home directory has the lowest priority); arrays are joined, higher-precedence items placed later. Environment variables (`CARGO_BUILD_JOBS`, `CARGO_TARGET_DIR`) take precedence over config files, and `--config KEY=VALUE` (or a path to an extra config file) takes precedence over environment variables.

```toml
# .cargo/config.toml (committed for project-wide settings)
[alias]
xtask = "run --package xtask --"
lint  = "clippy --all-targets --all-features -- -D warnings"

[build]
target-dir = "target"            # or set CARGO_TARGET_DIR to share one dir across checkouts
# rustflags = [...]              # extra flags passed to rustc

[target.x86_64-unknown-linux-gnu]
linker = "clang"

[env]
RUST_BACKTRACE = "1"

[term]
verbose = false
```

An alias value may be a string (split on spaces) or an array of strings. `target-dir` defaults to a `target` directory at the workspace root. Use `[patch]`, `[registries]` and `[source]` sections for overrides and mirrors; the Cargo reference advises preferring `[patch]` in `Cargo.toml` because config files are not usually checked in.

## Gotchas
- Rustflags come from four mutually exclusive sources and the first one set wins: `CARGO_ENCODED_RUSTFLAGS`, then `RUSTFLAGS`, then all matching `target.<triple>.rustflags` / `target.<cfg>.rustflags` entries joined together, then `build.rustflags`. A matching target section therefore hides `[build]` flags.
- Aliases are not allowed to redefine built-in commands.
- Paths in config files are relative to the parent of the directory holding the `.cargo` folder; paths from `--config KEY=VALUE` are relative to the working directory.

## Verify
`cargo lint` and `cargo xtask` run the aliases defined above.

## Checked
2026-11-03. Confirmed against the Cargo Reference "Configuration" page: merge and precedence rules, `--config` precedence, `[alias]` string/array forms and the built-in-command ban, `build.target-dir` default and `CARGO_TARGET_DIR`, `CARGO_BUILD_JOBS`, the four rustflags sources and their order, `target.<triple>.linker`, `[env]`, `[term]` `verbose`, `[patch]` advice, relative-path rules. Removed: the nextest alias, `target-cpu=native` and `-fuse-ld=lld` flags (rustc/linker behaviour, not on the page), `cargo config get`, the rebuild/cache and absolute-path claims, `cargo build -v` effect.
Method: documentation only; no commands were run.
