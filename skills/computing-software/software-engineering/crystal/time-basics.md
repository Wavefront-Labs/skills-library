---
id: computing-software.software-engineering.crystal.time-basics
name: time-basics
category: computing-software
field: software-engineering
product: crystal
tags: [time-basics, time, time-now, time-span, monotonic, time-arithmetic, duration, measure, epoch, unix, crystal]
level: intro
status: docs-checked
description: "Create Time values, compute with Time::Span and Time::MonthSpan, compare, measure elapsed time with monotonic clocks."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time construction and arithmetic

Goal: do time math correctly.

- `Time.utc` now in UTC; `Time.local` local; `Time.utc(2024, 3, 1, 12, 0)`; `Time.unix(secs)`; `t.to_unix`, `t.to_unix_ms`.
- Spans: `5.minutes`, `1.5.hours`, `Time::Span.new(days: 1)`; `t + 3.days`, `t - other` returns Span, `t + 2.months` (MonthSpan), `t.shift(months: 1)`.
- Elapsed: `Time.monotonic` or `Time.measure { work }` (monotonic, not affected by clock changes) instead of subtracting wall clock times.
- Parts: `t.year`, `t.month`, `t.day_of_week`, `t.day_of_year`; `t.at_beginning_of_day`, `t.at_end_of_month` (generated per interval).
- `sleep 100.milliseconds`.

Gotchas:
- `Time.local` depends on the TZ env var and tzdata.
- Month arithmetic clamps day 31 to month end.
- `Time::Span#total_seconds` is a Float64; `seconds`, `minutes` etc. return the component part.

Verify: `Time.utc(2024,1,31) + 1.month` gives Feb 29, 2024.

## Checked

Date 2026-11-03. Confirmed Time.utc, Time.local (location defaults to Location.local), Time.unix, Time.unix_ms, Time.monotonic, Time.measure, to_unix, to_unix_ms, shift, + and - with MonthSpan (day clamped to the last valid day of the month, as the doc describes for 2007-05-31 minus 1.month), day_of_week, day_of_year, at_beginning_of_* and at_end_of_* macros, and Time::Span#total_seconds in the Time and Time::Span source. Reworded the unverified span gotcha.

Method: documentation only; no commands were run.
