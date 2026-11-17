---
id: computing-software.software-engineering.d.d-array-conversion-and-building
name: d-array-conversion-and-building
category: computing-software
field: software-engineering
product: d
tags: [d-array-conversion-and-building, std-array, array, appender, assocarray, split, join, replicate, uninitializedarray, minimallyinitializedarray, d]
level: practitioner
status: draft
description: "Build arrays from ranges with array(), appender, assocArray, split/join, replicate, uninitializedArray and minimallyInitializedArray; know their allocation behaviour."
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

# std.array: array(), appender, assocArray, split, join, replicate, minimallyInitializedArray

Goal: materialise and assemble arrays efficiently.

- `range.array` allocates a new array (GC) from any input range; `appender!(T[])` for repeated pushes (`put`, `~=` operator form, `.data`, `.reserve(n)`, `.clear()`, `Appender!string` for text).
- `assocArray(zip(keys, values))` builds an AA; `assocArray(r)` from tuples; `uniq` + `array` removes dups after sorting.
- Splitting/joining: `"a,b".split(',')` (array of slices into the original), `split()` whitespace; `["a","b"].join(", ")`; `std.algorithm.joiner` is the lazy form.
- `replicate("ab", 3)` repeats; `array(repeat(0, n))`; `new int[](n)` zero fills; `uninitializedArray!(int[])(n)` skips init (fast, unsafe if read); `minimallyInitializedArray` init only if pointers present.
- `back`, `front`, `popFront` also exist as array primitives; `empty` tests length.

Gotchas:
- `split` returns slices of the original: free of copies but keeps the source alive.
- Do not `put` in an `Appender` copy and expect the original to see changes.

Verify: unittest `assert("a b".split == ["a","b"]);`
