---
id: computing-software.software-engineering.d.d-range-adaptors-take-drop-chunks-stride
name: d-range-adaptors-take-drop-chunks-stride
category: computing-software
field: software-engineering
product: d
tags: [d-range-adaptors-take-drop-chunks-stride, std-range, take, drop, chunks, slide, stride, retro, tail, padright, takeexactly, popfrontn, adaptors, d]
level: practitioner
status: docs-checked
description: "Reshape ranges with take, takeExactly, drop, dropExactly, chunks, slide, stride, retro, tail, radial, padLeft/padRight, popFrontN and frontTransversal."
sources:
  - https://dlang.org/phobos/std_range.html
  - https://dlang.org/phobos/std_range_primitives.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std.range adaptors: take, drop, chunks, slide, stride, retro, tail, padRight

Goal: window and slice ranges lazily.

- `take(r, n)` returns at most n elements; `takeExactly`; `drop(r, n)` / `dropExactly`; `dropBack`; `popFrontN` (std.range.primitives); `tail(r, n)`.
- `chunks(r, n)` fixed-size groups; `slide(r, windowSize, stepSize = 1)` sliding windows (unlike `chunks`, it advances a configurable number of items; partial windows allowed by default via `Yes.withPartial`); `stride(r, n)` every nth element; `retro(r)` reversed view; `radial`; `padRight`, `padLeft`; `tee(r, sink)`; `walkLength(r)`.
- Ranges of ranges and parallel iteration: `lockstep`, `transposed`, `frontTransversal`.
- Primitives in `std.range.primitives`: `popFrontN`, `moveFront`, `put`.

Verify: unittest: `assert(iota(7).chunks(3).map!array.array == [[0,1,2],[3,4,5],[6]]);`

## Checked

2026-11-03. Confirmed against: std.range and std.range.primitives reference pages.

Removed because the pages read did not confirm it: the 'D 2.087+' version note, O(n) `walkLength` claim, `retro` of forward-only ranges and string-chunking gotchas, `splitter` bullet.

Method: documentation only; no commands were run.
