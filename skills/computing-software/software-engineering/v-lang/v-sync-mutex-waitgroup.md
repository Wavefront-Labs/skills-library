---
id: computing-software.software-engineering.v-lang.v-sync-mutex-waitgroup
name: v-sync-mutex-waitgroup
category: computing-software
field: software-engineering
product: v-lang
tags: [v-sync-mutex-waitgroup, shared-state-and-sync, sync, mutex, waitgroup, rwmutex, once, atomic, stdatomic, lock unlock, v-lang]
level: practitioner
status: docs-checked
description: "Use the sync module for Mutex, RwMutex, WaitGroup, Once and stdatomic types when shared objects are not enough."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sync.Mutex, WaitGroup and atomics

Goal: coordinate threads with classic primitives.

- `import sync`; `mut mu := sync.new_mutex()`; `mu.lock()`; `defer { mu.unlock() }`.
- `mut wg := sync.new_waitgroup()`; `wg.add(n)`; each worker `wg.done()`; main `wg.wait()`.
- Read/write: `sync.new_rwmutex()` with `rlock()/runlock()/lock()/unlock()`.
- Atomics: `import sync.stdatomic`; `stdatomic.new_atomic[T](val)` returns `&AtomicVal[T]` with `.add(delta)`, `.load()` and `.store(val)`.
- Once: `mut once := sync.new_once()`; `once.do(fn () { ... })` runs the function a single time (calling `do` on the same Once from inside `f` deadlocks).

Gotchas:
- `sync.new_mutex()` and `sync.new_rwmutex()` return references (`&Mutex`, `&RwMutex`); `sync.new_waitgroup()` returns `&WaitGroup`.

Verify: run a counter test with several threads and assert the final total.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: new_mutex/new_rwmutex/new_waitgroup return references, Mutex lock/unlock, RwMutex rlock/runlock/lock/unlock, WaitGroup add/done/wait, Once and new_once and do (vlib/sync/once.v), stdatomic.new_atomic and AtomicVal add/load/store (vlib/sync/stdatomic/atomic.c.v).
Removed or corrected: the atomics '(confirm)', the unverified struct-embedding example, 'passing a Mutex by value copies it', the wg.add race claim and the thread-sanitizer command line.
Method: documentation only; no commands were run.
