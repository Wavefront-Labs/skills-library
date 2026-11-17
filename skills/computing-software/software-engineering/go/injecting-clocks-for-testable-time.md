---
id: computing-software.software-engineering.go.injecting-clocks-for-testable-time
name: injecting-clocks-for-testable-time
category: computing-software
field: software-engineering
product: go
tags: [go, go-time-rand, go-clock-injection, clock, injection, fake-clock, time-testing]
level: practitioner
status: docs-checked
description: "Make time-dependent Go code deterministic: inject a clock function or interface, use testing/synctest, and avoid sleeping in tests."
sources:
  - https://pkg.go.dev/testing/synctest
  - https://pkg.go.dev/time
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Injecting clocks for testable time

**Goal:** tests for expiry, backoff and scheduling that run in microseconds and never flake.

Minimal approach: inject `func() time.Time`.

```go
type Cache struct { now func() time.Time; ttl time.Duration; m map[string]entry }
func NewCache(ttl time.Duration) *Cache { return &Cache{now: time.Now, ttl: ttl, m: map[string]entry{}} }
func (c *Cache) Get(k string) (string, bool) {
    e, ok := c.m[k]
    if !ok || c.now().After(e.expires) { return "", false }
    return e.val, true
}

func TestExpiry(t *testing.T) {
    now := time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)
    c := NewCache(time.Minute); c.now = func() time.Time { return now }
    c.Set("a", "1")
    now = now.Add(61 * time.Second)
    if _, ok := c.Get("a"); ok { t.Fatal("should be expired") }
}
```

For timers, tickers and goroutines, `testing/synctest` (`synctest.Test` was added in Go 1.25) runs a function in an isolated "bubble":
`synctest.Test(t, func(t *testing.T){ ... time.Sleep(time.Hour); synctest.Wait() ... })`. Inside a bubble the `time` package uses a fake clock
that starts at midnight UTC 2000-01-01 and advances only when every goroutine in the bubble is durably blocked. `synctest.Wait` blocks until all
other goroutines in the bubble are durably blocked.

## Gotchas
- Compare with `time.Time.Equal`, not `==`: `==` also compares the location and the monotonic clock reading.
- Times from `time.Now()` carry a monotonic reading that is omitted when serialised; `Round(0)` strips it. The monotonic clock may stop while the computer sleeps on some systems.
- Blocking on I/O such as a network socket is not durably blocking, so a bubble never becomes idle on it; use an in-process fake network connection as the synctest docs do.
- A channel, `time.Timer` or `time.Ticker` created in a bubble panics if used from outside it.
- Since Go 1.23 the garbage collector recovers unreferenced, unstopped timers, so `time.After` in a loop no longer leaks until it fires.

## Checked
2026-11-09. Confirmed on pkg.go.dev/testing/synctest (`Test` added go1.25.0, bubble, fake clock start, durably blocking rules, `Wait`, fake network advice) and pkg.go.dev/time (monotonic clock section, `Equal`, `Round`, `UTC`, `After` and the Go 1.23 timer note).
Removed: the Go 1.24 experiment claim, the third-party clock libraries, "UTC() strips monotonic" (it only sets the location), and the timing and `-race` claims in Verify.
Method: documentation only; no commands were run.

## Verify
The expiry test finishes without real sleeping and passes repeatedly (`-count`).
