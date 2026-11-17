---
id: computing-software.software-engineering.go.waitgroup-patterns
name: waitgroup-patterns
category: computing-software
field: software-engineering
product: go
tags: [go, golang, waitgroup, sync-waitgroup, goroutines, wg-go, concurrency, copylocks]
level: practitioner
status: docs-checked
description: "Wait for goroutines correctly with sync.WaitGroup: Add before go, WaitGroup.Go (1.25), closing result channels, never copying, and when to switch to errgroup."
sources: ["https://pkg.go.dev/sync#WaitGroup", "https://go.dev/doc/go1.25#sync", "https://pkg.go.dev/golang.org/x/sync/errgroup", "https://pkg.go.dev/cmd/vet"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sync.WaitGroup patterns

**Goal:** every goroutine you start is waited for, with no race between `Add` and `Wait`
and no deadlock from an unclosed channel.

## The canonical shape
```go
var wg sync.WaitGroup
for _, item := range items {
    wg.Add(1)                 // BEFORE the go statement, in the parent goroutine
    go func() {
        defer wg.Done()       // defer so a panic or early return still counts down
        process(item)         // Go 1.22+: item is per-iteration, no copy needed
    }()
}
wg.Wait()
```
Go 1.25 adds `wg.Go(func())`, which does the Add/Done pair for you:
```go
for _, item := range items {
    wg.Go(func() { process(item) })
}
wg.Wait()
```
Prefer `wg.Go` when the module's `go` directive is 1.25+.

## Rules that bite
- **Add inside the goroutine is a race**: `Wait` may run before the goroutine calls `Add`
  and return early. Always call `Add` before `go`.
- **Negative counter panics** - a `Done` without matching
  `Add`, usually from calling `Done` twice on an error path. Use `defer wg.Done()` once at the top.
- **Never copy a WaitGroup** after first use. Pass `*sync.WaitGroup`, or better, keep it local and
  capture it in the closure. `go vet` (copylocks) catches value copies in function parameters.
- **Reuse:** a WaitGroup may be reused only after `Wait` returns; new `Add` calls must happen-after it.

## Collecting results
Close the results channel from a separate goroutine once all workers finish, so the
consumer's `range` terminates:
```go
results := make(chan Result)
var wg sync.WaitGroup
for _, u := range urls {
    wg.Go(func() { results <- fetch(u) })
}
go func() { wg.Wait(); close(results) }()
for r := range results { handle(r) }
```
Alternatively write into a pre-sized slice by index (`out[i] = f(x)`), which needs no channel or
mutex because each goroutine owns a distinct element.

## When WaitGroup is the wrong tool
- You need the **first error** and to **cancel the rest**: use `errgroup.WithContext`.
- You need a **concurrency limit**: `errgroup.Group.SetLimit(n)` or a buffered-channel semaphore;
  a bare WaitGroup launches everything at once.
- Long-lived workers that must stop on shutdown: pair the WaitGroup with a `context.Context` so
  workers can exit, then `Wait` in your shutdown path.

## Verify
- [ ] `go vet ./...` clean (copylocks).
- [ ] `go test -race ./...` passes with the concurrent path exercised.
- [ ] No `Add` call appears inside a spawned goroutine.

## Checked

- Date: 2026-10-28
- Confirmed on pkg.go.dev (sync.WaitGroup, errgroup, cmd/vet) and the Go 1.22 and 1.25 release notes: WaitGroup.Go added in 1.25, Add before Wait, negative counter panics, errgroup SetLimit, per-iteration loop variables (1.22), copylocks vet check.
- Removed: exact panic message.
Method: documentation only; no commands were run.
