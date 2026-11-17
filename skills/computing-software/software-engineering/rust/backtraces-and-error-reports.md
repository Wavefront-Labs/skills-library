---
id: computing-software.software-engineering.rust.backtraces-and-error-reports
name: backtraces-and-error-reports
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-backtrace, eyre, color-eyre, anyhow, std-backtrace, error-reporting, panic-hook, debugging, rust-debugging-diagnostics]
level: practitioner
status: verified
description: "Get useful Rust error reports: RUST_BACKTRACE and RUST_LIB_BACKTRACE, std::backtrace::Backtrace capture, anyhow backtraces, and color-eyre with span traces and sections."
sources: ["https://doc.rust-lang.org/std/backtrace/struct.Backtrace.html", "https://docs.rs/color-eyre/latest/color_eyre/", "https://docs.rs/anyhow/latest/anyhow/#details", "https://doc.rust-lang.org/std/panic/fn.set_hook.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Backtraces and error reports

**Goal:** when a Rust program fails, see where the error originated and why, not just a one-line
message.

## Environment switches
| Variable | Effect |
|---|---|
| `RUST_BACKTRACE=1` | backtrace on panics, and on captured error backtraces |
| `RUST_BACKTRACE=full` | unabridged frames |
| `RUST_LIB_BACKTRACE=1` / `0` | capture for errors (anyhow/eyre/std) independently of panics |
Capturing a backtrace is expensive (stack walk + later symbolisation), so libraries capture only
when enabled. In services, enable `RUST_LIB_BACKTRACE` only if errors are rare.

## std::backtrace (stable since 1.65)
```rust
use std::backtrace::{Backtrace, BacktraceStatus};
let bt = Backtrace::capture();           // respects the env vars
if bt.status() == BacktraceStatus::Captured { eprintln!("{bt}"); }
let always = Backtrace::force_capture(); // ignores env vars
```
Store one in your error type at creation if you need origin info in reports (thiserror treats a field of type
`std::backtrace::Backtrace` as the backtrace, but its README says using it requires a nightly compiler; the
`provide`/`request_ref` APIs for retrieving it from `dyn Error` are still unstable).

## anyhow
`anyhow::Error` captures a backtrace on creation when enabled. `{:?}` prints message, `Caused by:`
chain and backtrace; `{:#}` prints the chain on one line (good for logs). Add context at each layer:
`.with_context(|| format!("loading {path}"))?`.

## color-eyre for CLIs
```rust
use color_eyre::{eyre::WrapErr, Section};     // do not also import anyhow::Context: `.with_context` becomes ambiguous (E0034)
fn main() -> color_eyre::Result<()> {
    color_eyre::install()?;                     // installs panic and error report hooks
    let cfg = std::fs::read_to_string("cfg.toml")
        .wrap_err("reading config")
        .suggestion("create cfg.toml or pass --config")?;
    Ok(())
}
```
- Coloured backtraces with default frame filters (`HookBuilder::add_frame_filter` adds your own), sections (`.section()`, `.note()`,
  `.suggestion()`) and, with `tracing-error`'s `ErrorLayer`, a **SpanTrace** showing the tracing spans
  active when the error was created - often more useful than a backtrace in async code where stacks
  are runtime frames.
- `eyre` is the anyhow-compatible core; `color-eyre` is the reporter.

## Panic hook
```rust
std::panic::set_hook(Box::new(|info| {
    let bt = std::backtrace::Backtrace::force_capture();
    tracing::error!(panic = %info, backtrace = %bt, "panic");
}));
```
Send panics to logs/Sentry in services; `human-panic` writes a crash report file for end-user CLIs.

## Release builds
Backtraces need symbols: keep `debug = "line-tables-only"` (or `1`) in `[profile.release]` for
file:line info without full debuginfo size; `strip = true` removes them. Ship split debuginfo
(`split-debuginfo = "packed"`) and symbolicate offline if binary size matters.

## Verify
- [ ] With `RUST_BACKTRACE=1` a forced error shows frames with file:line in release builds.
- [ ] Logged errors include the full cause chain (`{:#}`), not just the top message.
- [ ] Panics in services reach the log pipeline via the hook.

## Checked
- rustc/cargo 1.99.1 (stable, Windows msvc, edition 2024), tokio 1.54.0, futures 0.3.34, rayon 1.12.0, thiserror 2.0.21, anyhow 1.0.104, color-eyre 0.6.5. Release profile with `debug = "line-tables-only"`.
- Ran the binary with env combinations: no variables gives `Backtrace::capture()` status `Disabled`; `RUST_BACKTRACE=1` or `RUST_LIB_BACKTRACE=1` gives `Captured`; `RUST_BACKTRACE=1` with `RUST_LIB_BACKTRACE=0` gives `Disabled`; `force_capture()` is `Captured` always.
- anyhow: `{:#}` prints `loading nonexistent.toml: The system cannot find the file specified. (os error 2)` on one line; `{:?}` prints message plus `Caused by:`; with `RUST_LIB_BACKTRACE=1` an `anyhow!` error prints `Stack backtrace:` and the release frame for `bt::main` shows `at ...bt.rs:16` (file:line from line tables).
- color-eyre: `install()`, `.wrap_err`, `.suggestion` printed the numbered error chain, `Location:`, a `Suggestion:` line and "Backtrace omitted. Run with RUST_BACKTRACE=1". Importing both `anyhow::Context` and `color_eyre::eyre::WrapErr` made `.with_context` ambiguous (E0034). Source: `add_frame_filter`, `add_default_filters`, `Section::{note,suggestion,section}` and the `ErrorLayer` hint exist in color-eyre 0.6.5; README describes SpanTrace capture needing tracing-error.
- The `set_hook` snippet compiled with the tracing crate; a hook calling `force_capture()` reported `Captured`. thiserror README (2.0.21): the Backtrace field needs nightly. human-panic README: writes a report file and prints its path. Cargo profiles docs list `debug = "line-tables-only"`, `strip` values none/debuginfo/symbols, and `split-debuginfo`.
