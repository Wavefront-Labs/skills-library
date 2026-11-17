---
id: computing-software.software-engineering.rust.cargo-workspaces
name: cargo-workspaces
category: computing-software
field: software-engineering
product: rust
tags: [rust, cargo, cargo-workspaces, monorepo, workspace-dependencies, resolver, rust-cargo-build]
level: practitioner
status: verified
description: "Organise multi-crate Rust projects with Cargo workspaces: virtual manifests, workspace.dependencies and lints inheritance, resolver versions, and running commands per member."
sources:
  - https://doc.rust-lang.org/cargo/reference/workspaces.html
  - https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#inheriting-a-dependency-from-a-workspace
  - https://doc.rust-lang.org/cargo/reference/resolver.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cargo workspaces

**Goal:** several crates that share one lockfile, one target directory, and centrally managed dependency versions and lints.

## 1. Virtual manifest at the root
```toml
# Cargo.toml
[workspace]
resolver = "3"                       # edition 2024 default; "2" for 2021 crates. Set it explicitly: a virtual manifest without it warns and falls back to "1" (tested, cargo 1.99.1)
members = ["crates/*", "xtask"]
exclude = ["crates/experimental"]
default-members = ["crates/app"]     # what `cargo build` builds at the root

[workspace.package]
version = "0.4.0"
edition = "2024"
license = "MIT OR Apache-2.0"
rust-version = "1.85"

[workspace.dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1.43", default-features = false }
core-types = { path = "crates/core-types", version = "0.4.0" }

[workspace.lints.rust]
unsafe_code = "forbid"
[workspace.lints.clippy]
pedantic = { level = "warn", priority = -1 }
unwrap_used = "warn"

[profile.release]
lto = "thin"
```
Profiles are only read from the workspace root.

## 2. Member manifests inherit
```toml
# crates/app/Cargo.toml
[package]
name = "app"
version.workspace = true
edition.workspace = true
license.workspace = true

[dependencies]
serde.workspace = true
tokio = { workspace = true, features = ["rt-multi-thread", "macros"] }   # features are additive to the workspace's
core-types.workspace = true

[lints]
workspace = true
```

## 3. Commands
```bash
cargo build --workspace
cargo test -p core-types
cargo run -p app -- --port 8080
cargo clippy --workspace --all-targets -- -D warnings
cargo tree -p app -e features -i serde      # who enables which serde features
cargo metadata --format-version 1 | jq '.workspace_members'
```

## 4. Feature unification
Within one build, a dependency's features are the **union** of what all members request. Building the whole workspace can enable features one member alone would not get, hiding missing `features` declarations. Check members in isolation in CI: `cargo hack check --each-feature -p <crate>` or `cargo build -p <crate>`. Resolver 2+ stops dev-dependency and build-dependency features from leaking into normal builds.

## 5. xtask pattern
A `xtask` binary crate for project automation (`cargo xtask codegen`) instead of shell scripts, with an alias in `.cargo/config.toml`:
```toml
[alias]
xtask = "run --package xtask --"
```

## Gotchas
- One `Cargo.lock` for all members: libraries published from the workspace are still resolved fresh by consumers; test with `cargo update` / `-Z minimal-versions`.
- `path` dependencies need a `version` too if the crate is published.
- Nested workspaces are not allowed; a crate under the root that is not a member errors unless `exclude`d.

## Verify
- `cargo build --workspace` and each `cargo build -p <crate>` succeed, `grep -r 'version = ' crates/*/Cargo.toml` shows no duplicated dependency versions, and lints apply in every member.
