---
id: computing-software.software-engineering.nim.times-datetime-and-formatting
name: times-datetime-and-formatting
category: computing-software
field: software-engineering
product: nim
tags: [times-datetime-and-formatting, stdlib-times, times, datetime, now, format, parse, utc, timezone, inzone, nim]
level: practitioner
status: docs-checked
description: "Get current time, build DateTime values, format and parse with format strings, and handle time zones."
sources:
  - https://nim-lang.org/docs/times.html
  - https://nim-lang.org/docs/monotimes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DateTime, now and formatting

Goal: work with dates correctly.

- `import std/times`; `let t = now()` (a `DateTime` in the local zone, shorthand for `getTime().local`), `getTime()` (a `Time`), `utc(t)`, `local(t)`, `t.inZone(utc())`.
- Construct: `dateTime(2025, mJan, 31, 12, 0, 0, zone = utc())`, or `initDateTime(monthday, month, year, hour, minute, second, zone)` (note the argument order).
- Fields: `t.year`, `t.month`, `t.monthday`, `t.weekday`, `t.yearday`, `t.hour`; ISO output `$t` or `t.format("yyyy-MM-dd'T'HH:mm:ss'Z'")`.
- Parse: `parse("2025-01-31", "yyyy-MM-dd", utc())`.
- Use `Time` for instants (`toUnix`, `fromUnix`) and `DateTime` for calendar fields.
- Elapsed time: `epochTime()`, `cpuTime()`, or `getMonoTime()` from `std/monotimes`; the docs warn that `now()` is unsuitable for benchmarking.

Gotchas:
- Format letters are case sensitive: `MM` is the two-digit month, `mm` the minute.

Verify: `$fromUnix(0).utc` gives `1970-01-01T00:00:00Z`.

## Checked

2026-11-02. Confirmed against lib/pure/times.nim (procs, format table, `fromUnix(0)` example, `now()` doc) and monotimes.nim. Removed: the TZ-database gotcha and the single-quote literal rule (not read in the format table).
Method: documentation only; no commands were run.
