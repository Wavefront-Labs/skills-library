---
id: computing-software.software-engineering.d.d-slice-append-capacity-assumesafeappend
name: d-slice-append-capacity-assumesafeappend
category: computing-software
field: software-engineering
product: d
tags: [d-slice-append-capacity-assumesafeappend, arrays-and-slices, capacity, reserve, assumesafeappend, appender, stomping, array-append, d]
level: advanced
status: draft
description: "Control array growth with capacity, reserve, assumeSafeAppend, Appender and understand stomping prevention when appending to shrunken slices."
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

# Append, capacity, reserve and assumeSafeAppend

Goal: append efficiently and safely.

- `~=` on a slice that ends where the GC block's used size ends extends in place; otherwise it copies. This prevents "stomping" other slices' data.
- `a.capacity` returns the number of elements it can hold without realloc (0 if it can't append in place).
- `a.reserve(n)` preallocates; `a.length = 0; a.assumeSafeAppend();` (from `object`) reuses the buffer after shrinking when you know no other slice views the tail.
- `std.array.appender!(T[])` (`Appender`) amortises appends better in hot loops; `app.put(x)`, `app.data`, `app.clear()`.
- `std.array.array(range)` materialises a range.

Gotchas:
- `assumeSafeAppend` on a slice another slice still uses leads to silent overwrites.
- Appender's `.data` slice is invalidated by further `put`.

Verify: print `.ptr` before and after `~=` in a loop to see reallocations; benchmark with Appender.
