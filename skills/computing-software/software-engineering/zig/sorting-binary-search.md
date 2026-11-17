---
id: computing-software.software-engineering.zig.sorting-binary-search
name: sorting-binary-search
category: computing-software
field: software-engineering
product: zig
tags: [zig, sorting-binary-search, zig-std-mem, std-sort, pdq, lessthan, binarysearch]
level: practitioner
status: docs-checked
description: "Sort slices in Zig with std.mem.sort, std.sort.pdq, block and insertion sort, comparator functions, and binary search with std.sort."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/sort.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/mem.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sorting and binary search
**Goal:** sort and search with explicit comparators.

```zig
std.mem.sort(i32, items, {}, std.sort.asc(i32));       // ascending, context void
std.mem.sort(Person, people, {}, struct {
    fn lt(_: void, a: Person, b: Person) bool { return a.age < b.age; }
}.lt);
std.sort.pdq(i32, items, {}, std.sort.desc(i32));      // unstable pattern-defeating quicksort
std.sort.block(i32, items, {}, std.sort.asc(i32));     // stable block sort
const idx = std.sort.binarySearch(i32, items, @as(i32, 7), cmp);   // ?usize, cmp: fn (i32, i32) std.math.Order
```
- In 0.15.1 `std.mem.sort` calls the stable `std.sort.block`, and `std.mem.sortUnstable` calls `std.sort.pdq`; `std.sort.insertion` suits tiny slices.
- Comparator signature `fn (ctx: Context, lhs: T, rhs: T) bool` for sort. `binarySearch(T, items, context, compareFn)` takes `compareFn: fn (context, item: T) std.math.Order` (the key lives in `context`) and returns `?usize`.
- Strings: compare with `std.mem.lessThan(u8, a, b)`.
- Index-range sorting: `std.sort.pdqContext(a, b, context)` and `std.mem.sortContext(a, b, context)` (currently insertion sort) sort the index range `a..b` through a context.

## Gotchas
- Sorting `[]const T` is a type error; sort a mutable slice.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `asc`, `desc`, `pdq`, `block`, `insertion`, `binarySearch` (signature and `?usize` result), `isSorted`, `pdqContext` in sort.zig; `mem.sort` (calls `block`), `sortUnstable`, `sortContext`, `lessThan` in mem.zig. Fixed: the binary-search comparator shape was wrong (key is passed via context). Removed: the `<=` crash claim.

Method: documentation only; no commands were run.

## Self-check
Sort 1000 random ints with pdq and assert `std.sort.isSorted(i32, items, {}, std.sort.asc(i32))`.
