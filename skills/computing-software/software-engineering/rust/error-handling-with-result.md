---
id: computing-software.software-engineering.rust.error-handling-with-result
name: error-handling-with-result
category: computing-software
field: software-engineering
product: rust
tags: [rust, error-handling, result, question-mark-operator, thiserror, anyhow, panic, unwrap, custom-error-types, error-trait, from-impl, rust-panic, rust-errors, rust-question-mark]
level: advanced
status: verified
description: "Idiomatic Rust error handling: the ? operator and From conversions, thiserror for libraries vs anyhow for applications, and when panic is actually correct."
sources: ["https://doc.rust-lang.org/book/ch09-00-error-handling.html", "https://docs.rs/thiserror/latest/thiserror/", "https://docs.rs/anyhow/latest/anyhow/", "https://rust-lang.github.io/api-guidelines/interoperability.html"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Rust error handling — Result, ?, and library vs application error types

**Goal:** propagate errors with enough context to debug, using the right crate for
whether you're writing a library (callers match on error variants) or an application
(errors mostly get logged/displayed).

## 1. The `?` operator and `From` conversion
```rust
fn read_config(path: &Path) -> Result<Config, ConfigError> {
    let text = fs::read_to_string(path)?;   // io::Error -> ConfigError via From
    let config: Config = toml::from_str(&text)?;  // toml::Error -> ConfigError via From
    Ok(config)
}
```
`?` early-returns the error, converting it via `From<E>` into the function's declared
error type. This only compiles if a `From` impl exists for every error type that can
flow through — the compiler error when it's missing ("the trait `From<io::Error>` is
not implemented for `ConfigError`") is the signal to add either a manual `impl
From<io::Error> for ConfigError` or derive it (next section).

## 2. Libraries: `thiserror` for a concrete, matchable error enum
```rust
#[derive(thiserror::Error, Debug)]
pub enum ConfigError {
    #[error("failed to read the config file")]
    Io(#[from] std::io::Error),
    #[error("invalid toml")]
    Parse(#[from] toml::de::Error),
}
```
Keep the source's own text out of `#[error("...")]` when the source is also reported: with
`{source}` or `{0}` in the message, anyhow's `Caused by:` chain prints the I/O message twice (seen in a run).
A variant that records context (the path) cannot use `#[from]`; build it with
`.map_err(|source| ConfigError::Io { path: path.into(), source })?`.
A library's public API should expose a concrete error enum so callers can
`match`/`if let` on the specific variant and react (retry on `Io`, abort on
`Parse`). `#[from]` auto-generates the `From` impl `?` needs. This is the Rust API
Guidelines' recommendation specifically because downstream crates depend on your
error type being inspectable — an opaque `anyhow::Error` return from a library forces
every caller to downcast or give up on structured handling.

## 3. Applications: `anyhow` for context-rich propagation without ceremony
```rust
fn run() -> anyhow::Result<()> {
    let config = read_config(&path)
        .context("loading configuration at startup")?;
    Ok(())
}
```
At the application's top level (a CLI, a service's main), callers usually just log
and exit — defining a dedicated enum for every possible failure site is ceremony with
no payoff. `anyhow::Error` erases the concrete type but preserves a chain of
`.context()` messages plus the original error's `Display`/source chain, which prints
as a readable multi-line explanation on failure. The rule of thumb: **thiserror in
library crates whose errors callers must match on; anyhow in binary crates/application
code that only needs to report failures.**

## 4. `.unwrap()`/`.expect()`: only when failure is actually impossible or truly fatal
```rust
let n: u32 = "42".parse().unwrap();           // fine: literal, can't fail
let config = load_config().expect("config.toml must exist at startup");  // fatal is the right behavior
```
`.expect("message")` over bare `.unwrap()` always — the message appears in the panic
and saves real debugging time. Never `.unwrap()` on a `Result`/`Option` derived from
external input (a parsed request, a file that may not exist, a network response) in
library or production-request-path code — that converts a recoverable error into a
process crash (or, inside a web handler, usually just that one request's panic,
depending on the framework's panic handling, which is still worse than a clean error
response).

## 5. When panic is actually the right tool
Panics are for invariant violations the program's logic should have prevented
(array index proven in-bounds by earlier logic but indexed unsafely anyway, a
`match` with an `unreachable!()` arm that really should be unreachable) — not for
"the user typed something we didn't expect" or "the network call failed," which are
`Result` territory. `debug_assert!` for invariants you want checked in dev/test
builds but are willing to skip in release for performance.

## Gotchas
- `Box<dyn Error>` as a quick stand-in error type works but loses the matchability of
  a concrete enum and the convenience of `anyhow`'s context chaining — it's rarely the
  best choice for either library or application code once you've seen the other two options.
- A `From` impl that "always succeeds" conversion (e.g. converting any error into a
  generic `AppError::Other(String)`) throws away the original error's type for later
  `downcast`/matching — keep the source error (`#[source]` in thiserror) even when
  wrapping into a coarser variant.
- `?` inside `main()` requires `main`'s return type to be `Result<(), E>` where `E:
  Debug` (for the default error-printing on exit) — forgetting this is a common
  first compile error when adding error handling to a quick script.

## Verify
- [ ] Library crates expose a concrete, `#[derive(thiserror::Error)]` enum; callers
      can `match` on at least the variants they're expected to handle differently.
- [ ] Application code uses `anyhow::Result` with `.context()` at each propagation
      boundary that adds useful information (which file, which request, which step).
- [ ] No `.unwrap()`/`.expect()` on a `Result`/`Option` derived from external input in
      a code path reachable by untrusted/user data.
- [ ] Every panic path is for a genuine invariant violation, confirmed by asking "can
      this input ever legitimately reach here" and answering no.

Related: computing-software.software-engineering.rust.ownership-and-borrowing

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5, toml 0.9. Compiled and ran the whole pattern: `?` converting `toml::de::Error` through `#[from]`, `.context("loading configuration at startup")` over a missing file (`{e:?}` printed the context line then `Caused by:` entries; `{e:#}` printed the chain on one line), the `map_err` path-carrying `Io { path, source }` variant, and `fn main() -> Result<(), ConfigError>` returning `Err` (stderr `Error: ...` Debug form, exit code 1).
- Corrected the original example: an `Io { path, source }` variant has no `From<io::Error>`, so `fs::read_to_string(path)?` did not fit it, and putting `{source}` in its message duplicated the text in the chain (the original `{source}` message printed the OS error twice).
- Confirmed `toml::de::Error` exists in toml 0.9; a TOML parse error prints line/column and a caret. `"42".parse().unwrap()` and `expect` ran (the `expect` panic message carries the text).
