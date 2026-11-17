---
id: computing-software.software-engineering.v-lang.v-shared-lock-rlock
name: v-shared-lock-rlock
category: computing-software
field: software-engineering
product: v-lang
tags: [v-shared-lock-rlock, shared-state-and-sync, shared, lock, rlock, shared-variable, data-race, race-detector, v-lang]
level: advanced
status: docs-checked
description: "Declare shared variables, pass them to threads and access them in lock (read/write) or rlock (read-only) blocks; know which shared map operations lock for you."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
  - https://docs.vlang.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# shared objects with lock and rlock

Goal: exchange data between threads through a variable that carries a hidden mutex.

```v
struct Counter {
mut:
	value int
}

fn (shared counter Counter) increment() {
	lock counter {
		counter.value += 1
	}
}

fn main() {
	shared counter := Counter{}
	spawn counter.increment()
	spawn counter.increment()
	rlock counter {
		println('Final value: ${counter.value}')
	}
}
```
- Create the variable with `shared` and pass it to the thread as `shared` too. The underlying struct contains a hidden mutex.
- `lock` gives read/write access, `rlock` read-only access.
- Shared variables must be structs, arrays or maps.
- A `shared` parameter is declared `shared m map[K]V` and passed as `shared m`; `shared &m` is unsupported (remove the `&`).
- Single operations on a `shared` map lock automatically: `m[k] = v`, `m[k] += v`, `m[k]++`, `m[k] << v`, `m.delete(k)`,
  `m.clear()` take a lock; reads such as `m[k]`, `k in m`, `m.len`, `m.keys()`, `m.values()`, `m.clone()` take an rlock.
- Operations that must happen together, iterating the map, `if v := m[k] {` and statements using two `shared` maps still
  need an explicit `lock`/`rlock` block.
- Channels are for message passing with implicit synchronisation; shared objects are for direct sharing with explicit
  `lock`/`rlock`.

Gotchas:
- A data race is two threads touching the same memory with at least one write and no ordering by a channel, lock block,
  `sync` primitive or atomic. Build, run or test with `-race` (`v -race run main.v`, `v -race test .`) to use the built-in detector.

Verify: several threads each incrementing a shared counter N times give exactly threads times N, checked inside an `rlock`.

## Checked

Read the Shared Objects, Thread-safe maps, Difference Between Channels and Shared Objects and Race Detector sections of the V documentation (doc/docs.md from the vlang/v repository, the source of docs.vlang.io). Removed claims the page does not state: "access outside lock/rlock is a compile error", `lock a, b { }` multi-lock form, lock-ordering and "no blocking I/O inside" advice. Tags previously contained spaces and were fixed.

Method: docs-only read of cited pages, 2026-11-08
