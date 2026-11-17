---
id: computing-software.software-engineering.nim.seq-array-operations
name: seq-array-operations
category: computing-software
field: software-engineering
product: nim
tags: [seq-array-operations, strings-and-sequences, seq, array, newseq, add, delete, insert, setlen, 2d-array, nim]
level: practitioner
status: docs-checked
description: "Create and manipulate seqs and arrays, add/delete/insert, 2D layouts, and choose between value and reference semantics."
sources:
  - https://nim-lang.org/docs/system.html
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# seq and array: dynamic and fixed collections

Goal: use the core sequence types.

- Array: fixed size: `var a: array[5, int]`, `array[0..4, int]`, `array[Color, string]`; literal `[1,2,3]`.
- Seq: dynamic: `var s = @[1,2,3]`, `newSeq[int](10)`, `newSeqOfCap[int](100)` (length zero, capacity 100), `s.add 4`, `s.insert(item, i)` (item first, then index), `s.delete(i)` (keeps order, O(n)), `s.del(i)` (moves the last item into slot i, O(1)), `s.pop()`, `s.setLen(n)`.
- 2D: `seq[seq[float]]` for ragged, flat `seq[float]` with index math for speed.

Gotchas:
- `newSeq[T](n)` creates n zeroed elements; `newSeqOfCap` creates none.

Verify: after `s.del(0)` on `@[1,2,3]`, s is `@[3,2]`.

## Checked

2026-11-03. Confirmed against the system page: newSeq (zeroed elements), newSeqOfCap (length zero), insert(x, item, i), delete (O(n), keeps order), del (O(1), takes the last item), setLen, pop. Real error fixed: `s.insert(0, at)` had the argument order backwards; the signature is `insert(x, item, i)`. Removed: stack-allocation, copy-semantics, bounds-check and loop-growth claims.

Method: documentation only; no commands were run.
