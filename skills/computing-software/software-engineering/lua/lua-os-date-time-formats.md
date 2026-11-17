---
id: computing-software.software-engineering.lua.lua-os-date-time-formats
name: lua-os-date-time-formats
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-date-time, os-date-time-formats]
level: practitioner
status: docs-checked
description: "Format and compute dates with os.date and os.time and handle time zones and normalisation."
sources: ["https://www.lua.org/manual/5.4/manual.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# os.date formats, time zones and date arithmetic
- `os.date("*t", t)` returns a table with `year month day hour min sec wday yday isdst` (wday 1 is Sunday; `isdst` may be absent); a leading `!` formats in UTC.
- `os.time(t)` normalises out-of-range fields to their valid ranges, so adding 30 to `day` works for date arithmetic; `hour` defaults to 12 when absent.
Verify: add 31 days to 2026-10-15 and check the month rollover.

## Checked

Date: 2026-11-02. Confirmed on Lua 5.4 manual os.date and os.time (*t fields, '!' prefix, field normalisation, default hour 12). Removed as not confirmed: strftime example format, the UTC offset trick, luatz and locale remarks.

Method: documentation only; no commands were run.
