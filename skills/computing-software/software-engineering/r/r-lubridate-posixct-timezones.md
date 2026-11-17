---
id: computing-software.software-engineering.r.r-lubridate-posixct-timezones
name: r-lubridate-posixct-timezones
category: computing-software
field: software-engineering
product: r
tags: [r, lubridate-posixct-timezones]
level: advanced
status: draft
description: "Parse and manipulate R date-times with as.POSIXct, tz handling, lubridate parsers, periods vs durations."
sources: ["https://cran.r-project.org/doc/manuals/r-release/R-lang.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Date-times
- `as.Date("2024-03-01")`, `as.POSIXct("2024-03-01 12:00", tz = "UTC")`; `format(x, "%Y-%m-%d %H:%M")`; `difftime(a, b, units = "days")`.
- lubridate: `ymd_hms()`, `with_tz()` (same instant, new display) vs `force_tz()` (same clock time, new instant), `floor_date`, `%m+%`.
- Periods (`months(1)`) are calendar-based; durations (`ddays(1)`) are fixed seconds.
- Always store UTC; the default tz is the system tz.
Verify: DST-day addition differs between `days(1)` and `ddays(1)`.
