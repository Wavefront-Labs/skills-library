---
id: computing-software.software-engineering.v-lang.v-fixed-size-arrays
name: v-fixed-size-arrays
category: computing-software
field: software-engineering
product: v-lang
tags: [v-fixed-size-arrays, fixed-arrays-and-slices, fixed array, 4int, fixed size, stack array, array literal, v-lang]
level: practitioner
status: docs-checked
description: "Declare fixed-size arrays like [4]int{} or [1, 2, 3]!, understand their value and stack semantics, and convert them to dynamic arrays by slicing."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixed-size arrays

Goal: use arrays whose length is part of the type.

- Declare: `mut fnums := [3]int{}` (type `[3]int`), or from a literal with the `!` suffix: `[1, 10, 100]!`, equivalent to `[1, 10, 100].to_fixed_size()`.
- The length is constant: you cannot append to or shrink them, only modify elements in place. `len` is available (`fnums[0..fnums.len]`).
- Their data is on the stack, access is more efficient and they need less memory than ordinary arrays, so they suit buffers that should not heap-allocate.
- Most array methods are defined on ordinary arrays; convert first by slicing: `anums := fnums[..]` gives a `[]int`. The slice copies the data, except when it is written to (passed as `mut`, `for mut`, `sort()`, `sort_with_compare()`, `reverse_in_place()`), which updates the fixed array itself.
- `copy(mut fixed, items)` copies as many elements as both arguments have and returns that count; it works with ordinary or fixed arrays and slices of either.
- `filter` on a fixed array produces a dynamic array; `map` preserves the length.

Verify: `assert [3]int{}.len == 3`.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Fixed size arrays"). Removed as not stated there: `[3]int{init: 7}`, the compile-time error for a constant out-of-range index, struct-embedded `[64]u8` buffers and C interop remarks, and "assigning copies the whole array".

Method: documentation only; no commands were run.
