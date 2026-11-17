---
id: computing-software.software-engineering.go.pipelines-and-fan-out-fan-in
name: pipelines-and-fan-out-fan-in
category: computing-software
field: software-engineering
product: go
tags: [go, goroutines, channels, go-pipelines, fan-out-fan-in, errgroup, bounded-concurrency, context, go-worker-pools, go-errgroup]
level: practitioner
status: verified
description: "Build Go concurrent pipelines: stage functions, fan-out/fan-in, cancellation with context, errgroup with limits, and avoiding goroutine leaks and deadlocks."
sources:
  - https://go.dev/blog/pipelines
  - https://pkg.go.dev/golang.org/x/sync/errgroup
  - https://go.dev/blog/context
  - https://go.dev/doc/effective_go#concurrency
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Pipelines and fan-out/fan-in in Go

**Goal:** process streams of work concurrently with bounded parallelism, prompt cancellation and no leaked goroutines.

## 1. Stage pattern
Each stage: receives from an inbound channel, sends to an outbound channel it owns and closes.
```go
func gen(ctx context.Context, ids []int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, id := range ids {
            select {
            case out <- id:
            case <-ctx.Done():
                return
            }
        }
    }()
    return out
}
```
Rule: the sender closes; receivers never close. Every send must also select on `ctx.Done()` or the goroutine leaks when downstream stops reading.

## 2. Fan-out / fan-in
```go
func fetchAll(ctx context.Context, in <-chan int, workers int) <-chan Result {
    out := make(chan Result)
    var wg sync.WaitGroup
    for range workers {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for id := range in {
                r := fetch(ctx, id)
                select {
                case out <- r:
                case <-ctx.Done():
                    return
                }
            }
        }()
    }
    go func() { wg.Wait(); close(out) }()   // close after all senders finish
    return out
}
```
Go 1.25 adds `wg.Go(func(){...})` which does Add/Done for you.

## 3. errgroup: the usual answer
```go
g, ctx := errgroup.WithContext(ctx)
g.SetLimit(8)                               // bounded concurrency
results := make([]Item, len(ids))
for i, id := range ids {
    g.Go(func() error {
        it, err := fetch(ctx, id)
        if err != nil { return fmt.Errorf("fetch %d: %w", id, err) }
        results[i] = it                     // distinct index per goroutine: no lock needed
        return nil
    })
}
if err := g.Wait(); err != nil { return err }   // first error; ctx cancelled for the rest
```
Since Go 1.22 loop variables are per-iteration, so capturing `i, id` is safe.

## 4. Choosing parallelism
- I/O bound: limit by downstream capacity (DB pool size, API rate limits), not CPU count.
- CPU bound: `runtime.GOMAXPROCS(0)` workers.
- Use a semaphore (`golang.org/x/sync/semaphore` or a buffered `chan struct{}`) when tasks have different weights.

## Gotchas
- Unbuffered channel with no reader = blocked goroutine forever; `goleak` in tests catches it (`defer goleak.VerifyNone(t)`).
- Order is not preserved through fan-out; carry an index or sequence number if order matters.
- Closing a channel twice or sending on a closed channel panics; only the single owner closes.
- `for v := range ch` blocks until close; forgetting the closer goroutine after `wg.Wait()` deadlocks ("all goroutines are asleep").
- Buffered channels hide backpressure problems; size buffers deliberately.

## Verify
- `go test -race` passes, `goleak.VerifyNone` reports no leaked goroutines after cancelling mid-stream, and throughput scales with the worker count until the limit.

## Checked
2026-10-21 on Go 1.27.3 (Windows), golang.org/x/sync v0.24.0: `gen`, `fetchAll` (with `for range workers` and a closer goroutine after `wg.Wait()`) and the errgroup loop with per-index results ran; 40 jobs took about 410, 100 and 50 ms with 1, 4 and 8 workers and results were out of order with more than one worker; after `cancel()` mid-stream the goroutine count returned to the starting 1; omitting the closer goroutine ended in `fatal error: all goroutines are asleep - deadlock!`. `goleak` and `-race` behaviour is shown in the goroutines-channels-and-context skill (-race needs cgo, unavailable here).
