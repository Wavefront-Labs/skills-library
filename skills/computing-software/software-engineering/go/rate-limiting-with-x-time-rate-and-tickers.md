---
id: computing-software.software-engineering.go.rate-limiting-with-x-time-rate-and-tickers
name: rate-limiting-with-x-time-rate-and-tickers
category: computing-software
field: software-engineering
product: go
tags: [go, golang, x-time-rate, rate-limiting, token-bucket, time-ticker, throttling, concurrency]
level: practitioner
status: verified
description: "Rate-limit Go code with golang.org/x/time/rate token buckets (Wait/Allow/Reserve, per-key limiters) and use time.Ticker correctly for periodic work."
sources: ["https://pkg.go.dev/golang.org/x/time/rate", "https://pkg.go.dev/time#Ticker", "https://go.dev/doc/go1.23#timer-changes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rate limiting with x/time/rate and tickers

**Goal:** cap request or work rates smoothly (token bucket) and run periodic jobs without
leaking tickers or drifting.

## Token bucket: rate.Limiter
`rate.NewLimiter(r, b)`: refill `r` tokens/second, bucket capacity `b` (burst).
```go
import "golang.org/x/time/rate"

lim := rate.NewLimiter(rate.Limit(10), 20)        // 10/s sustained, bursts of 20
lim := rate.NewLimiter(rate.Every(200*time.Millisecond), 1) // one per 200ms, no burst
```
Three ways to consume:
| Method | Behaviour | Use for |
|---|---|---|
| `Wait(ctx)` | blocks until a token is available or ctx done | outbound clients (respect a third-party API quota) |
| `Allow()` | non-blocking bool | inbound servers: reject with 429 |
| `Reserve()` | returns a reservation with `Delay()`; `Cancel()` to give back | scheduling, custom backoff |

```go
func (c *Client) Do(ctx context.Context, req *http.Request) (*http.Response, error) {
    if err := c.lim.Wait(ctx); err != nil { // returns error if wait would exceed ctx deadline
        return nil, err
    }
    return c.http.Do(req.WithContext(ctx))
}
```
`Wait` returns an error immediately if `n` exceeds the burst size, or if the context deadline is
sooner than the token would be available.

## Per-client limiting (HTTP middleware)
```go
type limiters struct {
    mu sync.Mutex
    m  map[string]*rate.Limiter
}
func (l *limiters) get(key string) *rate.Limiter {
    l.mu.Lock(); defer l.mu.Unlock()
    lim, ok := l.m[key]
    if !ok { lim = rate.NewLimiter(5, 10); l.m[key] = lim }
    return lim
}
// in handler: if !ls.get(clientIP(r)).Allow() { w.Header().Set("Retry-After", "1"); http.Error(w, "slow down", 429); return }
```
The map grows without bound; evict idle keys (store last-seen, sweep periodically) or use an LRU.
In-process limits are per instance: behind N replicas the effective limit is N times higher. For a
global limit use a shared store (Redis) or the gateway.

`SetLimit`/`SetBurst` adjust a live limiter (for example from remote config).

## time.Ticker for periodic work
```go
t := time.NewTicker(30 * time.Second)
defer t.Stop()
for {
    select {
    case <-ctx.Done():
        return
    case <-t.C:
        doWork(ctx)
    }
}
```
- A ticker drops ticks if the receiver is slow (since Go 1.23 the channel is unbuffered, `cap(t.C)` is 0); it does not queue a backlog.
  If work takes longer than the period, the next run starts immediately after.
- `time.Tick` is fine since Go 1.23: unreferenced tickers are now garbage-collected even unstopped,
  but `NewTicker` + `Stop` is still clearer and stoppable.
- `t.Reset(d)` changes the period. For "wait d after each run finishes" use `time.Sleep` or a
  `time.Timer` reset after work rather than a ticker.
- Add jitter for fleets so all replicas do not hit a dependency at the same second.

## Verify
- [ ] Load test shows sustained rate near `r` and initial burst near `b`.
- [ ] 429 responses include `Retry-After`.
- [ ] Per-key limiter map is bounded.
- [ ] Ticker loops exit on context cancellation (goleak in tests).

## Checked
2026-10-21 on Go 1.27.3 (Windows), golang.org/x/time v0.16.0: `NewLimiter(10, 20)` allowed exactly 20 immediate `Allow()` calls; `rate.Every(200ms)` with burst 1 gave Limit 5, and 4 `Wait` calls took about 600 ms; `WaitN(2)` over a burst of 1 failed with `exceeds limiter's burst 1`; a context deadline shorter than the delay failed immediately with `would exceed context deadline`; `Reserve().Delay()` was 200 ms and `SetLimit`/`SetBurst` changed a live limiter; a ticker slept through 5 periods delivered 1 tick (no backlog) and `cap(t.C)` is 0 on Go 1.27; `Reset` changed the period. Go 1.23 timer/ticker channel and garbage-collection change from https://go.dev/doc/go1.23. Also ran: the per-key limiter middleware (burst 10, rate 5) let 10 of 15 instant requests through and returned 429 with `Retry-After: 1` for 5. Redis-backed limits were not tested; that sentence is advice only.
