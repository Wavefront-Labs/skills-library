---
id: computing-software.software-engineering.d.d-static-arrays-and-array-operations
name: d-static-arrays-and-array-operations
category: computing-software
field: software-engineering
product: d
tags: [d-static-arrays-and-array-operations, arrays-and-slices, static-array, multidimensional-array, array-ops, vector-ops, value-type, d]
level: practitioner
status: draft
description: "Use fixed-size arrays (value types, stack storage), rectangular int[3][4] layout, slicing to dynamic, vector array ops, and the pass-by-value and ref rules."
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

# Static arrays, multidimensional arrays and array operations

Goal: choose static vs dynamic and avoid copies.

- `int[4] a;` is a value type stored inline (stack/struct); assignment and passing copy all elements; `.length` is compile-time.
- Slice it to pass cheaply: `f(a[])`. Never return a slice of a local static array (dangling; DIP1000 `-preview=dip1000` catches many cases).
- `int[3][2] m;` is 2 rows of 3 (the order reads right to left), indexed `m[row][col]`; `new int[][](r, c)` makes a jagged `int[][]`.
- Array operations: `a[] += b[]; a[] *= 2; c[] = a[] * b[] + 1;` evaluate element-wise without temporary allocations, require equal lengths and no overlapping.
- Init: `int[8] z = 0;` sets every element; `= void` leaves uninitialised.
- Compare with `==`; static arrays of different lengths do not convert.

Gotchas:
- Very large static arrays on the stack overflow it; allocate dynamic instead.
- `int[3][2]` is not `int[2][3]`; mistaking the order is common.

Verify: unittest with `static assert(typeof(m).sizeof == 24)` for int[3][2].
