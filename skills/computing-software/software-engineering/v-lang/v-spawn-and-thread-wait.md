---
id: computing-software.software-engineering.v-lang.v-spawn-and-thread-wait
name: v-spawn-and-thread-wait
category: computing-software
field: software-engineering
product: v-lang
tags: [v-spawn-and-thread-wait, concurrency-basics, spawn, thread, wait, thread-handle, join, v-lang]
level: practitioner
status: docs-checked
description: "Run functions concurrently with spawn, keep thread handles, wait for results singly or as an array, and know what a discarded handle does."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
  - https://docs.vlang.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# spawn and waiting on threads

Goal: run work in parallel and collect results.

- `spawn foo()` runs `foo()` concurrently in a different thread. The docs describe `spawn` threads as OS threads with
  resource overhead and scalability limits at high thread counts. `go foo()` is documented separately as running `foo()`
  in a lightweight thread managed by the V runtime.
- Keep the handle to wait: `h := spawn p(3, 4)` then `h.wait()`. For a value-returning function, `r := h.wait()`
  gives the result; the function does not need to change.
- Many tasks: `mut threads := []thread{}`, `threads << spawn task(1, 500)`, then `threads.wait()`.
  Same-typed results: `mut threads := []thread int{}` and `r := threads.wait()` returns an array of the values.
- If the spawned function returns `?T` or `!T`, waiting on the array returns `?[]T` or `![]T`, handled with `or`, `?` or `!`.
- A closure can be spawned: `spawn fn (a f64, b f64) { ... }(3, 4)`; a method too (`spawn counter.increment()`).
- A spawned call with a `mut param &T` parameter receives the caller's mutable pointer storage; keep that storage alive
  until the thread finishes.
- Sleep with `time.sleep(500 * time.millisecond)`.

Gotchas:
- Discarding a handle (including `dump(spawn ...)` or inside a discarded array or struct) detaches the thread; keep the
  handle and call `wait()` when the result or completion matters.
- Share state via `shared` objects or channels (see v-shared-lock-rlock and v-channels).

Verify: spawn workers that compute squares into a `[]thread int`, wait, and compare the array to the expected squares.

## Checked

Read the Spawning Concurrent Tasks section of the V documentation (doc/docs.md from the vlang/v repository, the source of docs.vlang.io). Removed claims the page does not state: "go was replaced by spawn in V < 0.3.x", an experimental coroutine mode, "main exiting kills running threads", "captured variables are copied" and the capture-list closure form. Tags previously contained spaces and were fixed.

Method: docs-only read of cited pages, 2026-11-08
