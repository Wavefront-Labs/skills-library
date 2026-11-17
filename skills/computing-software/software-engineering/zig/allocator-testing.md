---
id: computing-software.software-engineering.zig.allocator-testing
name: allocator-testing
category: computing-software
field: software-engineering
product: zig
tags: [zig, allocator-testing, zig-memory, failing-allocator, oom-testing, allocator-parameter, arena-per-request]
level: advanced
status: docs-checked
description: "Design Zig APIs that accept allocators, use FailingAllocator to test OutOfMemory paths, and apply arena-per-request patterns."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/testing.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/testing/FailingAllocator.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/heap/arena_allocator.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Allocator-passing design and failure testing
**Goal:** make allocation failures testable and APIs predictable.

- Accept `std.mem.Allocator` as a parameter or store it in `init`; do not reach for a global allocator in libraries.
- Temporary scratch: create a local `ArenaAllocator` over the passed allocator inside the function.
- Test every error path with `std.testing.FailingAllocator`:
```zig
test "init survives OOM at every point" {
    var i: usize = 0;
    while (i < 10) : (i += 1) {
        var failing = std.testing.FailingAllocator.init(std.testing.allocator, .{ .fail_index = i });
        _ = Thing.init(failing.allocator()) catch continue;
    }
}
```
In 0.15.1 `FailingAllocator.init(allocator, config)` takes a `Config` with `fail_index` and `resize_fail_index` (both default to `maxInt(usize)`). `std.testing.checkAllAllocationFailures(backing_allocator, test_fn, extra_args)` runs a function with failure injected at each allocation.
- Pair every allocation with `errdefer` until ownership is transferred to the returned value.
- Return ownership clearly: `toOwnedSlice()` on lists transfers the buffer to the caller.

## Gotchas
- Fixed-buffer tests can pass in Debug but OOM in release if object sizes differ.
- An arena used by a long-running server grows forever unless `reset(.retain_capacity)` per request.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `FailingAllocator.init(internal_allocator, config)` and `Config.fail_index`, `checkAllAllocationFailures(backing_allocator, test_fn, extra_args)`, `std.testing.allocator`, `ArenaAllocator.reset(.retain_capacity)`. Removed: the release-drift hedges.

Method: documentation only; no commands were run.

## Self-check
Run the test above and confirm `std.testing.allocator` reports no leaks at any failure index.
