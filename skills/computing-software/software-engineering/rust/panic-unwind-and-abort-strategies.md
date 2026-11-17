---
id: computing-software.software-engineering.rust.panic-unwind-and-abort-strategies
name: panic-unwind-and-abort-strategies
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-errors, rust-panic-unwind, panic, unwind, abort, catch-unwind]
level: practitioner
status: docs-checked
description: "Decide when Rust code should panic, how the panic profile setting (unwind or abort) behaves, catch_unwind limits, and the std::panic hook functions."
sources:
  - https://doc.rust-lang.org/book/ch09-03-to-panic-or-not-to-panic.html
  - https://doc.rust-lang.org/std/panic/index.html
  - https://doc.rust-lang.org/std/panic/fn.catch_unwind.html
  - https://doc.rust-lang.org/cargo/reference/profiles.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Panics, unwinding and abort

**Goal:** panics for bugs and broken invariants, `Result` for expected failures.

From The Rust Book: panic when your code could end up in a bad state, meaning an assumption, guarantee, contract or invariant has been broken, the bad state is unexpected (not something like malformed user input), and later code relies on not being in it. Return `Result` when failure is expected (a parser given malformed data, a rate-limited HTTP response). `unwrap` / `expect` are appropriate in examples, prototypes and tests (a panic is how a test fails), and with `expect` when other logic guarantees an `Ok` the compiler cannot see (for example parsing a hardcoded IP address, with the reason in the message). Use the type system to avoid repeated checks.

```toml
[profile.release]
panic = "abort"      # "unwind" (stack unwound on panic) or "abort" (process terminated)
```

Cargo notes: `"unwind"` actually resolves to the target's default (NVPTX always uses abort); tests, benchmarks, build scripts and proc macros ignore the `panic` setting; when building a test with `abort`, all dependencies are forced to build with unwind.

## `std::panic`
- `catch_unwind(f)` returns `Ok(result)` or `Err(cause)` (the original panic payload). The closure must be `UnwindSafe`; `AssertUnwindSafe` asserts it when needed. It is not recommended as a general try/catch (use `Result`), may not catch all panics (it only catches unwinding panics, not ones that abort), and a custom panic hook runs before the panic is caught.
- Rust functions called from foreign code without unwinding support should be `extern "C"`, which catches the panic and aborts the process, so `catch_unwind` is not needed there; use it for more graceful handling.
- Be careful dropping an `Err` result: dropping the payload may itself panic.
- `set_hook` registers a custom panic hook (replacing the previous one), `take_hook` unregisters it and returns it, `resume_unwind` triggers a panic without invoking the hook, `panic_any` panics with a payload.

## Verify
Test the production profile as well as dev, since `panic` behaves differently when set to `abort`.

## Checked
2026-11-03. Confirmed against The Rust Book "To panic! or Not to panic!", the `std::panic` module page, the `catch_unwind` function page and the Cargo profiles `panic` section. Removed: Rust 1.81 `extern "C"` abort/`C-unwind` claims, tokio `JoinError`, mutex poisoning, panic-while-panicking, exit status 134, clippy lint names, `should_panic`, the `tracing` hook example and dependency opt-out claims, none on those pages.
Method: documentation only; no commands were run.
