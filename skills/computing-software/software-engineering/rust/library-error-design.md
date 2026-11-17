---
id: computing-software.software-engineering.rust.library-error-design
name: library-error-design
category: computing-software
field: software-engineering
product: rust
tags: [rust, non-exhaustive, error-kinds, api-design, semver, thiserror, error-handling, library-design, rust-thiserror-anyhow]
level: advanced
status: verified
description: "Design public Rust library error types that can evolve: non_exhaustive enums, opaque error structs with kind() accessors, hiding dependency errors, and semver rules."
sources: ["https://doc.rust-lang.org/reference/attributes/type_system.html#the-non_exhaustive-attribute", "https://rust-lang.github.io/api-guidelines/interoperability.html", "https://doc.rust-lang.org/std/io/struct.Error.html", "https://doc.rust-lang.org/cargo/reference/semver.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Library error design

**Goal:** errors callers can act on, that you can extend in minor releases without breaking
anyone.

## Decide what callers need to do
Callers branch on **categories** (retry? not found? bad input?), not on every internal cause. Design
the matchable surface around those decisions and keep the rest as context and `source()`.

## Option A: non_exhaustive enum
```rust
#[derive(Debug, thiserror::Error)]
#[non_exhaustive]
pub enum Error {
    #[error("object {0} not found")]
    NotFound(String),
    #[error("request timed out")]
    Timeout,
    #[error("invalid argument: {0}")]
    InvalidArgument(String),
    #[error("transport error")]
    Transport(#[source] TransportError),   // your own wrapper, not reqwest::Error directly
}
```
- `#[non_exhaustive]` forces downstream `match` to include `_`, so adding variants is a minor change.
  Inside your crate it has no effect.
- Put it on variants with fields too (`#[non_exhaustive] Timeout { after: Duration }`) so you can
  add fields; downstream must match with `..` and cannot construct it.

## Option B: opaque struct + kind (the std::io::Error model)
```rust
pub struct Error { kind: ErrorKind, inner: Box<dyn std::error::Error + Send + Sync> }

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[non_exhaustive]
pub enum ErrorKind { NotFound, Timeout, InvalidArgument, Other }

impl Error {
    pub fn kind(&self) -> ErrorKind { self.kind }
    pub fn is_retryable(&self) -> bool { matches!(self.kind, ErrorKind::Timeout) }
}
```
Best for large libraries: internals (representation, causes) can change freely; the stable contract
is `kind()`, predicate methods, Display and `source()`. Boxing keeps `Result<T, Error>` small
(clippy `result_large_err` warns at 128 bytes).

## Rules
- **Do not expose dependency error types in public variants** (`Http(reqwest::Error)`): a major
  bump of that dependency becomes a major bump of yours. Wrap them, and expose them only via
  `source()` (as `dyn Error`), which callers can still downcast.
- Keep `From<DepError> for Error` impls private-ish: a public `From` is API surface.
- Errors should be `Send + Sync + 'static`, implement `Debug`, `Display`, `Error`.
- One error type per crate is normal; per-module types are justified when operations fail in
  genuinely different ways (a parser error vs a network error).
- Document which kinds each function returns in `# Errors` rustdoc sections (clippy
  `missing_errors_doc`).

## Semver checklist
| Change | Kind |
|---|---|
| add variant to non_exhaustive enum | minor |
| add variant to exhaustive enum | **major** |
| add field to non_exhaustive variant | minor |
| change a public variant's payload type | major |
| change Display text | minor by convention (not listed in Cargo's SemVer reference; tests matching strings will break, so tell users not to) |
Run `cargo semver-checks` in CI to catch the major ones.

## Verify
- [ ] No third-party error type appears in public signatures (`cargo doc` review or `cargo public-api`).
- [ ] Public error enums are `#[non_exhaustive]` unless deliberately closed.
- [ ] `cargo semver-checks` passes.

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5, with a two-crate workspace (`libne` as a path dependency) for the non_exhaustive checks.
- Compiled Option A (thiserror enum with `#[source] TransportError`, source() returned the wrapper) and Option B (`Error { kind, inner: Box<dyn Error + Send + Sync> }`, `kind()`, `is_retryable()`); `clippy::result_large_err` stayed quiet for it.
- Downstream behaviour of `#[non_exhaustive]` confirmed: matching the enum without `_` fails; a non_exhaustive struct variant matched without `..` fails with E0638 "`..` required with variant marked as non-exhaustive"; constructing it with a struct expression fails with E0639; inside the defining crate an exhaustive match compiles (no effect).
- Cargo SemVer reference (doc.rust-lang.org/cargo/reference/semver.html, fetched): "Major: adding new enum variants", "Major: adding new fields to an enum variant" (both avoided by non_exhaustive), "Major: adding a public field when no private field exists". clippy `large-error-threshold` default 128 (clippy lint configuration doc); `missing_errors_doc` is in the pedantic group (clippy source).
- `std::io::Error` model (kind + boxed inner) is in the std docs linked in sources; `cargo semver-checks` and `cargo public-api` were not run.
