---
id: computing-software.software-engineering.rust.documentation-with-rustdoc-and-docs-rs
name: documentation-with-rustdoc-and-docs-rs
category: computing-software
field: software-engineering
product: rust
tags: [rust, rustdoc, docs-rs, documentation, doc-comments, intra-doc-links, doc-tests, missing-docs]
level: practitioner
status: docs-checked
description: "Document Rust crates with rustdoc: doc comments and conventional sections, intra-doc links, doc tests, feature badges on docs.rs, lints and CI checks."
sources: ["https://doc.rust-lang.org/rustdoc/", "https://doc.rust-lang.org/rustdoc/write-documentation/linking-to-items-by-name.html", "https://docs.rs/about/metadata", "https://rust-lang.github.io/api-guidelines/documentation.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Documentation with rustdoc and docs.rs

**Goal:** API docs that are complete, tested, correctly linked, and render well on docs.rs with
all features visible.

## Doc comments
```rust
//! Crate-level docs at the top of lib.rs: what it is, a quick example, feature flags.

/// Parses a duration like `"1h30m"`.
///
/// # Examples
/// ```
/// # use mycrate::parse_duration;
/// let d = parse_duration("90s")?;
/// assert_eq!(d.as_secs(), 90);
/// # Ok::<(), mycrate::Error>(())
/// ```
///
/// # Errors
/// Returns [`Error::InvalidUnit`] if the unit is not one of `h`, `m`, `s`.
///
/// # Panics
/// Never panics.
pub fn parse_duration(s: &str) -> Result<Duration, Error> { .. }
```
- First line is the summary shown in lists: one sentence.
- Conventional sections: `# Examples`, `# Errors`, `# Panics`, `# Safety` (mandatory for `unsafe
  fn`). Clippy `missing_errors_doc` and `missing_panics_doc` (pedantic group) and `missing_safety_doc` (style group) enforce them.
- `#![doc = include_str!("../README.md")]` reuses the README as crate docs (and doc-tests its
  examples).

## Intra-doc links
`[`Client`]`, `[`Client::send`]`, `[`crate::config::Options`]`, `[`Vec`]`, `[text](Self::method)`.
rustdoc resolves them by path and fails loudly when they break:
```rust
#![deny(rustdoc::broken_intra_doc_links)]
```

## Doc tests
- Every ```` ``` ```` block is compiled and run by `cargo test --doc` (each as a separate crate
  using only the public API).
- Lines starting with `# ` are hidden from rendered docs but compiled (imports, setup, the
  `Ok::<(), E>(())` trick enabling `?`).
- Attributes: `no_run` (compile only), `ignore`, `should_panic`, `compile_fail`, `text` (not Rust).
- `cargo nextest` does not run doc tests (not supported by nextest), so keep a separate
  `cargo test --doc` step in CI.

## Lints
```rust
#![warn(missing_docs)]                                   // rustc lint for public items
#![warn(rustdoc::missing_crate_level_docs, rustdoc::private_intra_doc_links)]
```
```bash
RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --all-features
cargo doc --open
cargo doc --document-private-items   # internal docs for maintainers
```

## docs.rs configuration
docs.rs builds with default features unless told otherwise:
```toml
[package.metadata.docs.rs]
all-features = true
rustdoc-args = ["--cfg", "docsrs"]
targets = ["x86_64-unknown-linux-gnu"]
```
```rust
#![cfg_attr(docsrs, feature(doc_cfg))]   // badges "Available on crate feature X only"
```
(`doc_cfg` is nightly-only and now includes the automatic `cfg` badges that the separate `doc_auto_cfg` feature used to provide; docs.rs builds on nightly, so gating it on `docsrs` is the usual pattern. `#[doc(cfg(...))]` overrides the badge on a single item and `#[doc(auto_cfg = false)]` turns it off.)
Set `documentation` in Cargo.toml only if hosting elsewhere; docs.rs links automatically.
Test locally: `RUSTDOCFLAGS="--cfg docsrs" cargo +nightly doc --all-features`.

## Other
- `#[doc(hidden)]` for items public only for macro use.
- `#[doc(alias = "len")]` improves search.
- Examples in `examples/` are built by `cargo test` and scraped into docs with
  `-Zrustdoc-scrape-examples` on docs.rs (`cargo-args = ["-Zunstable-options", "-Zrustdoc-scrape-examples"]`).

## Verify
- [ ] `RUSTDOCFLAGS="-D warnings" cargo doc --all-features --no-deps` passes in CI.
- [ ] `cargo test --doc` passes.
- [ ] docs.rs build log is green after publishing; feature-gated items show badges.

## Checked

2026-10-25. Checked against the rustdoc book (unstable features: `doc_cfg` and `doc(auto_cfg)`, lints, documentation tests with `no_run`, `ignore`, `should_panic`, `compile_fail`), the docs.rs metadata crate (`all-features`, `rustdoc-args`, `targets`, `cargo-args`, `[package.metadata.docs.rs]`), Clippy lint sources (lint names and groups) and the nextest running docs (doctests unsupported). Wrong in the draft and fixed: `feature(doc_auto_cfg)`, which the rustdoc book no longer lists; the current feature is `doc_cfg`. `rustdoc::broken_intra_doc_links`, `rustdoc::missing_crate_level_docs` and `rustdoc::private_intra_doc_links` all appear in the lints page.

Method: documentation only; no commands were run.
