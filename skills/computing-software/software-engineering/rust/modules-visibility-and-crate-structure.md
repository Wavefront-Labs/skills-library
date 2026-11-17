---
id: computing-software.software-engineering.rust.modules-visibility-and-crate-structure
name: modules-visibility-and-crate-structure
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-modules, pub-crate, visibility, crate-structure, re-exports, prelude, lib-rs, use-declarations, rust-modules-crates, rust-visibility]
level: practitioner
status: docs-checked
description: "Structure Rust crates with modules and visibility: file layout, pub/pub(crate)/pub(super), re-exports for a clean public API, preludes, and lib plus bin splits."
sources: ["https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html", "https://doc.rust-lang.org/reference/visibility-and-privacy.html", "https://rust-lang.github.io/api-guidelines/", "https://doc.rust-lang.org/cargo/reference/cargo-targets.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Modules, visibility and crate structure

**Goal:** a crate whose public API is small and deliberate, with internals free to change, and a
file layout others can navigate.

## File layout (2018+ style)
```
src/
  lib.rs            // crate root: mod declarations + public re-exports
  main.rs           // thin binary: parse args, call lib
  config.rs         // mod config;
  store.rs          // mod store; with submodules in store/
  store/
    postgres.rs     // mod postgres; declared inside store.rs
  bin/admin.rs      // extra binaries
tests/              // integration tests: see only the public API
```
`mod foo;` looks for `foo.rs` or `foo/mod.rs` (prefer `foo.rs` + `foo/` directory). A module exists
only if declared with `mod` somewhere; files are not auto-discovered.

## Visibility
| Modifier | Visible to |
|---|---|
| (none) | current module and its children |
| `pub(super)` | parent module |
| `pub(crate)` | whole crate, never external users |
| `pub(in crate::a::b)` | a specific ancestor path |
| `pub` | everyone who can reach the item's path |

- Default to private; use `pub(crate)` for cross-module internals. A `pub` item inside a private
  module is not reachable externally unless re-exported, but `pub(crate)` states intent and lets the
  `unreachable_pub` lint keep you honest.
- Struct fields are private independently of the struct: `pub struct Config { pub port: u16, secret: String }`.
  Private fields prevent construction with literal syntax outside the module, so you can enforce
  invariants via `new()`.
- Enum variants and their fields are public if the enum is.

## Shape the public API with re-exports
```rust
// lib.rs
mod client;
mod error;
mod internal;           // never exported
pub use client::{Client, ClientBuilder};
pub use error::{Error, Result};
pub mod prelude { pub use crate::{Client, Error, Result}; }
```
Users write `mycrate::Client`, not `mycrate::client::Client`; you can move code between files without
breaking them. `#[doc(inline)]` / `#[doc(no_inline)]` control how re-exports show in rustdoc.
Re-export dependency types that appear in your API (`pub use http;`) so users get the matching version.

## use declarations
- Group: std, external crates, then `crate::` (rustfmt `group_imports = "StdExternalCrate"`, an unstable
  option, or keep manually).
- Import types by name, functions via their module (`use std::fs; fs::read(..)`) for readability.
- `use super::*;` in `#[cfg(test)] mod tests` is idiomatic; avoid glob imports elsewhere except preludes.
- `self::`, `super::`, `crate::` for relative paths; in `pub(in path)` the path must start with `crate`, `self` or `super` (2018+).

## lib + bin split
Put logic in `lib.rs` and keep `main.rs` to argument parsing and error reporting: integration tests
and benches can then exercise the library. Large projects split into a workspace of crates; crate
boundaries are the unit of compilation parallelism and of `pub(crate)` privacy.

## Verify
- [ ] `cargo doc --open` shows only intended items at the crate root.
- [ ] `#![warn(unreachable_pub)]` (rustc lint) produces no warnings.
- [ ] `cargo-semver-checks` passes for libraries after internal moves.

## Checked

2026-10-25. Checked against the Rust Reference (visibility and privacy: `pub(in path)`, `pub(crate)`, `pub(super)`, `pub(self)`; modules: `foo.rs` or `foo/mod.rs`, not both), the rustc source for the `unreachable_pub` lint (allow-by-default, recommends `pub(crate)`), the rustfmt Configurations page (`group_imports`, `StdExternalCrate`, stable: no), the Cargo Book targets page (`src/bin/`) and the rustdoc book (`doc(inline)`). No wrong claims found; softened the import-path remark.

Method: documentation only; no commands were run.
