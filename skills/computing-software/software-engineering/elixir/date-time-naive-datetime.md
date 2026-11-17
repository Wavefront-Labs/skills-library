---
id: computing-software.software-engineering.elixir.date-time-naive-datetime
name: date-time-naive-datetime
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, date, time, naivedatetime, datetime, utc, iso8601, date-diff, date-add, date-range, date-time-types, elixir-datetime]
level: practitioner
status: docs-checked
description: "Use Date and DateTime: parse and format ISO 8601, compare, compute differences, add and shift durations."
sources: ["https://hexdocs.pm/elixir/DateTime.html", "https://hexdocs.pm/elixir/Date.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Date, Time, NaiveDateTime and DateTime

**Goal:** do date arithmetic without the time zone traps.

```elixir
Date.utc_today() ; DateTime.utc_now()
{:ok, dt, offset} = DateTime.from_iso8601("2026-11-02T10:00:00+02:00")   # converted to UTC; offset 7200
Date.from_iso8601!("2026-11-02") ; Date.new!(2026, 11, 2)
Date.add(~D[2026-11-02], 7) ; Date.diff(~D[2026-11-09], ~D[2026-11-02])  #=> 7
DateTime.add(dt, 3600, :second) ; DateTime.diff(a, b, :millisecond)
DateTime.compare(a, b)  # :lt | :eq | :gt   (don't use < on structs)
DateTime.to_unix(dt) ; DateTime.from_unix!(1_700_000_000)
Date.range(~D[2026-01-01], ~D[2026-01-05])
DateTime.to_iso8601(dt)
Date.shift(~D[2026-01-31], month: 1)   # calendar-aware shift; DateTime.shift/3 also exists
```

## Rules
- `<`/`>`/`==` on date structs are structural comparisons over the struct fields; use `compare/2`, `before?/2` or `after?/2`, or `Enum.sort(dates, Date)`.
- `DateTime.from_naive/3` attaches a time zone to a `NaiveDateTime`; `DateTime.from_iso8601/1` converts the string to UTC and returns the offset in seconds.
- Zones other than UTC need a time zone database (see the time zones skill).
- `Date.add/2` adds days; use `Date.shift/2` or `DateTime.shift/3` with a duration such as `month: 1` for calendar-aware shifting.

## Self-check
`DateTime.diff(a, b)` defaults to seconds; pass a unit for finer precision.

## Checked
2026-11-03: confirmed against the Date and DateTime module docs on hexdocs (function names and arities, diff and add default unit `:second`, `from_iso8601` converting to UTC with an offset in seconds, `compare/2` versus structural operators, `shift`, `Date.range/2`, `to_unix`/`from_unix!`). Removed: `NaiveDateTime.utc_now`, `Calendar.strftime`, `System` time calls, the Ecto `:utc_datetime` advice and the Timex remark (not on the pages read).
Method: documentation only; no commands were run.
