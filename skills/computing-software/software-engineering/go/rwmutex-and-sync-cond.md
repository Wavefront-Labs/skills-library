---
id: computing-software.software-engineering.go.rwmutex-and-sync-cond
name: rwmutex-and-sync-cond
category: computing-software
field: software-engineering
product: go
tags: [go, golang, rwmutex, sync-rwmutex, sync-cond, condition-variable, locking, concurrency]
level: advanced
status: verified
description: "Use sync.RWMutex only where reads dominate and measure it, avoid recursive read locks, and use sync.Cond (or channels) correctly with Wait in a loop."
sources: ["https://pkg.go.dev/sync#RWMutex", "https://pkg.go.dev/sync#Cond", "https://go.dev/ref/mem"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RWMutex and sync.Cond

**Goal:** pick the right lock, and do not deadlock on the RWMutex or Cond rules that
the compiler cannot check.

## RWMutex: when it pays
`RWMutex` allows many concurrent `RLock` holders or one `Lock` holder. With very short critical sections the result depends on the core count: in one test on a 12-thread
CPU (two-entry map lookup) `RWMutex` was slower than `Mutex` at 4 procs (29.5 vs 23.1 ns/op) and faster at 12 (36.1 vs 51.6).
It pays when reads heavily dominate and contention is high. Benchmark both with `-cpu=1,4,12` (your core counts) before switching.

```go
type Cache struct {
    mu sync.RWMutex
    m  map[string]Item
}
func (c *Cache) Get(k string) (Item, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    it, ok := c.m[k]
    return it, ok
}
func (c *Cache) Set(k string, it Item) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.m[k] = it
}
```
For read-mostly data replaced wholesale, `atomic.Pointer[T]` (copy-on-write) beats any lock.
For a concurrent map with disjoint keys, consider `sync.Map`.

## RWMutex traps
- **No recursive read locking.** If a goroutine holds `RLock` and calls something that takes
  `RLock` again while a writer is waiting, it deadlocks: a blocked `Lock` call stops new readers.
- **No upgrade.** You cannot turn an `RLock` into a `Lock`. Release, take `Lock`, and re-check the
  condition (another writer may have run in between).
- Unlocking a mutex you do not hold is a fatal runtime error, not a recoverable panic.
- Never copy a struct containing a mutex after use; `go vet` copylocks flags it. Methods that touch
  the lock need pointer receivers.

## sync.Cond
Use when goroutines wait for a **state change** guarded by a mutex and you need `Broadcast` to
wake all of them (channels can only wake all by closing, once).
```go
type Queue struct {
    mu    sync.Mutex
    cond  *sync.Cond
    items []int
}
func NewQueue() *Queue { q := &Queue{}; q.cond = sync.NewCond(&q.mu); return q }
func (q *Queue) Put(v int) {
    q.mu.Lock(); q.items = append(q.items, v); q.mu.Unlock()
    q.cond.Signal()
}
func (q *Queue) Get() int {
    q.mu.Lock()
    defer q.mu.Unlock()
    for len(q.items) == 0 { // ALWAYS a loop: the condition may have changed again before Wait relocked
        q.cond.Wait()        // atomically unlocks, sleeps, relocks
    }
    v := q.items[0]; q.items = q.items[1:]
    return v
}
```
Limits: `Cond.Wait` cannot be cancelled by a `context` or timeout. If waiters need cancellation,
use a channel (`select` on the channel and `ctx.Done()`), which is why most Go code prefers
channels over `Cond`.

## Verify
- [ ] Benchmark shows RWMutex beats Mutex under realistic read/write ratio.
- [ ] No code path takes `RLock` twice on one goroutine.
- [ ] Every `Cond.Wait` is inside a `for` that re-checks the predicate.
- [ ] `go test -race` clean.

## Checked
2026-10-21 on Go 1.27.3 (Windows): the `Queue` with `sync.Cond` (4 consumers, 100 puts) summed to 5050; a second `RLock` on the same goroutine while a writer was queued ended in `fatal error: all goroutines are asleep - deadlock!`, as did `RLock` then `Lock`; unlocking an unlocked `Mutex` and `RUnlock` of an unlocked `RWMutex` were fatal errors; a parallel benchmark of a two-entry map lookup (ns/op at -cpu 1, 4, 12) gave Mutex 14.4/23.1/51.6, RWMutex 14.4/29.5/36.1 and `atomic.Pointer` 5.2/1.7/1.0, so RWMutex lost at 4 CPUs and won at 12 on this machine. `go doc` confirms the no-recursive-read-lock and no-upgrade rules, that `Cond.Wait` should be in a loop because the condition may change before Wait relocks, and the two use cases `sync.Map` is optimised for.
