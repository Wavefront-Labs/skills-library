---
id: computing-software.software-engineering.zig.ownership-transfer
name: ownership-transfer
category: computing-software
field: software-engineering
product: zig
tags: [zig, ownership-transfer, zig-defer, ownership, init-deinit, errdefer-ordering, toownedslice]
level: practitioner
status: docs-checked
description: "Structure Zig init and builder functions so ownership moves to the caller on success and everything is released on any error path."
sources:
  - https://ziglang.org/documentation/0.15.1/#errdefer
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/array_list.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/fs/Dir.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ownership transfer with defer and errdefer
**Goal:** no leaks, no double frees, in constructors and parsers.

Pattern: acquire, `errdefer` release, finally hand over.
```zig
pub fn load(a: std.mem.Allocator, path: []const u8) !Doc {
    const text = try std.fs.cwd().readFileAlloc(a, path, 1 << 20);
    errdefer a.free(text);
    var items: std.ArrayList(Item) = .empty;
    errdefer {
        for (items.items) |it| it.deinit(a);
        items.deinit(a);
    }
    try parse(a, text, &items);
    return .{ .text = text, .items = try items.toOwnedSlice(a) };
}
```
- In 0.15.1 `std.ArrayList(T)` is the allocator-less (unmanaged) type: start from `.empty` or `initCapacity(gpa, n)`, and pass the allocator to `deinit(gpa)` and `toOwnedSlice(gpa)`. The old managed type with `init(allocator)` is deprecated (`array_list.Managed`).
- `Dir.readFileAlloc(allocator, file_path, max_bytes)` returns a caller-owned buffer and fails with `error.FileTooBig` past `max_bytes`.
- `errdefer` runs when the function returns an error after the `errdefer` statement, including from a later `try`; `defer` always runs on scope exit.
- After success the caller owns the memory and must free it (here via a `deinit`).

## Self-check
Inject a failure at every allocation index with `std.testing.FailingAllocator` and confirm no leaks are reported.

## Checked
2026-11-02. Confirmed in the 0.15.1 language reference (errdefer) and `lib/std/array_list.zig`, `lib/std/fs/Dir.zig`, `lib/std/std.zig`.
Fixed: the old snippet used `std.ArrayList(Item).init(a)`, `items.deinit()` and `toOwnedSlice()` with no allocator, which is the pre-0.15 managed API. Removed: self-undefined-in-deinit trick, partial-array tracking advice, double-free gotcha, init mirrors deinit advice, "toOwnedSlice failing still triggers errdefers" comment.
Method: documentation only; no commands were run.
