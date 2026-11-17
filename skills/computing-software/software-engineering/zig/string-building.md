---
id: computing-software.software-engineering.zig.string-building
name: string-building
category: computing-software
field: software-engineering
product: zig
tags: [zig, string-building, zig-strings, splitscalar, tokenizescalar, std-mem-join, bufprint, allocprint, trim]
level: practitioner
status: docs-checked
description: "Split, tokenize, trim, join and build strings in Zig with std.mem and std.fmt, and manage the allocation of results."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/mem.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/fmt.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Splitting, trimming and building strings
**Goal:** the everyday text-manipulation recipes.

```zig
var it = std.mem.splitScalar(u8, "a,b,,c", ',');       // yields "a","b","","c"
while (it.next()) |part| { ... }
var tok = std.mem.tokenizeScalar(u8, "  a  b ", ' ');   // skips empty tokens
const t = std.mem.trim(u8, "  hi \n", " \n");           // slice, no allocation
const joined = try std.mem.join(alloc, ", ", &.{ "a", "b" });  defer alloc.free(joined);
var buf: [64]u8 = undefined;
const msg = try std.fmt.bufPrint(&buf, "{s}={d}", .{ "x", 5 });   // stack formatting
const heap = try std.fmt.allocPrint(alloc, "{s}!", .{msg});       defer alloc.free(heap);
```
- `splitSequence`, `splitAny`, `tokenizeAny`, `tokenizeSequence`, `splitBackwardsScalar`; the older `std.mem.split`/`tokenize` names do not exist in 0.15.1.
- `std.mem.replaceOwned(u8, alloc, s, from, to)`, `std.mem.concat(alloc, u8, &.{a, b})`.
- A growable builder: `std.ArrayList(u8)` (unmanaged in 0.15.1) with `appendSlice(alloc, s)`, or `std.fmt.allocPrint`.
- Parse numbers: `std.fmt.parseInt(i32, s, 10)`, `parseFloat(f64, s)` (error unions).

## Gotchas
- Iterator results alias the input; they dangle if you free the source.
- `bufPrint` returns `error.NoSpaceLeft` when the buffer is too small.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `splitScalar`/`splitSequence`/`splitAny`/`splitBackwardsScalar`, `tokenizeScalar`/`Any`/`Sequence`, `trim`, `join`, `concat`, `replaceOwned` in mem.zig; `bufPrint`, `allocPrint`, `parseInt`, `parseFloat` in fmt.zig. Fixed: the old `split`/`tokenize` names are absent from 0.15.1, not just renamed.

Method: documentation only; no commands were run.

## Self-check
Parse "k=v;k2=v2" into pairs using `splitScalar` twice and assert both pairs.
