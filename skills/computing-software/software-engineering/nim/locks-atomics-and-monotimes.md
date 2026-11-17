---
id: computing-software.software-engineering.nim.locks-atomics-and-monotimes
name: locks-atomics-and-monotimes
category: computing-software
field: software-engineering
product: nim
tags: [locks-atomics-and-monotimes, stdlib-math-random-misc, locks, withlock, atomics, atomic, monotimes, getmonotime, condvar, benchmark-timing, nim]
level: advanced
status: docs-checked
description: "Protect shared state with Lock and withLock, use Atomic types, and time code with monotimes."
sources:
  - https://nim-lang.org/docs/locks.html
  - https://nim-lang.org/docs/atomics.html
  - https://nim-lang.org/docs/monotimes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# locks, atomics and monotonic timing

Goal: synchronise and measure.

- `import std/locks`: `var L: Lock; initLock(L); withLock L: counter += 1`; `deinitLock(L)`. Condition variables: `Cond`, `wait`, `signal`.
- Annotate globals: `var counter {.guard: L.}: int` so the compiler checks protected access.
- `import std/atomics`: `var a: Atomic[int]`, `a.fetchAdd(1)`, `a.load()`, `a.store(x)`, `compareExchange`.
- Timing: `import std/monotimes`; `let t0 = getMonoTime(); ...; echo (getMonoTime() - t0).inMilliseconds`.

Gotchas:
- `getMonoTime()` timestamps are monotonic: they measure time passed since some system-defined point and never go backwards.

Verify: parallel increments with the lock end at the exact count.

## Checked

2026-11-03. Confirmed against the locks, atomics and monotimes pages: Lock/initLock/deinitLock/withLock, Cond with wait and signal, Atomic[T] load/store/fetchAdd/compareExchange, getMonoTime, inMilliseconds, monotonic semantics. Removed: the doNotOptimizeAway-style benchmark advice, the uninitialised lock statement and the epochTime remark (times module not read).

Method: documentation only; no commands were run.
