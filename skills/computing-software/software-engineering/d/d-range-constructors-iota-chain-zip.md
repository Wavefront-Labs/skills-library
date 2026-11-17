---
id: computing-software.software-engineering.d.d-range-constructors-iota-chain-zip
name: d-range-constructors-iota-chain-zip
category: computing-software
field: software-engineering
product: d
tags: [d-range-constructors-iota-chain-zip, std-range, iota, only, repeat, generate, recurrence, cycle, chain, roundrobin, zip, lockstep, enumerate, d]
level: practitioner
status: draft
description: "Create ranges with iota, only, repeat, generate, recurrence, cycle, chain, roundRobin, zip, lockstep, enumerate and refRange for lazy sequences."
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

# std.range constructors: iota, chain, zip, repeat, generate, recurrence, only

Goal: build input sequences without arrays.

- `iota(n)`, `iota(a, b)`, `iota(a, b, step)` (works with floats, but sums drift); `only(1, 2, 3)` makes a range from values; `repeat(x)` infinite or `repeat(x, n)`; `generate!(() => rand())` infinite calls; `recurrence!((a, n) => a[n-1] + a[n-2])(0, 1)` fibonacci.
- Combine: `chain(a, b)`, `roundRobin(a, b)`, `zip(a, b)` yields tuples (`StoppingPolicy.shortest|longest|requireSameLength`), `lockstep(a, b)` in `foreach (x, y; lockstep(a, b))`, `enumerate(r, start)` index pairs, `cycle(r)`.
- Wrap: `inputRangeObject(r)` / `InputRange!T` to hide types behind an interface (virtual calls).
- `refRange(&r)` shares position of a range across consumers.
- `assumeSorted(r)` enables binary search.
- Infinite ranges: `take` them before `.array`.

Gotchas:
- `zip` of unequal lengths stops at the shortest silently.
- `generate` with a delegate that captures state is not forward-copyable (`save` stops being meaningful).

Verify: unittest `assert(recurrence!((a,n)=>a[n-1]+a[n-2])(0,1).take(8).array == [0,1,1,2,3,5,8,13]);`
