---
id: computing-software.software-engineering.crystal.set-tuple-range
name: set-tuple-range
category: computing-software
field: software-engineering
product: crystal
tags: [set-tuple-range, stdlib-collections, set, tuple, namedtuple, range, step, includes, union-intersection, deque, slice, crystal]
level: intro
status: docs-checked
description: "Use Set(T) for uniqueness, Tuple and NamedTuple for fixed shapes, and Range with step, includes?, each and to_a."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Set, Tuple, NamedTuple and Range

Goal: choose the right small collection.

- `Set{1, 2}`, `s << 3`, `s.includes?(2)`, `|`, `&`, `-`, `subset_of?`.
- Tuple `{1, "a"}`: fixed size, heterogeneous, immutable, stack allocated, `t[0]` index is compile-time checked, `t.to_a` gives a union array.
- NamedTuple `{a: 1}`: `nt[:a]`, `nt.merge(b: 2)`, `to_h`, `nt.keys`.
- Range: `(1..10).step(2)`, `(1...10).includes?(10)` false, `(1..).each` endless with `break`, `('a'..'e').to_a`, `r.sum`.
- Also: `Deque(T)`, `Slice(T)` (typed view over memory), `StaticArray(T, N)`, `Bytes` = Slice(UInt8).

Gotchas:
- Tuples of different shapes are different types; do not mix in an Array without a union.
- A range with float endpoints has no `each`; use `step` (float `step(by:)`) or an integer range.

Verify: `Set{1,2} | Set{2,3}` equals `Set{1,2,3}`.

## Checked

Date 2026-11-03. Confirmed Tuple is a fixed-size, immutable, stack-allocated sequence with compile-time index and range checks (Tuple source), Set#subset_of?, NamedTuple#merge, Range#step and Range#sum, and StaticArray(T, N) in the standard library source. Removed the unconfirmed insertion-order claim for Set and the unconfirmed prelude comment.

Method: documentation only; no commands were run.
