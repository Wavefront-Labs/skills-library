---
id: computing-software.software-engineering.d.d-shared-atomic-and-synchronized
name: d-shared-atomic-and-synchronized
category: computing-software
field: software-engineering
product: d
tags: [d-shared-atomic-and-synchronized, concurrency-parallelism, shared, core-atomic, atomicop, atomicload, synchronized, mutex, condition, memory-order, lock-free, d]
level: advanced
status: docs-checked
description: "Share data across threads with the shared qualifier, atomicOp/atomicLoad/atomicStore with memory ordering, synchronized methods, Mutex, Condition and __gshared hazards."
sources:
  - https://dlang.org/phobos/core_atomic.html
  - https://dlang.org/phobos/core_sync_mutex.html
  - https://dlang.org/phobos/core_sync_condition.html
  - https://dlang.org/phobos/core_thread_osthread.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# shared, core.atomic and synchronized

Goal: write correct shared-memory code.

- `core.atomic`: `atomicOp!"+="(counter, 1)` on a `shared` variable, `atomicLoad(counter)`, `atomicStore(counter, v)`, `cas(&counter, old, new)`. `MemoryOrder` is an enum with `acq`, `rel`, `seq` among its members; `seq` is the default for `atomicStore` and `cas`.
- `core.sync.mutex.Mutex` is a class (it implements the object monitor); `core.sync.condition.Condition` has `wait` and `notify`; `core.sync.semaphore`, `core.sync.rwmutex` and `core.sync.barrier` are the other primitives.
- Manual threads: `core.thread.Thread` with `start()`; `thread_joinAll()` (core.thread.threadbase) joins all non-daemon threads.
- Prefer message passing (`std.concurrency`) or `std.parallelism` when possible.

Gotchas:
- `shared` is a type qualifier, not a lock; review any cast that removes it.
- Check the language spec for the exact rules for `synchronized` before relying on them.

Verify: 8 threads each calling `atomicOp!"+="` 100000 times; final value must be 800000.

## Checked

2026-11-03. Confirmed against: core.atomic, core.sync.mutex, core.sync.condition, core.sync.semaphore, core.sync.barrier, core.sync.rwmutex, and core.thread.threadbase.

Removed because the pages read did not confirm it: claim that `shared` reads/writes fail to compile, `synchronized` statement/class semantics, `__gshared`, `shared this()` pattern, casting advice, 800000 verification example arithmetic left as an exercise.

Method: documentation only; no commands were run.
