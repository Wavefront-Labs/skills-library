---
id: computing-software.software-engineering.go.time-package-monotonic-durations-and-locations
name: time-package-monotonic-durations-and-locations
category: computing-software
field: software-engineering
product: go
tags: [go, golang, go-time, monotonic-clock, time-zones, tzdata, duration, time-formatting, timers, go-time-rand]
level: practitioner
status: verified
description: "Use Go's time package correctly: monotonic readings, Equal vs ==, the 2006-01-02 layout, time zones and embedded tzdata, Duration pitfalls and Go 1.23 timer semantics."
sources: ["https://pkg.go.dev/time", "https://pkg.go.dev/time/tzdata", "https://go.dev/doc/go1.23#timer-changes"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# The time package: monotonic clock, Durations and locations

**Goal:** measure elapsed time reliably, store and compare instants correctly, and format and
parse times in the right zone.

## Monotonic vs wall clock
`time.Now()` carries both a wall reading and a monotonic reading. `Sub`, `Since`, `Until`,
`Before`, `After` use the monotonic part when both values have it, so elapsed time is immune to
NTP jumps and DST.
```go
start := time.Now()
doWork()
elapsed := time.Since(start)     // correct even if the wall clock is stepped
```
`t.Add` keeps the monotonic reading; `t.Round(0)` (the canonical way), `Truncate`, `AddDate`,
`In`, `Local`, `UTC` and serialisation strip it. Values parsed or unmarshalled never have one.

## Comparing instants
- Use `t1.Equal(t2)`, not `==`. `==` compares location pointer and monotonic reading too, so the
  same instant in UTC and in local time are not `==`.
- Do not use `time.Time` as a map key for the same reason; use `t.UnixNano()` or normalise with
  `t.UTC().Round(0)`.
- Zero value: `t.IsZero()`, not comparison with `time.Time{}` after a round trip through a DB.

## Formatting and parsing
Layouts use the reference time `Mon Jan 2 15:04:05 MST 2006` (1 2 3 4 5 6 -7):
```go
t.Format(time.RFC3339)            // 2026-10-18T14:03:00Z
t.Format("2006-01-02 15:04")
time.Parse(time.RFC3339, s)       // zone taken from the string
time.ParseInLocation("2006-01-02 15:04", s, loc)  // no zone in string -> interpret in loc
time.DateOnly, time.TimeOnly, time.DateTime        // Go 1.20 constants
```
`time.Parse` with a layout lacking a zone returns UTC, which surprises people parsing local times.

## Locations
```go
loc, err := time.LoadLocation("Australia/Sydney")
t.In(loc)
```
`LoadLocation` reads the system tz database; minimal containers (scratch, distroless-static) lack
it and return an error. Fix: `import _ "time/tzdata"` (embeds about 410 KB; the Windows `-tags timetzdata` binary grew from 2.40 MB to 2.81 MB on Go 1.25.1) or build with
`-tags timetzdata`. Store and transmit in UTC, convert to user zones at the edges; store the IANA zone
name alongside future local events (meetings) because offsets change.

## Durations
- `time.Duration` is int64 nanoseconds. `time.Sleep(5)` sleeps 5 ns; write `5 * time.Second`.
- Multiplying by a variable needs conversion: `time.Duration(n) * time.Millisecond`.
- `time.ParseDuration("1h30m")` for config; it does not accept days (`d`).
- Calendar arithmetic (months, DST-aware days) uses `t.AddDate(0, 1, 0)`, not `Add(24*time.Hour)`.
  `AddDate` normalises: Jan 31 + 1 month = Mar 3 (or 2).

## Timers (Go 1.23 changes)
With `go 1.23`+ in go.mod: unstopped, unreferenced `Timer`/`Ticker` are garbage-collected, and their
channels are unbuffered so `Reset`/`Stop` guarantee no stale value is received afterwards. The old
"drain the channel before Reset" dance is unnecessary. Behaviour depends on the go.mod `go` line
(`GODEBUG=asynctimerchan=1` restores the old one).

## Testability
Inject a clock (`now func() time.Time`) or use `testing/synctest` (Go 1.25 stable), in which
`time.Sleep` and timers advance a fake clock instantly inside the bubble.

## Verify
- [ ] Elapsed-time metrics use `time.Since` on a `time.Now()` value, not parsed timestamps.
- [ ] Times persisted in UTC; `LoadLocation` works in the production image.
- [ ] No `==` on `time.Time` (staticcheck and code search).

## Checked
- Go 1.25.1: `Now()` and `Add` keep the monotonic reading; `Round(0)`, `Truncate`, `AddDate`, `In`, `Local`, `UTC` and parsed values do not; the same instant in UTC and Sydney is `!=` but `Equal`, and the Sydney value is not found as a map key; layout and `DateOnly`/`TimeOnly`/`DateTime` constants; `Parse` without a zone gives UTC and `ParseInLocation` interprets in the location (`+1100 AEDT`); `Duration(5)` prints `5ns`; `ParseDuration("1h30m")` works and `1d` fails with `unknown unit "d"`; `AddDate` Jan 31 plus a month is Mar 3 (Mar 2 in a leap year) and across the Sydney DST change `AddDate` gave 12:00 while `Add(24h)` gave 13:00; with `go 1.22` an unstopped timer left a stale value after `Reset` (channel cap 1) while `go 1.23` did not (cap 0); `testing/synctest.Test` advanced a 10-hour sleep instantly. The minimal-container `LoadLocation` failure was not reproduced (this machine falls back to GOROOT's zoneinfo).
