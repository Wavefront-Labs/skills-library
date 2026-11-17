---
id: computing-software.software-engineering.d.d-datetime-parsing-and-formatting
name: d-datetime-parsing-and-formatting
category: computing-software
field: software-engineering
product: d
tags: [d-datetime-parsing-and-formatting, std-datetime, date-parsing, date-formatting, iso-8601, formattedread, strftime, fromisoextstring, parsertc, date-format, d]
level: practitioner
status: docs-checked
description: "Parse dates from ISO strings, handle non-ISO formats manually (std.format formattedRead, std.regex), and format with std.format since SysTime lacks strftime."
sources:
  - https://dlang.org/phobos/std_datetime_date.html
  - https://dlang.org/phobos/std_datetime_systime.html
  - https://dlang.org/phobos/std_format.html
  - https://dlang.org/phobos/core_stdc_time.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parsing and formatting dates (ISO 8601, custom formats, std.format)

Goal: read and write dates in the formats you need.

- Built in: ISO 8601 via `fromISOString`, `fromISOExtString`, `toISOString`, `toISOExtString`; also `toSimpleString`.
- Custom parse: `std.format.formattedRead` reads an input range according to a format string, e.g. `int y, m, d; "2025/03/01".formattedRead!"%d/%d/%d"(y, m, d); auto date = Date(y, m, d);`.
- Custom format: `writefln("%04d-%02d-%02d", dt.year, dt.month, dt.day)`; `dt.month` is the `Month` enum (`Month.oct` prints as the enumerator name) and `dayOfWeek` returns `DayOfWeek` (`DayOfWeek.mon`).
- C-style: `core.stdc.time` declares `strftime`, which works on a C `tm` struct (you must fill it yourself).
- Unix epoch: `SysTime(unixTimeToStdTime(secs))` or `SysTime.fromUnixTime(secs, UTC())`.
- ISO week: `Date.isoWeek` and `isoWeekYear`.

Verify: unittest parsing and formatting round-trip for the leap day 2024-02-29.

## Checked

2026-11-03. Confirmed against: std.datetime.date, std.datetime.systime, std.format and core.stdc.time reference pages.

Removed because the pages read did not confirm it: RFC 2822 and `datefmt` package claim, locale/English-only claim, `Date.fromISOExtString` trailing-text claim, `to!string(dt.month)` result claim, `isoWeek` locale claim.

Method: documentation only; no commands were run.
