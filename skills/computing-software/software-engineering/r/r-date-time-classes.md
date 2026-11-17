---
id: computing-software.software-engineering.r.r-date-time-classes
name: r-date-time-classes
category: computing-software
field: software-engineering
product: r
tags: [r, r-dates, date-time-classes]
level: practitioner
status: docs-checked
description: "Parse, format and do arithmetic on dates and times with correct time zones."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/DateTimeClasses.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Date, POSIXct, POSIXlt and time zones
- `POSIXct` is the signed number of seconds since the beginning of 1970 in UTC; a non-empty `tzone` attribute sets how it is converted to `POSIXlt` and printed.
- `POSIXlt` is a named list of vectors with components `sec min hour mday mon year wday yday isdst`.
Verify: print one POSIXct value under two `tz` settings.

## Checked

Date: 2026-11-02. Confirmed on ?DateTimeClasses (POSIXct seconds since 1970 UTC, tzone attribute and display, POSIXlt components). Removed as not confirmed on that page: as.Date format strings, difftime units, seq by month, lubridate advice and silent NA parsing.

Method: documentation only; no commands were run.
