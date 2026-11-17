---
id: computing-software.software-engineering.d.d-foreach-loops-and-opapply
name: d-foreach-loops-and-opapply
category: computing-software
field: software-engineering
product: d
tags: [d-foreach-loops-and-opapply, statements, foreach, foreach_reverse, opapply, ranges, loop, labelled-break, ref-foreach, d]
level: practitioner
status: docs-checked
description: "Iterate with foreach over arrays, ranges, associative arrays and tuples; foreach_reverse, ref iteration, index tracking, opApply and labelled break/continue."
sources:
  - https://dlang.org/spec/statement.html
  - https://dlang.org/spec/version.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# foreach, ranges, opApply and loop control

Goal: iterate idiomatically.

- Arrays/strings: `foreach (i, x; arr)`; `foreach (ref x; arr) x *= 2;`. Strings decode with `foreach (dchar c; s)`.
- Associative arrays: `foreach (k, v; aa)`; ranges: `foreach (x; r)` uses `empty/front/popFront`.
- Integer range: `foreach (i; 0 .. n)` (n exclusive). `foreach_reverse (i; 0 .. n)`.
- Tuples/type lists unroll at compile time: `foreach (T; AliasSeq!(int,long)) ...` (use `static foreach` for declarations).
- Custom: struct/class `opApply(scope int delegate(ref T) dg)`; return the delegate's non-zero result to honour `break`.
- `break label;` / `continue label;` leave outer loops; `Label: foreach ...`.
- `while`, `do ... while`, `for (;;)`.

Gotchas:
- `ref` lets the body modify the elements; it cannot be applied to an array index variable.
- `foreach_reverse` over an associative array is illegal, and the iteration order of `foreach` over one is unspecified.

Verify: a unittest sums `foreach (i; 1 .. 11)` and expects 55.

## Checked
Checked 2026-11-03 against the D spec Statements page (foreach over arrays, associative arrays, ranges, `opApply`, foreach ranges, sequences, ref parameters, labels). Removed: the array-length remark and the element-copy remark (not stated there).

Method: documentation only; no commands were run.
