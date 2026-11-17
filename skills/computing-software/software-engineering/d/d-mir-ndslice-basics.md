---
id: computing-software.software-engineering.d.d-mir-ndslice-basics
name: d-mir-ndslice-basics
category: computing-software
field: software-engineering
product: d
tags: [d-mir-ndslice-basics, ecosystem-mir, mir, mir-algorithm, ndslice, slice, sliced, iota, transposed, strided, multidimensional-array, tensor, numeric-d, d]
level: practitioner
status: draft
description: "Use mir.ndslice for multidimensional arrays: slice!double, sliced, iota, transposed, reversed, strided, map/zip, diagonal, iteration with each, and lazy views."
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

# mir-algorithm ndslice: slice, iota, map, strides and views

Goal: do NumPy-style array work in D.

```d
import mir.ndslice;
auto m = slice!double(3, 4);          // 3x4 contiguous, elements start as NaN
m[] = 0;                               // fill
m[1, 2] = 5;
auto t = m.transposed;                 // view, no copy
auto r = iota(3, 4).map!(a => a * 2);  // lazy expression
auto s = [1.0, 2, 3, 4, 5, 6].sliced(2, 3);  // wrap an existing array
```
- dub: `dependency "mir-algorithm" version="~>3.x"` (confirm current major version).
- Views: `.transposed`, `.reversed`, `.strided!(dim)(k)`, `.diagonal`, `.byDim`, `.pack!n`, `.flattened`, `.dropOne`, `s[1 .. $, 0 .. 2]` slicing, `.shape`, `.strides`.
- Algorithms: `mir.ndslice.algorithm`/`topology`: `.each!`, `.map!`, `.zip`, `.reduce!`, `.field`, `iota`, `ones`, `eye`, `diagonal`; `mir.math.sum` (`sum!"fast"`), `mir.math.common` fast-math functions (`fabs`, `sqrt`, `fmuladd`).
- Interop: `.ptr` to pass to BLAS (`lubeck`, `mir-blas`), `std.range` ranges via `.byElement`.
- Memory: `slice` allocates GC; `uninitSlice`, `rcslice` (reference-counted `@nogc`).

Gotchas:
- `slice!double` initialises to NaN (double.init) unless you fill; use `uninitSlice` plus explicit fill for speed.
- Views alias memory; mutate carefully.
- Stride and layout choices affect cache performance; ldc2 -O3 recommended.

Verify: unittest with `assert(iota(2,3).transposed.shape == [3,2]);`
