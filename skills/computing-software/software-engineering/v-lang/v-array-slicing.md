---
id: computing-software.software-engineering.v-lang.v-array-slicing
name: v-array-slicing
category: computing-software
field: software-engineering
product: v-lang
tags: [v-array-slicing, fixed-arrays-and-slices, slice, slicing, a1..3, clone, range, subarray, v-lang]
level: practitioner
status: docs-checked
description: "Slice arrays with a[start..end], open-ended and negative-index a#[..-n] forms, and know when a slice shares memory with its parent."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Slicing arrays and strings

Goal: take sub-ranges safely.

- `a[1..4]` is elements 1 to 3 (end exclusive); `a[..4]` starts at 0, `a[1..]` runs to the end. The right-side index must be greater than or equal to the left side index.
- A slice is itself an array, so every array operation works on it, e.g. `array_2 << array_1[..3]`.
- A slice always has `cap == len`, so pushing to it reallocates (copy on grow) and detaches it from the parent.
- Assigning a slice such as `a[2..4]` outside `unsafe`, when the parent or the slice is mutable, makes V insert an implicit `.clone()` and print a notice. To share memory on purpose write `mut b := unsafe { a[2..4] }`; for an explicit independent copy call `a[2..4].clone()`.
- Strings slice by byte offsets and give a string: `'Bob'[1..3] == 'ob'`.
- Negative indexes need the `#` form: `a#[-3..]` is the last three elements, `a#[..-3]` drops the last three. The result is always a valid array and may be empty (`a#[20..30]` is `[]`).

Gotchas:
- Plain `a[i]` panics when the index is out of range; use `a.last()` (same as `a[a.len - 1]`) for the final element.
- `@[direct_array_access]` on a function removes bounds checks for its array operations; only use it where indexes are verified.

Verify: `assert [0, 10, 20, 30, 40][1..4] == [10, 20, 30]`.

## Checked

Date: 2026-11-03. Confirmed in the V documentation (doc/docs.md, "Array Slices", "Slices with negative indexes", "Strings", "Memory-unsafe code" and `@[direct_array_access]`). Removed as not stated there: "a[1..3] = ..." not supported, out-of-range slice panics, string slices splitting UTF-8, the "plain negative indexes are not supported" claim (docs only say negative slices need the `#` gate), and the claim that `-prod` keeps bounds checks.

Method: documentation only; no commands were run.
