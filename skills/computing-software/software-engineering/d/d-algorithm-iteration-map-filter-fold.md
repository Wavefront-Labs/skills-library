---
id: computing-software.software-engineering.d.d-algorithm-iteration-map-filter-fold
name: d-algorithm-iteration-map-filter-fold
category: computing-software
field: software-engineering
product: d
tags: [d-algorithm-iteration-map-filter-fold, std-algorithm, map, filter, fold, reduce, joiner, splitter, uniq, group, chunkby, cumulativefold, each, d]
level: practitioner
status: draft
description: "Transform and reduce with std.algorithm.iteration: map, filter, fold (seed and tuple), sum, cumulativeFold, joiner, splitter, each, uniq, group, chunkBy, permutations."
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

# std.algorithm.iteration: map, filter, fold, reduce, joiner, splitter, uniq, group

Goal: pick the right iteration algorithm.

- `map!f`, `filter!p`, `each!f` (eager, consumes), `fold!((a,b)=>a+b)(seed)` (replaces `reduce`; seedless version takes first element), tuple folds `fold!(min, max)`, `cumulativeFold`, `sum` (pairwise accurate for floats), `mean` via `sum / n`.
- `joiner(rangeOfRanges, sep)` flattens; `splitter(range, sep)` lazy split (strings: `text.splitter(',')`); `splitWhen`, `chunkBy!pred` groups adjacent, `group(sortedRange)` gives `(value, count)` tuples, `uniq` drops adjacent duplicates, `cache`, `substitute`, `permutations`.
- Key counts: `words.array.sort.group` or an AA `++counts[w]`.
- Lambda form `(a, b) => a < b`; string form legacy.
- Combine with `std.range` (`iota`, `zip`, `take`) and `std.array.array`.

Gotchas:
- `uniq` and `group` only affect adjacent items; `sort` first.
- `map` over `immutable` strings yields `dchar`s when auto-decoding; use `.byCodeUnit` for speed when ASCII only.

Verify: unittest `assert([1,2,3,4].map!(x=>x*x).fold!"a+b" == 30);`
