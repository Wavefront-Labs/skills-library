---
id: computing-software.software-engineering.crystal.array-api
name: array-api
category: computing-software
field: software-engineering
product: crystal
tags: [array-api, stdlib-collections, array, push, pop, sort, map, select, reject, uniq, flatten, each-slice, slice, first, last, sort-by, sum, bounds, crystal]
level: intro
status: docs-checked
description: "Create and manipulate Array(T): push, pop, shift, slices, sort, map, select, uniq, flatten, sample, each_slice and bounds methods."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Array API

Goal: use Array fluently.

- Build: `[1, 2]`, `[] of String`, `Array(Int32).new(3, 0)`, `Array.new(3) { |i| i * i }`, `(1..5).to_a`.
- Access: `a[0]` raises IndexError, `a[0]?` nil, `a.fetch(9, 0)`, `a.first`, `a.last(2)`, `a[1..]`, `a[1, 2]`.
- Mutate: `<<`, `push`, `unshift`, `pop`, `shift`, `insert`, `delete`, `delete_at`, `concat`, `clear`, `compact!`, `uniq!`, `reverse!`, `shuffle!`.
- Transform: `map`, `select`, `reject`, `flat_map`, `group_by`, `partition`, `zip`, `each_cons`, `each_slice`, `sort`, `sort_by`, `min_by`, `sum`, `tally`, `reduce`, `join`.
- Equality is by value; `dup` is shallow.

Gotchas:
- `Array.new(3, [1])` fills every slot with the same inner array (no copy); use the block form `Array.new(3) { [1] }`.
- `map` on a nilable result gives `Array(T?)`; use `compact_map`.
- Mutating while iterating is unsafe.

Verify: `crystal eval 'p [3,1,2].sort'`.

## Checked

Date 2026-11-03. Confirmed Array, Indexable, Indexable::Mutable and Enumerable method names (new with size and value or block, [], []?, fetch, push/<<, pop, shift, unshift, insert, delete, delete_at, concat, compact!, uniq!, reverse!, shuffle!, map, select, reject, flat_map, group_by, partition, zip, each_cons, each_slice, sort_by, min_by, sum, tally, reduce, join, sample, flatten) in the Crystal standard library source, and the shared-value warning on Array.new(size, value). Reworded the shared-array gotcha to a compilable example.

Method: documentation only; no commands were run.
