---
id: computing-software.software-engineering.nim.slices-and-openarray-views
name: slices-and-openarray-views
category: computing-software
field: software-engineering
product: nim
tags: [slices-and-openarray-views, strings-and-sequences, slice, backwards-index, toopenarray, view, range-index, indexing, nim]
level: practitioner
status: docs-checked
description: "Use ranges, the ^ index, ..< and toOpenArray to process parts of sequences, arrays and strings; slices copy, views do not."
sources:
  - https://github.com/nim-lang/Nim/blob/devel/lib/system/indices.nim
  - https://github.com/nim-lang/Nim/blob/devel/lib/system.nim
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Slices, indexing operators and views

Goal: operate on sub-ranges.

- `s[2..4]` returns a copy of elements 2 through 4 inclusive (a `seq` for sequences and arrays, a `string` for strings).
- `s[2..<4]`: `a ..< b` is a shortcut for `a .. pred(b)`, so the end is excluded.
- `^x` is a backwards index: `a[^x]` is `a[a.len-x]`, so `a[^1]` is the last element. It also works in slices: `s[^3..^1]`, `s[1 .. ^2]`. `a..^b` is a shortcut for `a .. ^b`.
- Zero-copy view: `toOpenArray(s, first, last)` (last inclusive) gives a non-owning slice of a `seq`, `array`, `openArray` or `string`. Pass it to procs taking `openArray`.
- Slice assignment on an array requires equal lengths: `a[1..2] = @[99, 88]`; a different length raises `RangeDefect`. For a `seq` or `string`, a different length performs a splice instead (`s[1 .. ^2] = "xyz"` turns `"abcdefgh"` into `"axyzh"`).

Gotchas:
- The slice operator allocates a new `seq`/`string`; `toOpenArray` allocates nothing, so prefer it in hot loops.
- `toOpenArray` on a `string` gives an `openArray[char]`; `toOpenArrayByte` gives bytes.

Verify: modifying a copy made with `s[a..b]` leaves the original untouched.

## Checked

2026-11-08. Read in full: lib/system/indices.nim (BackwardsIndex, `^`, `..^`, `..<`, slice `[]` and `[]=` for strings, arrays and seqs, with their doc examples) and the `toOpenArray` / `toOpenArrayByte` declarations and doc in lib/system.nim (file searched, not read end to end). Fixed: slice assignment needs equal length only for arrays; seqs and strings splice. Removed: `system.rev` / `reversed` advice, `std/sequtils` slicing, custom `[]`/`[]=` operator advice and the seq-reallocation view gotcha (not confirmed). Manual, tutorial and lib.html dropped from sources.
Method: documentation only; no commands were run.
