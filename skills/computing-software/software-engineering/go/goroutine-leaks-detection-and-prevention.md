---
id: computing-software.software-engineering.go.goroutine-leaks-detection-and-prevention
name: goroutine-leaks-detection-and-prevention
category: computing-software
field: software-engineering
product: go
tags: [go, go-concurrency-basics, go-goroutine-leaks, goroutine-leak, leak-detection]
level: practitioner
status: docs-checked
description: "Find and prevent leaked goroutines in Go with context cancellation, pprof goroutine dumps and goleak in tests."
sources:
  - https://go.dev/doc/diagnostics
  - https://pkg.go.dev/runtime/pprof
  - https://github.com/uber-go/goleak
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Goroutine leaks: detection and prevention

**Goal:** every goroutine has a documented exit condition.

Typical leaks: a sender blocked on an unbuffered channel nobody reads, a receiver on a channel nobody closes, or a goroutine ignoring `ctx.Done()`.

```go
func fetch(ctx context.Context, urls []string) []string {
    out := make(chan string, len(urls))        // buffered: senders never block
    for _, u := range urls {
        go func() {
            select {
            case out <- get(ctx, u):
            case <-ctx.Done():
            }
        }()
    }
    ...
}
```

**Detect:**
- The `goroutine` profile reports the stack traces of all current goroutines; it can be collected through the endpoints of `net/http/pprof` (registered on the default mux, or register the handlers yourself on an internal port). In `runtime/pprof`, `debug=2` prints the stacks in the form a dying program uses, and a `goroutineleak` profile (stack traces of all leaked goroutines) is listed among the predefined profiles; check your Go version's docs before relying on it.
- `runtime.NumGoroutine()` returns the number of current goroutines and can be monitored to detect leaks (Go diagnostics page).
- In tests use `defer goleak.VerifyNone(t)`, or `goleak.VerifyTestMain(m)` in a `TestMain` to check once per package.

## Gotchas
- goleak cannot tell a leaked goroutine from a test that has not finished when tests use `t.Parallel`; use `VerifyTestMain` for those.
- With `VerifyTestMain` the leak check runs once after all tests, so a failure does not say which test leaked; run tests individually to find it.
- Buffering to hide a leak just moves it; fix the exit path.

## Checked
2026-11-09. Confirmed on go.dev/doc/diagnostics (goroutine profile, `net/http/pprof` handlers, `NumGoroutine`), pkg.go.dev/runtime/pprof (`goroutine` and `goroutineleak` profiles, `debug=2`) and the goleak README (`VerifyNone`, `VerifyTestMain`, `t.Parallel` note, per-package check).
Removed: the `time.After` pre-1.23 claim, the HTTP-body cause, `goleak.IgnoreTopFunction` and "ignores nothing by default", the localhost port in the curl command, and the `-count` advice.
Method: documentation only; no commands were run.

## Verify
Run the suite with goleak enabled and confirm no unexpected goroutines are reported; the goroutine count at idle should return to its baseline after load.
