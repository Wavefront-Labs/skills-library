---
id: computing-software.software-engineering.nim.sets-and-bitsets
name: sets-and-bitsets
category: computing-software
field: software-engineering
product: nim
tags: [sets-and-bitsets, collections-tables-sets-options, hashset, orderedset, set, bitset, intset, union, intersection, nim]
level: practitioner
status: docs-checked
description: "Choose between HashSet and the built-in bit set[T] for membership tests and set algebra."
sources:
  - https://nim-lang.org/docs/sets.html
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/setutils.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HashSet, OrderedSet and built-in set types

Goal: model unique collections.

- `import std/sets`; `var s = initHashSet[int]()`, `s.incl 3`, `s.excl 3`, `3 in s`, `s.len`, `toHashSet([1,2,3])`.
- Algebra: `a + b` (union), `a * b` (intersection), `a - b` (difference), `a -+- b` (symmetric difference), `a <= b` (subset), `disjoint(a, b)`.
- `OrderedSet` iterates in insertion order.
- Built-in `set[T]` works only for small ordinal base types (int8-int16, uint8-uint16, `char`, enums, subranges) and is implemented as a bit vector: `var vowels = {'a','e','i','o','u'}`; `c in vowels`.
- `std/intsets` offers `IntSet`, an efficient sparse bit set of ints (listed on the library index).

Gotchas:
- `var s: set[int64]` is a compile error ("set is too large"); use `std/sets` for larger base types.

Verify: `{1,2} + {2,3}` as HashSets gives 1,2,3.

## Checked

2026-11-03. Confirmed against the sets page and manual: initHashSet, toHashSet, incl/excl, `+ * - -+-`, `<=`, disjoint, OrderedSet, the set-size limit and the `set[int64]` error. Removed: the claim that mutating while iterating is invalid and the exact 2^16 element wording (the manual limits the base type, not the element count).

Method: documentation only; no commands were run.
