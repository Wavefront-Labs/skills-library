---
id: computing-software.software-engineering.nim.sequtils-functional-helpers
name: sequtils-functional-helpers
category: computing-software
field: software-engineering
product: nim
tags: [sequtils-functional-helpers, stdlib-sequtils-algorithm, sequtils, map, filter, mapit, filterit, zip, foldl, toseq, deduplicate, any, all, nim]
level: practitioner
status: docs-checked
description: "Transform sequences functionally with map, filter, foldl, anyIt, allIt, zip, concat, toSeq and mapIt."
sources:
  - https://nim-lang.org/docs/sequtils.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sequtils: map, filter, zip and friends

Goal: transform collections concisely.

- `import std/sequtils`. `s.map(proc(x:int):int = x*2)`; template forms with implicit `it`: `s.mapIt(it * 2)`, `s.filterIt(it > 0)`, `s.anyIt(it == 3)`, `s.allIt(...)`, `s.countIt(...)`.
- `foldl(s, a + b)` (`a`, `b` implicit), `foldr`.
- Combine: `zip(a, b)`, `unzip`, `concat(a, b)`, `a & b`, `cycle`, `repeat(x, n)`, `deduplicate`, `distribute`, `toSeq(iter)`.
- In-place: `keepIf`, `apply`, `delete(s, first..last)` (the `delete(s, first, last)` form is deprecated), `insert(dest, src, pos)`.
- Index/search: `findIt`, `minIndex`, `maxIndex`.

Gotchas:
- `filter` returns a new seq; `keepIf` mutates.

Verify: `@[1,2,3].mapIt(it*it)` is @[1,4,9].

## Checked

2026-11-03. Confirmed against the sequtils page: map, mapIt, filterIt, anyIt, allIt, countIt, foldl/foldr (variables a and b), zip, unzip, concat, cycle, repeat, deduplicate, distribute, toSeq, keepIf, apply, delete, insert, minIndex, maxIndex, findIt. Removed: `find` as a sequtils proc (it is not on the page; `findIt` is), the non-deprecated claim for `delete(s, first, last)`, the claim about nested `mapIt` shadowing and the allocation advice (not on the page).

Method: documentation only; no commands were run.
