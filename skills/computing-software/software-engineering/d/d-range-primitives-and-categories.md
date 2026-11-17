---
id: computing-software.software-engineering.d.d-range-primitives-and-categories
name: d-range-primitives-and-categories
category: computing-software
field: software-engineering
product: d
tags: [d-range-primitives-and-categories, ranges, range, input-range, forward-range, random-access-range, empty, front, popfront, save, isinputrange, d]
level: practitioner
status: docs-checked
description: "Implement input, forward, bidirectional and random-access ranges (empty, front, popFront, save, back, popBack, opIndex, length) and check them with isInputRange."
sources:
  - https://dlang.org/phobos/std_range_primitives.html
  - https://dlang.org/phobos/std_range.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Range primitives and range categories

Goal: write types that work with the whole range library.

```d
struct Count {
    int cur, end;
    bool empty() const { return cur >= end; }
    int front() const { return cur; }
    void popFront() { ++cur; }
    Count save() const { return this; }     // makes it a forward range
}
static assert(isForwardRange!Count);
```
- InputRange: `empty`, `front`, `popFront`. ForwardRange adds `save`. Bidirectional adds `back`, `popBack`. RandomAccess adds indexing and `length`.
- Checks in `std.range.primitives`: `isInputRange!R`, `isForwardRange`, `isBidirectionalRange`, `isRandomAccessRange`, `hasLength`, `hasSlicing`, `ElementType!R`.
- Arrays act as ranges through the free functions in `std.range.primitives` (`empty`, `front`, `popFront`, ...).

Verify: `static assert` the category and run `.array` on it in a unittest.

## Checked

2026-11-03. Confirmed against: std.range.primitives reference page.

Removed because the pages read did not confirm it: 'ranges are usually structs' and class-range remarks, the 'front must not advance state' gotcha, optional `opSlice` note.

Method: documentation only; no commands were run.
