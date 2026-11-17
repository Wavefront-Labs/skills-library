---
id: computing-software.software-engineering.zig.threads-mutex
name: threads-mutex
category: computing-software
field: software-engineering
product: zig
tags: [zig, threads-mutex, zig-concurrency, std-thread, mutex, condition, join, thread-spawn]
level: advanced
status: docs-checked
description: "Spawn and join Zig threads with std.Thread.spawn, protect shared state with Mutex and Condition, and avoid dangling stack references."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Thread.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/heap/debug_allocator.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/heap/arena_allocator.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spawning threads, Mutex and Condition
**Goal:** run work in parallel safely.

```zig
var counter: usize = 0;
var mu = std.Thread.Mutex{};

fn work() void {
    for (0..1000) |_| {
        mu.lock();
        defer mu.unlock();
        counter += 1;
    }
}
pub fn main() !void {
    var ts: [4]std.Thread = undefined;
    for (&ts) |*t| t.* = try std.Thread.spawn(.{}, work, .{});
    for (ts) |t| t.join();
}
```
- `spawn(config, function, args_tuple)`; arguments are copied. Pass pointers deliberately and make sure the pointee outlives the thread.
- Join (`join`) or `detach` every spawned thread.
- `std.Thread.Condition`, `RwLock`, `Semaphore`, `ResetEvent`, `WaitGroup`, `Futex` and `Pool` (`pool.spawn(func, args)`) all exist in 0.15.1.
- `std.Thread.getCpuCount()` for sizing.
- Prefer message passing via a mutex-protected queue over many fine-grained locks.

## Gotchas
- Sharing a stack variable with a thread that outlives the frame is a use-after-return.
- `std.heap.DebugAllocator` (`GeneralPurposeAllocator` is an alias) has a `thread_safe` config field defaulting to `!builtin.single_threaded`; `ArenaAllocator` has no locking, so use one arena per thread.
- Never hold a mutex across blocking IO if avoidable.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `Thread.spawn(config, function, args)`, `join`, `detach`, `getCpuCount`, `Mutex`, `Condition`, `RwLock`, `Semaphore`, `ResetEvent`, `WaitGroup`, `Futex`, `Pool.spawn` in Thread.zig and Thread/; the `thread_safe` option in debug_allocator.zig and the absence of locking in arena_allocator.zig. Removed: the thread-sanitizer flag claim.

Method: documentation only; no commands were run.

## Self-check
Run the counter with 4 threads, assert 4000; remove the lock and observe lost updates in ReleaseFast.
