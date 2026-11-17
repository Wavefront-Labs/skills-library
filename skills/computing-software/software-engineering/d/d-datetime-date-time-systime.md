---
id: computing-software.software-engineering.d.d-datetime-date-time-systime
name: d-datetime-date-time-systime
category: computing-software
field: software-engineering
product: d
tags: [d-datetime-date-time-systime, std-datetime, systime, datetime, date, timeofday, clock-currtime, iso-extended-string, unix-time, std-datetime-date, d]
level: practitioner
status: docs-checked
description: "Model dates and times with Date, TimeOfDay, DateTime, SysTime and Clock.currTime, arithmetic with add!/roll!, comparisons, ISO and RFC formats and conversions to Unix time."
sources:
  - https://dlang.org/phobos/std_datetime_date.html
  - https://dlang.org/phobos/std_datetime_systime.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Date, TimeOfDay, DateTime and SysTime

Goal: create, compare and format timestamps.

- Types: `Date(2025, 3, 1)`, `TimeOfDay(13, 5)` (hour, minute, second = 0), `DateTime(2025, 3, 1, 13, 5, 0)` (no zone), `SysTime(DateTime, TimeZone)` (an instant plus a zone). Now: `Clock.currTime` (local, `LocalTime()` by default) or `Clock.currTime(UTC())` style with a `TimeZone` argument.
- Arithmetic: `d + dur!"days"(30)`, `d.add!"months"(1)` (`AllowDayOverflow.yes` by default; pass `AllowDayOverflow.no` to clamp to the end of the month), `d.roll!"days"(5)` (rolling does not affect larger units), `d2 - d1` returns a `Duration`, `d.dayOfWeek`, `d.dayOfYear`, `d.isLeapYear`, `d.endOfMonth`.
- Strings: `toISOString`, `toISOExtString`, `toSimpleString`; parse with `Date.fromISOExtString("2025-03-01")` and `SysTime.fromISOExtString("2025-03-01T13:05:00Z")`.
- Unix time: `SysTime.fromUnixTime(secs, UTC())`, `st.toUnixTime()`, `std.datetime.systime.stdTimeToUnixTime` / `unixTimeToStdTime`.
- Compare with `<` and `==`; sorting works.

Gotchas:
- `DateTime` has no time zone; do not mix it with `SysTime` implicitly.
- `Date` has no `+` for months; use `add!"months"` or `roll!`.

Verify: unittest adds one month to Jan 31 with `AllowDayOverflow.no` and checks the clamp.

## Checked

2026-11-03. Confirmed against: std.datetime.date and std.datetime.systime reference pages.

Removed because the pages read did not confirm it: the `Clock.currTime` zone-database remark; the exact literal strings for ISO output are kept only where the pages show the same format.

Method: documentation only; no commands were run.
