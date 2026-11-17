---
id: computing-software.software-engineering.zig.multiarraylist-queue
name: multiarraylist-queue
category: computing-software
field: software-engineering
product: zig
tags: [zig, multiarraylist-queue, zig-std-containers, multiarraylist, priorityqueue, linkedlist, bitset, enumarray]
level: advanced
status: docs-checked
description: "Choose among Zig MultiArrayList, PriorityQueue, DoublyLinkedList, SinglyLinkedList, BitSet, EnumArray, and fifo structures for specific performance needs."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/std.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/multi_array_list.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/priority_queue.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/static_string_map.zig
  - https://ziglang.org/documentation/0.15.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MultiArrayList, PriorityQueue, linked lists, BufSet
**Goal:** know what the std offers beyond list and map.

- `std.MultiArrayList(T)`: struct-of-arrays storage for cache-friendly column scans; `list.items(.field)` returns a slice of that field; `append(alloc, struct_value)`.
- `std.PriorityQueue(T, Context, compareFn)`: binary heap; `add`, `remove`, `peek`; the comparator returns `std.math.Order`.
- `std.DoublyLinkedList` / `std.SinglyLinkedList` are intrusive: embed a `Node` field in your struct and recover the parent with `@fieldParentPtr("node", n)` (the language reference gives `@fieldParentPtr(comptime field_name, field_ptr)`).
- `std.StaticBitSet(N)`, `std.DynamicBitSet`, `std.EnumSet`, `std.EnumMap`, `std.enums.EnumArray`.
- `std.fifo`, `std.RingBuffer`, `std.Deque` and `std.BoundedArray` are not exported by 0.15.1's `std.zig`; `std.PriorityDequeue` and `std.BufSet` are.
- `std.StaticStringMap(V)` builds a perfect lookup at comptime: ideal for keyword tables.
```zig
const kw = std.StaticStringMap(Token).initComptime(.{ .{ "if", .kw_if }, .{ "else", .kw_else } });
const t = kw.get("if");
```
## Gotchas
- Intrusive lists never allocate; nodes must outlive list membership.
- `MultiArrayList` slices invalidate on growth like ArrayList.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `MultiArrayList` (`items(.field)`, `append(gpa, elem)`), `PriorityQueue(T, Context, compareFn)` with `add`/`remove`/`peek`, `StaticStringMap.initComptime`/`get`, and the std.zig exports `DoublyLinkedList`, `SinglyLinkedList`, `StaticBitSet`, `DynamicBitSet`, `EnumSet`, `EnumMap`, `EnumArray`, `BufSet`, `PriorityDequeue`; `@fieldParentPtr` signature. Fixed: fifo, RingBuffer, Deque are not in 0.15.1 std. Removed: the `ComptimeStringMap` rename claim.

Method: documentation only; no commands were run.

## Self-check
Sort 10k points by priority with `PriorityQueue` and confirm non-decreasing pops.
