---
id: computing-software.software-engineering.zig.atomics-ordering
name: atomics-ordering
category: computing-software
field: software-engineering
product: zig
tags: [zig, atomics-ordering, zig-concurrency, std-atomic-value, fetchadd, acquire-release, cmpxchg]
level: advanced
status: docs-checked
description: "Use std.atomic.Value and the builtin atomic operations in Zig with correct memory orderings for counters, flags and lock-free structures."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/atomic.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/builtin.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Thread/Futex.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atomics and memory ordering
**Goal:** write correct lock-free primitives.

```zig
var count = std.atomic.Value(u32).init(0);
_ = count.fetchAdd(1, .monotonic);                   // counters need no ordering
const v = count.load(.acquire);
count.store(0, .release);
if (count.cmpxchgStrong(expected, new, .acq_rel, .acquire)) |actual| { /* failed, actual is current */ } else { /* succeeded */ }
var ready = std.atomic.Value(bool).init(false);
// producer: data = 1; ready.store(true, .release);
// consumer: while (!ready.load(.acquire)) std.atomic.spinLoopHint();
```
- Orderings: `.unordered`, `.monotonic`, `.acquire`, `.release`, `.acq_rel`, `.seq_cst`.
- `cmpxchgStrong` returns `null` on success, else the observed value; `cmpxchgWeak` may spuriously fail (use in loops).
- In 0.15.1 `std.atomic.Value(T)` is the atomic wrapper; `std.atomic.Atomic` does not exist.
- Builtins: `@atomicLoad`, `@atomicStore`, `@atomicRmw`, `@cmpxchgStrong`, `@cmpxchgWeak` (there is no `@fence` in the 0.15.1 language reference).
- `std.Thread.Futex.wait/wake` for blocking primitives.

## Gotchas
- Prefer `Mutex` unless profiling proves contention; lock-free code is easy to get subtly wrong.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `atomic.Value` (`init`, `load`, `store`, `fetchAdd`, `cmpxchgStrong`, `cmpxchgWeak`), `spinLoopHint`, the six `AtomicOrder` values in builtin.zig, `Futex.wait/wake`, and the atomic builtins in the language reference (`@cmpxchgStrong` returns `?T`). Fixed: `@fence` is not in the 0.15.1 language reference. Removed: ABA claim.

Method: documentation only; no commands were run.

## Self-check
Count with `fetchAdd` from 8 threads and assert the total; implement a spin-wait flag and verify under `-Doptimize=ReleaseFast`.
