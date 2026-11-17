---
id: computing-software.software-engineering.crystal.atomic-and-wait-group
name: atomic-and-wait-group
category: computing-software
field: software-engineering
product: crystal
tags: [atomic-and-wait-group, multithreading, atomic, wait-group, waitgroup, compare-and-set, counter, fiber-join, barrier, crystal]
level: advanced
status: docs-checked
description: "Use Atomic(T) for lock-free counters and flags and WaitGroup to wait for a set of fibers to finish."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atomic and WaitGroup

Goal: lightweight coordination.

- `Atomic(Int32).new(0)`; `add(1)` and `sub` return the previous value; `get`, `set`, `swap`; `compare_and_set(old, new)` returns `{value, Bool}`; `Atomic::Flag` (`test_and_set`, `clear`) for a spin flag.
- `WaitGroup`: `wg = WaitGroup.new(3)`; each fiber calls `wg.done`; main calls `wg.wait`; `wg.add(n)` raises the counter and `wg.spawn { ... }` adds one and spawns; `WaitGroup.wait { |w| w.spawn { ... } }` waits for all fibers spawned in the block.
- Fallback pattern: `done = Channel(Nil).new; n.times { spawn { work; done.send nil } }; n.times { done.receive }`.

Gotchas:
- Calling `done` more times than the counter allows raises.
- Atomic only protects a single word; invariants over several fields need a Mutex.
- Memory ordering default is sequentially consistent; relaxed variants take an `ordering` arg.

Verify: 1000 fibers incrementing an atomic yields 1000.

## Checked

Date 2026-11-03. Confirmed in the Atomic and WaitGroup source: Atomic(T) add, sub (returning the previous value), get, set, swap, compare_and_set returning {T, Bool}, Atomic::Ordering with a sequentially_consistent default, Atomic::Flag test_and_set and clear, WaitGroup.new(n), add, done, wait, spawn and WaitGroup.wait with a block. Removed the '(confirm)' hedges.

Method: documentation only; no commands were run.
