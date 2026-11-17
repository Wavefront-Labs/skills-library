---
id: computing-software.software-engineering.rust.integer-overflow-wrapping-checked-saturating
name: integer-overflow-wrapping-checked-saturating
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-types-data, rust-integer-overflow, integer-overflow, wrapping, checked-arithmetic]
level: practitioner
status: docs-checked
description: "Handle Rust integer overflow deliberately: panics in debug, wrapping in release, checked_, wrapping_, saturating_ and overflowing_ methods, and profile overflow-checks."
sources:
  - https://doc.rust-lang.org/book/ch03-02-data-types.html#integer-overflow
  - https://doc.rust-lang.org/std/primitive.u32.html
  - https://doc.rust-lang.org/cargo/reference/profiles.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Integer overflow: wrapping, checked, saturating

**Goal:** arithmetic with explicit overflow semantics.

Default behaviour (The Rust Book): compiled in debug mode, overflow checks make the program **panic**; compiled with `--release`, there are no panicking checks and values wrap with two's complement (a `u8` 256 becomes 0). Relying on wrapping is considered an error. The Cargo profile setting `overflow-checks` controls the `-C overflow-checks` flag: when enabled, a panic occurs on overflow. The dev profile sets it `true` and the release profile `false` by default.

The standard library offers four families on primitive integers:

```rust
let a: u8 = 250;
a.checked_add(10);        // None
a.wrapping_add(10);       // 4   (wraps in all compilation modes)
a.saturating_add(10);     // 255 (clamps at MAX/MIN)
a.overflowing_add(10);    // (4, true): value plus overflow flag
```

Other methods to know: `checked_abs` and `unsigned_abs` for `abs()` on the minimum signed value, `checked_div`. `std::num::Wrapping<T>` and `std::num::Saturating<T>` put the wrapping or saturating intent in the type.

To keep checks in release builds (for example when handling untrusted sizes), enable them in the profile:

```toml
[profile.release]
overflow-checks = true
```

## Verify
Unit tests at the type's boundaries (`u8::MAX`, `i32::MIN`), run in both dev and release profiles to see the difference.

## Checked
2026-11-03. Confirmed against The Rust Book "Data Types: Integer Overflow" (debug panic, release two's-complement wrapping, the four `wrapping_*` / `checked_*` / `overflowing_*` / `saturating_*` families), the Cargo profiles page (`overflow-checks`, per-profile defaults) and the `i32` primitive page (`checked_abs`, `unsigned_abs`, `checked_div`, `Wrapping`/`Saturating` pages exist). Removed: `try_fold` and `try_from` examples, the `as` truncation figures and clippy lint, wasm32 and indexing remarks, shift and float claims.
Method: documentation only; no commands were run.
