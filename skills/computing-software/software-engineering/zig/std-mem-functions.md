---
id: computing-software.software-engineering.zig.std-mem-functions
name: std-mem-functions
category: computing-software
field: software-engineering
product: zig
tags: [zig, std-mem-functions, zig-std-mem, std-mem-eql, indexof, copyforwards, memcpy, memset]
level: practitioner
status: docs-checked
description: "Use std.mem for eql, order, indexOf, copy, set, zeroes, readInt and byte-level operations in Zig, and avoid overlap bugs."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/mem.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/meta.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/crypto/timing_safe.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std.mem comparison, search and copy
**Goal:** know the byte-level toolbox.

```zig
std.mem.eql(u8, a, b);               std.mem.order(u8, a, b);
std.mem.indexOf(u8, hay, needle);    std.mem.lastIndexOf(u8, hay, needle);
std.mem.indexOfScalar(u8, s, ' ');   std.mem.count(u8, s, "ab");
std.mem.startsWith(u8, s, "ab");     std.mem.endsWith(u8, s, "z");
@memcpy(dst[0..n], src[0..n]);       // equal lengths, no overlap
std.mem.copyForwards(u8, dst, src);  // overlap OK when dst before src
std.mem.copyBackwards(u8, dst, src); // overlap OK when dst after src
@memset(buf, 0);                     std.mem.zeroes(T);
std.mem.reverse(u8, s);              std.mem.rotate(u8, s, 2);
std.mem.min(u8, s);                  std.mem.max(u8, s);
```
- Most take `comptime T: type` first; slices are `[]const T`.
- `std.mem.Allocator` lives here, as do `alignForward` and `isAligned` for layout math. `std.mem.page_size` is not in 0.15.1; use `std.heap.page_size_min`.
- Equality on structs: `std.meta.eql(a, b)` or `std.testing.expectEqual` (not `std.mem.eql` unless slices).

## Gotchas
- `@memcpy` with overlapping slices is illegal behavior; `copyForwards`/`copyBackwards` document the direction.
- `std.mem.eql` is O(n) and not constant time; for secrets use `std.crypto.timing_safe.eql`.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `eql`, `order`, `indexOf`, `lastIndexOf`, `indexOfScalar`, `count`, `startsWith`, `endsWith`, `copyForwards`, `copyBackwards`, `zeroes`, `reverse`, `rotate`, `min`, `max`, `alignForward`, `isAligned` in mem.zig; `std.meta.eql`; `std.crypto.timing_safe.eql`; the `@memcpy`/`@memset` builtin entries in the language reference. Fixed: `std.mem.page_size` does not exist in 0.15.1.

Method: documentation only; no commands were run.

## Self-check
Shift a buffer left by two with the right copy function and assert contents.
