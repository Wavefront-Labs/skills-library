---
id: computing-software.software-engineering.v-lang.v-integer-types-and-literals
name: v-integer-types-and-literals
category: computing-software
field: software-engineering
product: v-lang
tags: [v-integer-types-and-literals, primitive-types, int, i64, u8, integer types, literals, hex, binary, usize, v-lang]
level: intro
status: docs-checked
description: "Choose among i8-i128, u8-u128, int, uint and write decimal, hex, octal and binary literals with underscores; know overflow and checking flags."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integer types and literals

Goal: pick the right integer type.

- Types: `i8 i16 i32 i64 i128` and `u8 u16 u32 u64 u128`, plus `int` and `uint`, which are platform-width (64 bits on 64-bit targets, 32 on 32-bit targets). Use `i32` or `i64` when you need a fixed width.
- `isize` and `usize` are deprecated: use `int` and `uint` (and `uint` for pointer addresses and C `size_t`).
- Literals: `123`, `0x7B`, `0b01111011`, `0o173` are all `int`; `1_000_000` underscores work in any base. Other types by casting: `i64(123)`, `u8(42)`.
- A character literal in backticks is a `rune` (alias for `u32`), not a `u8`.
- Integer arithmetic wraps on overflow, a shift by the bit width or more gives 0, and a cast to a smaller integer type keeps the low bits. `v -check-overflow` and `v -check-casts` turn these into runtime panics (code outside the standard library); `@[ignore_overflow]` exempts a function.
- `>>>` is an unsigned right shift (shown on `i128`); `>>` is arithmetic on signed values.
- Operators need the same type on both sides, so cast explicitly; integer literals may be assigned to `f32`/`f64` without a cast.
- `'42'.int()` parses a string; literals in any base are accepted (`'0xc3'.int() == 195`).
- `u8` is the byte type; `string.bytes()` gives `[]u8`.

Verify: `assert 0x7B == 123 && 0b01111011 == 123 && 0o173 == 123`.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Primitive types", "128-bit integers", "Numbers", "Checked integer arithmetic", "Strings"). Corrected or removed: "int is 32-bit" (the docs say platform width), `isize`/`usize` as the pointer-sized types (deprecated), "overflow wraps silently in release builds, debug may panic" (docs: wraps unless the opt-in flags are used), the `i64(x) + y` division and modulo sign remarks (not stated), and the old `u8(255) + 1` wrap test.

Method: documentation only; no commands were run.
