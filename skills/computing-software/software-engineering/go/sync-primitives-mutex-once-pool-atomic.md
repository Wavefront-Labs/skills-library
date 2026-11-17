---
id: computing-software.software-engineering.go.sync-primitives-mutex-once-pool-atomic
name: sync-primitives-mutex-once-pool-atomic
category: computing-software
field: software-engineering
product: go
tags: [go, goroutines, channels, sync-once, sync-pool, sync-mutex, atomic, data-race, go-sync-memory, go-atomic-types, go-sync-map-once]
level: practitioner
status: verified
description: "Pick the right Go sync primitive: Mutex/RWMutex, Once and OnceValue, Pool for allocation reuse, atomic types, sync.Map, and verifying with the race detector."
sources:
  - https://pkg.go.dev/sync
  - https://pkg.go.dev/sync/atomic
  - https://go.dev/ref/mem
  - https://go.dev/doc/articles/race_detector
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# sync.Mutex, Once, Pool and atomic

**Goal:** correct shared-state access with the simplest primitive that fits, proven by `-race`.

## 1. Mutex
```go
type Counter struct {
    mu sync.Mutex
    m  map[string]int
}
func (c *Counter) Inc(k string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.m[k]++
}
```
- Keep the mutex next to the fields it guards; never copy a struct containing a mutex (`go vet` copylocks check). Use pointer receivers.
- `RWMutex` only helps when reads dominate **and** critical sections are non-trivial; otherwise plain `Mutex` is faster.
- Do not hold a lock while doing I/O or calling unknown callbacks.

## 2. Once, OnceValue, OnceFunc (1.21+)
```go
var loadConfig = sync.OnceValues(func() (*Config, error) { return parse("config.yaml") })
cfg, err := loadConfig()          // runs once; later calls return cached results
```
`sync.Once.Do` runs exactly once even if `f` panics (and the panic is not retried); for retry-on-error semantics write your own with a mutex.

## 3. Pool: reuse short-lived allocations
```go
var bufPool = sync.Pool{New: func() any { return new(bytes.Buffer) }}
func render(v any) []byte {
    b := bufPool.Get().(*bytes.Buffer)
    b.Reset()
    defer bufPool.Put(b)
    json.NewEncoder(b).Encode(v)
    return bytes.Clone(b.Bytes())     // never return pooled memory to callers
}
```
- Items can be dropped at any GC; Pool is a cache, not a resource limiter (use a channel/semaphore for connection limits).
- Avoid pooling huge buffers: cap the size before `Put` or one big request bloats the pool.
- Measure with benchmarks (`-benchmem`); pools add complexity.

## 4. Atomics
```go
var requests atomic.Int64
requests.Add(1)
var cfg atomic.Pointer[Config]
cfg.Store(newCfg)                  // lock-free hot reload; readers do cfg.Load()
```
Typed atomics (`atomic.Int64`, `Bool`, `Pointer[T]`) are 64-bit aligned automatically and prevent non-atomic access by accident. Use atomics for independent counters/flags; once two values must change together, use a mutex.

## 5. sync.Map
Optimised for keys written once and read many times, or disjoint key sets per goroutine. For general use a `map` + `Mutex` is clearer and often faster; consider sharding for heavy contention.

## Gotchas
- Data races are undefined behaviour in Go (torn reads, corrupted maps); "concurrent map writes" is a fatal error that cannot be recovered.
- `WaitGroup.Add` must happen before starting the goroutine, not inside it.
- Lock ordering: acquire multiple mutexes in a consistent order to avoid deadlocks.
- `defer mu.Unlock()` in a loop body defers until function return; wrap the body in a function.

## Verify
- `go test -race ./...` (and a race-enabled staging build under load) reports no races; contention shows in the mutex profile (`runtime.SetMutexProfileFraction`, `go tool pprof .../mutex`).

## Checked
2026-10-21 on Go 1.27.3 (Windows): `sync.OnceValues` ran once and cached both the value and the error; `Once.Do` ran its panicking function once and the second call returned normally; `OnceFunc` ran once; the `bufPool` render pattern returned correct JSON; a `sync.Pool` item survived a Put/Get but a Put item was gone after two `runtime.GC()` calls; `atomic.Int64` and `atomic.Pointer` worked; with `GOARCH=386` an `atomic.Int64` after a bool sat at offset 8 (aligned) and the sync/atomic docs say Int64/Uint64 are automatically aligned; `defer mu.Unlock()` inside a loop left a goroutine blocked on the second `Lock` (2 goroutines alive); `go vet` was clean. `sync.Map` optimisation cases and RWMutex guidance confirmed under rwmutex-and-sync-cond (`go doc sync.Map`). `-race` needs cgo and could not run here; the mutex profile (`runtime.SetMutexProfileFraction(1)` + `pprof.Lookup("mutex")` + `go tool pprof -top`) attributed 335 ms of delay to a contended `Mutex.Unlock` in a 4-goroutine test.
