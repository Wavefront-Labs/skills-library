---
id: computing-software.software-engineering.d.d-opequals-opcmp-opindex-opcall
name: d-opequals-opcmp-opindex-opcall
category: computing-software
field: software-engineering
product: d
tags: [d-opequals-opcmp-opindex-opcall, operator-overloading, opequals, opcmp, opindex, opslice, opdollar, opcall, opcast, opassign, opdispatch, opindexassign, d]
level: advanced
status: docs-checked
description: "Implement equality, ordering, indexing, slicing, $, call and cast operators, plus opAssign, opDispatch and opApply, with correct const signatures and toHash."
sources:
  - https://dlang.org/spec/operatoroverloading.html
  - https://dlang.org/spec/statement.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# opEquals, opCmp, opIndex, opSlice, opDollar, opCall and opCast

Goal: complete value-type behaviour.

- Equality: `bool opEquals(const S o) const`; ordering: `int opCmp(const S o) const` returns <0, 0, >0 and drives `<`, `<=`, `>`, `>=`. Keep `opEquals`, `opCmp` and `toHash` consistent, especially for associative-array keys.
- Index: `ref T opIndex(size_t i)`, assign via `opIndexAssign(T v, size_t i)`, `opIndexOpAssign!"+"`; multi-dim `opIndex(size_t a, size_t b)`.
- Slice: `opSlice(size_t dim)(size_t lo, size_t hi)` (returns a bounds struct) with `opIndex(Bounds b)`; `opDollar(size_t dim)()` for `$`. Simple form `T[] opSlice(size_t lo, size_t hi)`.
- Call: `R opCall(Args)` makes `s(args)` work; static `opCall` constructs structs.
- Cast: `opCast(T)()` handles explicit `cast(T)`; `opCast!bool` is also used for `if (s)` and `if (!s)`.
- `opAssign(S rhs)`: custom assignment (class identity assignment cannot be overloaded); `opDispatch` forwards unknown member names.
- `opApply`/`opApplyReverse` define `foreach` / `foreach_reverse` over a struct or class.
- `in` is overloaded with `opBinary!"in"` / `opBinaryRight!"in"`; `opIn` and `opIn_r` are deprecated.

Gotchas:
- If a struct defines `opCmp` but not `opEquals`, the compiler supplies member-wise `opEquals`, which may disagree with `opCmp`; define both.
- Declaring a static `opCall` disables struct literal syntax and cannot be mixed with constructors.

Verify: unittest for each operator on a small matrix or vector type.

## Checked
Checked 2026-11-03 against the D spec Operator Overloading page (comparison, index, slice, dollar, call, cast, assignment, forwarding) and the Statements page (`opApply`). Removed: the `sort`/const claims and the class-`bool` cast remark (not on those pages); replaced `opIn_r` with the documented replacement.

Method: documentation only; no commands were run.
