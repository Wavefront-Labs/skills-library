---
id: computing-software.software-engineering.zig.allocator-interface
name: allocator-interface
category: computing-software
field: software-engineering
product: zig
tags: [zig, allocator-interface, zig-memory, std-mem-allocator, alloc-free, create-destroy, dupe]
level: practitioner
status: docs-checked
description: "Use std.mem.Allocator to create, alloc, free, dupe and realloc in Zig, passing allocators explicitly and tracking ownership."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/mem/Allocator.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/array_list.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The Allocator interface and ownership
**Goal:** manage heap memory explicitly and correctly.

```zig
const a: std.mem.Allocator = ...;
const p = try a.create(Node);        defer a.destroy(p);   // single item
const buf = try a.alloc(u8, 256);    defer a.free(buf);    // slice
const copy = try a.dupe(u8, "hello"); defer a.free(copy);
const z = try a.dupeZ(u8, "c-string");
buf = try a.realloc(buf, 512);       // may move
const s = try std.fmt.allocPrint(a, "{d}-{s}", .{ 1, "x" });
```
- No hidden allocation: any function that allocates takes an allocator (or a struct that stores one). Look at the signature to know.
- Ownership rule: whoever allocates documents who frees; free with the same allocator and the exact slice length you allocated (`free` uses `slice.len`).
- Failures are `error.OutOfMemory`; handle them, do not hide with `catch unreachable` in library code.
- Use `defer`/`errdefer` immediately after each allocation.
- "Unmanaged" containers do not store the allocator and take it per call. In 0.15.1 `std.ArrayList` is unmanaged and `std.array_list.Managed` stores the allocator.

## Gotchas
- Free exactly the slice you allocated (same pointer and length), not a sub-slice such as `buf[1..]`.
- Mixing allocators: freeing `page_allocator` memory through an arena is wrong.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `create`, `destroy`, `alloc`, `free`, `realloc`, `dupe`, `dupeZ` in mem/Allocator.zig; `std.array_list.Managed` and unmanaged `ArrayList` in array_list.zig. Removed: the claim about what a sub-slice free does.

Method: documentation only; no commands were run.

## Self-check
Allocate/free under `std.testing.allocator`; deliberately skip a free and read the leak report.
