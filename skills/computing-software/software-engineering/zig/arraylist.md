---
id: computing-software.software-engineering.zig.arraylist
name: arraylist
category: computing-software
field: software-engineering
product: zig
tags: [zig, arraylist, zig-std-containers, arraylist-unmanaged, append, toownedslice, std-arraylist]
level: practitioner
status: docs-checked
description: "Use std.ArrayList and ArrayListUnmanaged in Zig for growable arrays, including the 0.15 unmanaged default and toOwnedSlice."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/array_list.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/std.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ArrayList and unmanaged lists
**Goal:** growable arrays with correct ownership.

```zig
var list: std.ArrayList(u32) = .empty;            // 0.15.1: unmanaged, allocator passed per call
defer list.deinit(alloc);
try list.append(alloc, 1);
try list.appendSlice(alloc, &.{ 2, 3 });
const last = list.pop();                          // ?u32
const items = list.items;                         // slice view
const owned = try list.toOwnedSlice(alloc);       // caller frees; list is empty now
```
- In 0.15.1 `std.ArrayList` is the unmanaged variant (`.empty`, allocator per call). The allocator-storing form is `std.array_list.Managed(T)` (`init(gpa)`), and `std.ArrayListUnmanaged` is a deprecated alias of `ArrayList`. Older releases differ; check the docs for your version.
- `ensureTotalCapacity`, `appendAssumeCapacity` avoid repeated growth in hot paths; `insert`, `orderedRemove` (O(n)), `swapRemove` (O(1), reorders).
- `list.items` is invalidated by any growth.
- `std.BoundedArray` is not exported by 0.15.1's `std.zig`.

## Gotchas
- Forgetting `deinit` leaks.
- Storing `*T` into `items` then appending leaves dangling pointers; store indexes.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `ArrayList`/`Managed`/`.empty`, `pop` returning `?T`, `toOwnedSlice`, `ensureTotalCapacity`, `appendAssumeCapacity`, `orderedRemove` (documented O(N)) and `swapRemove` (documented O(1)) in array_list.zig; the `ArrayListUnmanaged` deprecation and absence of `BoundedArray` in std.zig. Removed: the claim that `deinit` after `toOwnedSlice` is safe.

Method: documentation only; no commands were run.

## Self-check
Append 1000 items, confirm `items.len`, `toOwnedSlice`, free it, and pass the leak check.
