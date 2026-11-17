---
id: computing-software.software-engineering.go.goroutines-channels-and-context
name: goroutines-channels-and-context
category: computing-software
field: software-engineering
product: go
tags: [go, golang, goroutines, channels, context, context-cancellation, withtimeout, errgroup, select, race-detector, go-test-race, goroutine-leak, goleak, channel-ownership, sync-waitgroup, mutex, worker-pool, backpressure, pprof, concurrency, synctest, go-concurrency-basics, go-context, go-context-cancellation, go-context-cause]
level: practitioner
status: verified
description: "Write leak-free concurrent Go: channel ownership rules, context cancellation everywhere, errgroup for fan-out, select patterns, and catching races and leaks with -race and goleak."
sources: ["Go blog - Go Concurrency Patterns: Context", "Go blog - Go Concurrency Patterns: Pipelines and cancellation", "golang.org/x/sync/errgroup package documentation", "Go documentation - Data Race Detector"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Goroutines, channels and context — concurrency that always terminates

**Goal:** every goroutine you start has a known owner, a way to stop, and a way to
report errors; the race detector and leak checks run in CI.

## 1. The three questions before `go func()`
1. **When does it stop?** (context cancelled, input channel closed, work done)
2. **Who waits for it?** (`WaitGroup`, `errgroup`, a result channel)
3. **Where does its error go?**
If you can't answer all three, it will leak. A blocked goroutine holds its stack and
everything it references forever.

## 2. Channel ownership rules
- The **sender owns** the channel: it creates it, writes, and is the only one that
  `close`s it. Receivers never close.
- Closing signals "no more values"; it is not required for GC. Close when receivers
  `range` over it.
- Send on a closed channel panics; receive from closed returns zero value immediately
  (`v, ok := <-ch` to detect). A nil channel blocks forever — useful to disable a
  `select` case.
- Expose direction in signatures: `func produce(ctx context.Context) <-chan Item`.
- Unbuffered = handoff/synchronisation. Buffer only with a reason (known burst size,
  semaphore); a buffer doesn't fix a slow consumer, it delays the deadlock.

## 3. Context
- First parameter, named `ctx`, never stored in structs (except long-lived request-
  scoped objects by explicit design). Never pass `nil`; use `context.TODO()`.
- Always `defer cancel()` from `WithCancel`/`WithTimeout`/`WithDeadline` — `go vet`
  (lostcancel) flags misses.
- Every blocking send/receive in a goroutine must also select on `ctx.Done()`:
```go
for _, it := range items {
    select {
    case out <- it:
    case <-ctx.Done():
        return ctx.Err()
    }
}
```
- `context.Cause(ctx)` with `WithCancelCause` (Go 1.20+) tells you *why*;
  `context.WithoutCancel` (1.21+) for cleanup work that must outlive the request;
  `context.AfterFunc` (1.21+) to run something on cancellation.

## 4. errgroup for fan-out
```go
g, ctx := errgroup.WithContext(ctx)
g.SetLimit(8)                       // bounded concurrency
for _, u := range urls {
    g.Go(func() error {             // Go 1.22+: loop var is per-iteration
        return fetch(ctx, u)
    })
}
if err := g.Wait(); err != nil { return err }  // first error; ctx cancelled for the rest
```
Results: write into a pre-sized slice by index (no lock needed), or a mutex-guarded map.
`sync.WaitGroup.Go` (Go 1.25+) shortens the plain-WaitGroup pattern.

## 5. select patterns
- Timeout per operation: `case <-time.After(d)` is fine since Go 1.23 (unreferenced
  timers are collected); in hot loops prefer one `time.NewTimer` and `Reset`.
- Non-blocking try: `select { case ch <- v: default: dropped++ }` for load-shedding.
- `select` picks randomly among ready cases — don't rely on order; check `ctx.Done()`
  first in a separate non-blocking select if priority matters.

## 6. Catching races and leaks
- `go test -race ./...` in CI (typical program: 2-20x slower, 5-10x memory per the Go docs; needs cgo, so a C compiler must be present — it failed here with `-race requires cgo`). It only finds races that actually execute.
- Leaks in tests: `go.uber.org/goleak` — `defer goleak.VerifyNone(t)` or
  `goleak.VerifyTestMain(m)`.
- Production: `runtime.NumGoroutine()` as a metric; a steadily rising line is a leak.
  `curl localhost:6060/debug/pprof/goroutine?debug=1` groups stacks — thousands parked
  on the same `chan send` line is your culprit. Keep pprof on an internal port.
- Deterministic tests of timing code: `testing/synctest` (stable in Go 1.25).

## Gotchas
- Returning early from a consumer (error on item 3) leaves the producer blocked on send
  forever unless it also selects on `ctx.Done()`.
- `time.Tick` in a function that returns leaked a ticker before Go 1.23; still prefer
  `NewTicker` + `defer Stop()`.
- `wg.Add` must happen before `go`, not inside the goroutine.
- Maps are not safe for concurrent write — that's a fatal runtime error, not a panic
  you can recover.
- Copying a struct containing a `sync.Mutex` copies the lock; `go vet` (copylocks) catches it.
- `http.Client` without a timeout ignores your intent unless the request carries a ctx
  (`http.NewRequestWithContext`).

## Verify
- [ ] Every `go` statement has a documented stop condition and a waiter.
- [ ] Only senders close channels; no "close from receiver" code.
- [ ] Blocking channel ops in goroutines also select on `ctx.Done()`.
- [ ] `go test -race ./...` and `go vet ./...` pass in CI.
- [ ] goleak verifies tests leave no goroutines behind.
- [ ] Goroutine count is exported as a metric and is flat under steady load.

Related: computing-software.software-engineering.concurrency.profiling-before-optimising

## Checked
2026-10-21 on Go 1.27.3 (Windows), golang.org/x/sync v0.24.0, goleak: `errgroup.WithContext` + `SetLimit(2)` kept peak concurrency at 2, returned the first error and cancelled the context; `context.WithCancelCause`/`Cause`, `WithoutCancel`, `AfterFunc` and `sync.WaitGroup.Go` ran; closed-channel receive gave `0 false` and send panicked; `select` split 491/509 over 1000 rounds; `go vet` flagged a discarded cancel (lostcancel) and a copied `sync.Mutex` (copylocks); concurrent map writes ended in `fatal error: concurrent map writes` that `recover` did not catch; `/debug/pprof/goroutine?debug=1` grouped 5 goroutines stuck on one send line; `goleak.VerifyNone` failed a test that leaked a goroutine blocked on a channel send. From official pages: race detector overhead (5-10x memory, 2-20x time) at https://go.dev/doc/articles/race_detector, Go 1.23 timer collection (https://go.dev/doc/go1.23), `testing/synctest` and `WaitGroup.Go` in Go 1.25 (https://go.dev/doc/go1.25). `go test -race` itself could not run here (needs cgo and a C compiler).
