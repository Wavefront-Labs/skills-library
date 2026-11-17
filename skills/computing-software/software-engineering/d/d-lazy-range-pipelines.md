---
id: computing-software.software-engineering.d.d-lazy-range-pipelines
name: d-lazy-range-pipelines
category: computing-software
field: software-engineering
product: d
tags: [d-lazy-range-pipelines, ranges, range-pipeline, lazy, map, filter, take, iota, chain, zip, ufcs-chain, array, d]
level: practitioner
status: draft
description: "Compose map, filter, take, drop, chain, zip, iota, retro, cycle, array into lazy pipelines, evaluate with array/each/sum, and avoid repeated recomputation."
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

# Lazy range pipelines with UFCS chaining

Goal: transform data without intermediate arrays.

```d
import std.algorithm, std.range, std.array;
auto evensSq = iota(1, 100).filter!(n => n % 2 == 0).map!(n => n * n).take(5).array;
```
- `map!f`, `filter!pred`, `take(n)`, `drop(n)`, `chain(a,b)`, `zip(a,b)`, `iota(a,b,step)`, `retro`, `cycle`, `stride(n)`, `chunks(n)`, `enumerate`, `tee`, `joiner`, `splitter`.
- Materialise: `.array`, `.each!`, `foreach`, `.sum`, `.fold!((a,b)=>a+b)(seed)`, `copy(range, outputRange)`.
- Lazy means each element is recomputed if you iterate twice; cache with `.array` when iterating repeatedly or the transform is costly.
- Lambda syntax: `a => a * 2`; string lambdas still work but are legacy.
- Types are long template types: use `auto`; return as `auto` or `InputRange!T` (`std.range.interfaces`) for ABI-stable signatures.

Gotchas:
- `map` result is not an array (no `.length` if the source lacks it); `.array` before indexing.
- `filter` front-eagerly evaluates the predicate on the first element at construction (calls `front` early), a source of surprise with side effects.

Verify: `assert(evensSq == [4, 16, 36, 64, 100]);`
