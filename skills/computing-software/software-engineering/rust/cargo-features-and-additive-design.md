---
id: computing-software.software-engineering.rust.cargo-features-and-additive-design
name: cargo-features-and-additive-design
category: computing-software
field: software-engineering
product: rust
tags: [rust, cargo, cargo-features, optional-dependencies, conditional-compilation, cargo-hack]
level: practitioner
status: verified
description: "Design Cargo feature flags correctly: additive features, optional dependencies with dep: syntax, default features, cfg gating, docs.rs display and testing feature combinations."
sources:
  - https://doc.rust-lang.org/cargo/reference/features.html
  - https://doc.rust-lang.org/cargo/reference/features.html#feature-unification
  - https://github.com/taiki-e/cargo-hack
  - https://docs.rs/about/metadata
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cargo feature flags and additive features

**Goal:** optional functionality that compiles in every combination and never breaks a downstream build through unification.

## 1. Declaring features
```toml
[features]
default = ["std"]
std = ["serde?/std"]                 # enable serde's std only if serde is already enabled
serde = ["dep:serde"]                # explicit feature for an optional dependency
tls = ["dep:rustls", "dep:webpki-roots"]
full = ["serde", "tls"]

[dependencies]
serde = { version = "1", optional = true, default-features = false, features = ["derive"] }
rustls = { version = "0.23", optional = true }
webpki-roots = { version = "0.26", optional = true }
```
`dep:` prevents optional dependencies from creating implicit features with their own names (so `rustls` alone is not a public feature).

## 2. Using them in code
```rust
#![cfg_attr(not(feature = "std"), no_std)]

#[cfg(feature = "serde")]
impl serde::Serialize for Money { ... }

#[cfg(feature = "tls")]
pub mod tls;

#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Order { ... }
```
Docs.rs: show what needs which feature:
```toml
[package.metadata.docs.rs]
all-features = true
rustdoc-args = ["--cfg", "docsrs"]
```
```rust
#![cfg_attr(docsrs, feature(doc_cfg))]   // doc_auto_cfg was removed in Rust 1.92 (E0557 on nightly 1.101); badges now come from doc_cfg
```
Build with `RUSTDOCFLAGS="--cfg docsrs" cargo +nightly doc --all-features`; the item page shows "Available on crate feature `tls` only" (tested).

## 3. The additive rule
Cargo unifies features across the dependency graph: if any crate enables `tls`, everyone gets it. Therefore:
- Enabling a feature must only **add** API/behaviour, never remove or change it.
- No mutually exclusive features (`backend-a` vs `backend-b` that cannot coexist). If unavoidable, pick a priority at compile time and document it, or use separate crates.
- Do not use features to switch semantics (e.g. `feature = "u64-ids"` changing a type).

## 4. Default features
Consumers write `default-features = false` to opt out, but any other crate in their graph that uses defaults turns them back on. Keep defaults minimal; `std` is the common one.

## 5. Testing combinations
```bash
cargo test --no-default-features
cargo test --all-features
cargo hack check --feature-powerset --depth 2 --no-dev-deps   # combinations up to 2 features
cargo hack test --each-feature
```
Add these to CI for libraries.

## Gotchas
- `unexpected_cfgs` warns on misspelled feature names in `cfg` (Rust 1.80+ checks against declared features).
- Features of dev-dependencies leak into normal builds with resolver 1; use resolver 2+.
- Removing a feature or making it no longer enable something is a semver-breaking change.
- `cargo build --workspace` can mask a missing feature declaration in one crate (another member enables it).

## Verify
- `cargo hack check --each-feature` passes, `--no-default-features` builds, and docs.rs-style `cargo doc --all-features` shows feature badges.
