---
id: computing-software.software-engineering.rust.conventional-std-traits
name: conventional-std-traits
category: computing-software
field: software-engineering
product: rust
tags: [rust, traits, from-into, derive-traits, display, default, tryfrom, asref, rust-api-guidelines, interoperability, rust-conversion-traits]
level: practitioner
status: verified
description: "Implement the standard traits Rust users expect: derive Debug/Clone/PartialEq/Hash/Default, From/TryFrom, Display, AsRef, FromStr, per the Rust API Guidelines."
sources: ["https://rust-lang.github.io/api-guidelines/interoperability.html", "https://doc.rust-lang.org/std/convert/index.html", "https://doc.rust-lang.org/book/appendix-03-derivable-traits.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Conventional std traits

**Goal:** types that work with `{:?}`, `?`, `HashMap`, `.into()`, `parse()` and generic
code everywhere, as the Rust API Guidelines (C-COMMON-TRAITS, C-CONV-TRAITS) expect.

## Derive eagerly (C-COMMON-TRAITS)
```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash, PartialOrd, Ord, Default)]
pub struct UserId(u64);
```
- `Debug` on every public type (required by `unwrap`, `assert_eq!`, logging).
- `Clone`, `Copy` (small plain values only; adding Copy later is fine, removing it is breaking).
- `PartialEq`/`Eq`/`Hash` together for map keys; `Eq` only if no floats.
- `Default` when there's an obvious empty value; enables `..Default::default()`.
- serde `Serialize`/`Deserialize` behind a `serde` cargo feature for libraries.

## Conversions
```rust
impl From<u64> for UserId { fn from(v: u64) -> Self { UserId(v) } }   // gives Into for free
impl TryFrom<i64> for UserId {
    type Error = InvalidId;
    fn try_from(v: i64) -> Result<Self, Self::Error> { u64::try_from(v).map(UserId).map_err(|_| InvalidId) }
}
impl FromStr for UserId { type Err = ParseIntError; fn from_str(s: &str) -> Result<Self, Self::Err> { s.parse().map(UserId) } }
```
- Implement `From`, never `Into` directly.
- `From` must be lossless and infallible; otherwise `TryFrom`.
- `From<LowerError> for MyError` makes `?` convert errors automatically.
- Accept flexible args: `fn open(path: impl AsRef<Path>)`, `fn new(name: impl Into<String>)`.

## Display vs Debug
`Display` is for end users (`to_string()` comes free); `Debug` for developers. Implement
Display for errors and user-facing values only. Don't put secrets in Debug output;
implement Debug manually to redact.

## Other expected traits
- `AsRef<str>`/`Borrow<str>` for string-like newtypes (Borrow requires Hash/Eq consistency).
- `Deref` only for smart pointers, not to fake inheritance (API guidelines C-DEREF).
- `IntoIterator` for collections; `Extend` and `FromIterator` to support `collect()`.
- `Send`/`Sync` are auto traits: check you didn't lose them (`fn assert_send<T: Send>() {}` test).

## Verify
- [ ] Every public type implements Debug (`#![warn(missing_debug_implementations)]`).
- [ ] Tests use `assert_eq!` on public types (proves PartialEq + Debug).

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5. Compiled and ran the derive set (`Debug, Clone, PartialEq, Eq, Hash, PartialOrd, Ord, Default`) as a HashMap key, `From<u64>` with `.into()`, `TryFrom<i64>` (-1 gave `Err(InvalidId)`, 3 gave `Ok`), `FromStr` through `parse::<UserId>()` (valid and invalid input), `impl AsRef<Path>` with `&str`, `String`, `PathBuf`, `impl Into<String>`, and `fn assert_send<T: Send>()`.
- Guideline ids C-COMMON-TRAITS and C-CONV-TRAITS exist on rust-lang.github.io/api-guidelines/interoperability.html (fetched); C-DEREF is on the predictability page.
- `missing_debug_implementations` accepted as a rustc lint name by `clippy-driver` (an unknown name gives "unknown lint").
