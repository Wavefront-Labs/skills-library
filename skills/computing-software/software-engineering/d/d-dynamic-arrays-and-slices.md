---
id: computing-software.software-engineering.d.d-dynamic-arrays-and-slices
name: d-dynamic-arrays-and-slices
category: computing-software
field: software-engineering
product: d
tags: [d-dynamic-arrays-and-slices, arrays-and-slices, slice, dynamic-array, slicing, dup, bounds-check, array-literal, d]
level: practitioner
status: draft
description: "Understand D slices as pointer+length views, slicing syntax a[1..3], $ , length assignment, copying vs aliasing, .dup, and bounds checking."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dynamic arrays and slice semantics

Goal: use slices without accidental aliasing.

- A `T[]` is `{ptr, length}`; `a[1 .. 3]` makes a view, not a copy; `$` is the length inside brackets (`a[$-1]`).
- Assigning slices copies the view only; use `.dup` (mutable) or `.idup` (immutable) for a deep-enough copy, and `a[] = b[]` for element copy (lengths must match).
- Fill: `a[] = 0;`; array ops: `c[] = a[] + b[];` (vectorised element-wise).
- Appending: `a ~= x;` may reallocate and then stop aliasing the old slice; `a.length = n` grows with `.init` values.
- Bounds checks run unless `-boundscheck=off` or `-release`; failure throws `RangeError` (`core.exception`).
- Literals `[1,2,3]` are dynamic arrays; `int[3] s = [1,2,3];` static.

Gotchas:
- Two slices of the same buffer can overwrite each other when one appends past capacity-sharing.
- `a[]` with no bounds is the whole slice; `a = null` vs `a.length = 0` retains capacity differences.

Verify: unittest that mutates a slice and sees the change in the original, then `.dup`s and does not.
