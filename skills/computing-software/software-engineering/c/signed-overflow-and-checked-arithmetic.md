---
id: computing-software.software-engineering.c.signed-overflow-and-checked-arithmetic
name: signed-overflow-and-checked-arithmetic
category: computing-software
field: software-engineering
product: c
tags: [c, signed-overflow, checked-arithmetic, builtin-add-overflow, integer-overflow]
level: advanced
status: docs-checked
description: "Avoid signed overflow undefined behaviour and detect overflow before it corrupts sizes or indexes."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://wiki.sei.cmu.edu/confluence/display/c/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signed overflow and checked arithmetic

Goal: arithmetic on untrusted values that cannot silently wrap or invoke UB.

- Signed overflow is undefined; unsigned arithmetic wraps modulo 2^N.
- Check before operating: for `a + b` with `int`, test `b > 0 && a > INT_MAX - b` or `b < 0 && a < INT_MIN - b`.
- For allocation sizes, check multiplication: `if (n != 0 && size > SIZE_MAX / n) fail;` or use `__builtin_mul_overflow`.
- GCC and Clang provide `__builtin_add_overflow`, `__builtin_sub_overflow`, `__builtin_mul_overflow(a, b, &result)` returning true on overflow.
- `-fwrapv` makes signed wrap defined but hides bugs; prefer `-fsanitize=signed-integer-overflow` in testing.

Verify: build with `-fsanitize=undefined` and run tests with boundary values (`INT_MAX`, `SIZE_MAX / 2 + 1`).

## Checked

2026-11-02. Confirmed in GCC Integer Overflow Builtins and Code Gen / Instrumentation Options: `__builtin_add_overflow`, `__builtin_sub_overflow`, `__builtin_mul_overflow` (result pointer), `-fwrapv` assumes wrap-around, `-fsanitize=signed-integer-overflow`. Removed: the `x + 1 < x` folding example, `calloc` overflow claim and C23 `<stdckdint.h>` (cppreference page not found).

Method: documentation only; no commands were run.
