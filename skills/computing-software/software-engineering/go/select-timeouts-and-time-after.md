---
id: computing-software.software-engineering.go.select-timeouts-and-time-after
name: select-timeouts-and-time-after
category: computing-software
field: software-engineering
product: go
tags: [go, go-select, time-after, timeouts, non-blocking-channel, nil-channels, goroutines]
level: practitioner
status: verified
description: "Use Go's select correctly: multiplexing channels with ctx.Done, timeouts with time.After vs timers, non-blocking sends and receives, nil channels to disable cases, and fairness."
sources: ["https://go.dev/ref/spec#Select_statements", "https://go.dev/blog/pipelines", "https://pkg.go.dev/time#After", "https://go.dev/doc/go1.23#timer-changes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# select, timeouts and time.After

**Goal:** channel coordination that never blocks forever, respects cancellation, and
doesn't leak timers.

## Basics
```go
select {
case msg := <-in:
    handle(msg)
case out <- result:
    // sent
case <-ctx.Done():
    return ctx.Err()
}
```
- Blocks until one case can proceed; if several are ready, one is chosen **at random** (no
  priority, no ordering).
- A `default` case makes it non-blocking.

## Timeouts
```go
select {
case r := <-resultCh:
    return r, nil
case <-time.After(2 * time.Second):
    return nil, errors.New("timed out")
}
```
Prefer context deadlines so the timeout also propagates to the work:
`ctx, cancel := context.WithTimeout(ctx, 2*time.Second); defer cancel()`.

`time.After` in a **loop** creates a new timer every iteration. Before Go 1.23 unreferenced
timers were not collected until they fired (memory growth in hot loops); Go 1.23 made them
collectable and channels unbuffered, but a reused timer is still cheaper:
```go
t := time.NewTimer(idle)
defer t.Stop()
for {
    select {
    case ev := <-events:
        handle(ev)
        t.Reset(idle)          // Go 1.23+: Reset/Stop are safe without draining
    case <-t.C:
        return errIdle
    case <-ctx.Done():
        return ctx.Err()
    }
}
```

## Non-blocking operations
```go
select {
case jobs <- j:
default:
    dropped.Add(1)             // queue full: shed load instead of blocking
}
```

## nil channels disable cases
Receiving from or sending to a nil channel blocks forever, so setting a channel variable to
nil removes it from a select - the idiom for merging until both inputs close:
```go
for a != nil || b != nil {
    select {
    case v, ok := <-a:
        if !ok { a = nil; continue }
        out <- v
    case v, ok := <-b:
        if !ok { b = nil; continue }
        out <- v
    }
}
```

## Priority
select has no priority. To prefer cancellation, check `ctx.Err()` before the select or nest
a non-blocking select on `ctx.Done()` first.

## Gotchas
- `for { select { default: } }` busy-loops a CPU core.
- `break` inside select breaks the select, not the enclosing for: use a labelled break or return.
- Sending on a closed channel panics even inside select.

## Verify
- [ ] Every blocking select in long-running goroutines has a `ctx.Done()` case.
- [ ] Hot loops reuse timers instead of calling time.After per iteration.

## Checked
2026-10-21 on Go 1.27.3 (Windows): 2 million unreferenced `time.After(time.Hour)` calls left about 290 KB of live heap after a GC (collectable since 1.23); `Reset` on a timer that had already fired, without draining, fired after the new 100 ms and `Stop` returned false; the nil-channel merge loop merged both inputs and ended; a plain `break` inside a `select` only left the select (loop kept going, 5 receives) while `break loop` stopped after 2; a send on a closed channel inside `select` panicked even with a `default`; with both cases ready `select` chose the done channel 500 of 1000 times; `for { select { default: } }` spun freely. Timer behaviour change confirmed in https://go.dev/doc/go1.23.
