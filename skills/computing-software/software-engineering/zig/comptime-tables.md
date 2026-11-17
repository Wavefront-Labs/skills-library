---
id: computing-software.software-engineering.zig.comptime-tables
name: comptime-tables
category: computing-software
field: software-engineering
product: zig
tags: [zig, comptime-tables, zig-comptime, comptime-lookup-table, staticstringmap, embedfile, comptime-parsing]
level: advanced
status: docs-checked
description: "Generate lookup tables, perfect hashes and parsers at compile time in Zig with comptime blocks, StaticStringMap and embedded files."
sources:
  - https://ziglang.org/documentation/0.15.1/#embedFile
  - https://ziglang.org/documentation/0.15.1/#setEvalBranchQuota
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/static_string_map.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/enums.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comptime-generated tables and string maps
**Goal:** precompute data at compile time.

```zig
const crc_table = blk: {
    @setEvalBranchQuota(10_000);
    var t: [256]u32 = undefined;
    for (&t, 0..) |*e, i| {
        var c: u32 = @intCast(i);
        for (0..8) |_| c = if (c & 1 != 0) (c >> 1) ^ 0xEDB88320 else c >> 1;
        e.* = c;
    }
    break :blk t;
};
const keywords = std.StaticStringMap(Kind).initComptime(.{
    .{ "fn", .kw_fn }, .{ "const", .kw_const },
});
const data = @embedFile("assets/words.txt");
```
- `@setEvalBranchQuota` raises the comptime branch limit; the reference says the default is 1000.
- `@embedFile` embeds a file's bytes as a comptime-known value, so tables can be parsed at compile time.
- `std.StaticStringMap(V)` has `initComptime`; the old `ComptimeStringMap` name is not in 0.15.1's `std`.
- `std.enums.directEnumArray` builds enum-indexed arrays.

## Self-check
Compare the comptime table to a runtime-computed one for all 256 entries in a test.

## Checked
2026-11-02. Confirmed in the 0.15.1 language reference (`@setEvalBranchQuota` default 1000, `@embedFile`), `lib/std/static_string_map.zig` and `lib/std/enums.zig`.
Removed: read-only data placement claim, build-time generator advice, "comptime is interpreted" and float-difference gotchas, `ComptimeStringMap` as a current alias, line-count `comptime std.mem.count` line.
Method: documentation only; no commands were run.
