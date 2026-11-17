---
id: computing-software.software-engineering.go.happens-before-and-data-races
name: happens-before-and-data-races
category: computing-software
field: software-engineering
product: go
tags: [go, go-sync-memory, go-happens-before, memory-model, data-race]
level: advanced
status: docs-checked
description: "Apply the Go memory model: what establishes happens-before, why unsynchronised reads race, and how to fix common races."
sources:
  - https://go.dev/ref/mem
  - https://go.dev/doc/articles/race_detector
  - https://go.dev/blog/loopvar-preview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Happens-before and data races

**Goal:** reason about visibility instead of guessing.

A data race is two accesses to the same memory location, at least one a write, unordered by happens-before (the memory model's formal definition also requires at least one to be non-synchronizing). The Go memory model (version of June 6, 2022) guarantees sequentially consistent outcomes (DRF-SC) for data-race-free programs. Synchronisation edges from the model:
- The `go` statement that starts a goroutine is synchronized before the goroutine's execution starts.
- A channel close is synchronized before a receive that returns because the channel is closed. A send is synchronized before the corresponding receive completes.
- For a `sync.Mutex` or `sync.RWMutex`, call n of `Unlock` is synchronized before call m of `Lock` returns (n < m).
- `once.Do(f)`: only one call runs `f`, and other calls block until `f()` has returned.
- All `sync/atomic` operations behave as though executed in some sequentially consistent order, and if atomic operation A is observed by B, A is synchronized before B.
- Other `sync` types (wait groups, condition variables and so on) document their own guarantees; read their docs.

```go
var ready bool; var msg string
go func() { msg = "hi"; ready = true }()
for !ready {}        // RACE: no edge, so no guarantee the write is ever observed
print(msg)
```
The model says a statement with no following synchronization event is not guaranteed to be observed by another goroutine, and that an aggressive compiler might even delete a `go` statement whose only effect is such an assignment. Fix with a channel, a mutex, or a `sync/atomic` value.

Programs with races are incorrect: a read may observe any concurrent write, and later reads need not observe earlier writes. The race detector's article states that concurrent reads and writes of the same map are not safe.

## Gotchas
- "Benign" races on counters or flags are still races; use `sync/atomic` or a lock.
- Closing over a loop variable raced under per-loop variable scope (the race detector article shows it printing 55555 instead of 01234). Go 1.22 changes loops to per-iteration scope, applied only in modules whose `go.mod` declares go 1.22 or later.
- Unsynchronized send and close on the same channel can also be a race.

## Verify
Run the tests with `go test -race`. The race detector only finds races that happen at runtime, so it cannot find races in code paths that are not executed: it cannot prove absence of races. Run a `-race` binary under a realistic workload as well.

## Checked
2026-11-09. Read go.dev/ref/mem (edge rules, DRF-SC, race definition, atomics, compiler restrictions), the race detector article and the Go 1.22 loopvar blog post. Removed: WaitGroup.Wait edge (the model defers to sync docs), torn multi-word values claim, the "fatal error: concurrent map writes" runtime message, and specific atomic type names (not on pages read).
Method: documentation only; no commands were run.
