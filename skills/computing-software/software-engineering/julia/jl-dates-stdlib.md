---
id: computing-software.software-engineering.julia.jl-dates-stdlib
name: jl-dates-stdlib
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-dates, dates-stdlib]
level: practitioner
status: docs-checked
description: "Parse, format and do arithmetic with Dates and handle time zones with TimeZones.jl."
sources: ["https://docs.julialang.org/en/v1/stdlib/Dates/", "https://docs.julialang.org/en/v1/base/base/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Date, DateTime, periods and TimeZones.jl
- `using Dates; Date(2026, 11, 2)`, `Date("2026-11-02")`, `Date("02/11/2026", dateformat"dd/mm/yyyy")`.
- Adding a `Month` clamps to month-end (January 31 plus one month is February 28); `Dates.value`, `dayofweek` (1 is Monday), `firstdayofmonth`, `lastdayofmonth`.
- `DateTime` has no time zone; time zones need TimeZones.jl.
- `now()` is local time, `now(UTC)` is UTC; `time()` returns the system time in seconds since the epoch.
Verify: round-trip format and parse.

## Checked

Date: 2026-11-02. Confirmed on Julia Dates stdlib docs (month clamping, dayofweek, firstdayofmonth, lastdayofmonth, Dates.value, naive DateTime, now(UTC)) and Base docs (time()). Removed as not confirmed: the `ZonedDateTime(dt, tz"...")` call form.

Method: documentation only; no commands were run.
