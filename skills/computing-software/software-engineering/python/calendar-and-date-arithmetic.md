---
id: computing-software.software-engineering.python.calendar-and-date-arithmetic
name: calendar-and-date-arithmetic
category: computing-software
field: software-engineering
product: python
tags: [python, py-time, calendar-date-arithmetic, calendar, monthrange, timedelta, business-days, relativedelta, isocalendar]
level: practitioner
status: docs-checked
description: "Do calendar math safely: month ends, add months, weekdays, ISO weeks, leap years, business days and age calculations with datetime and calendar."
sources: ["https://docs.python.org/3/library/calendar.html", "https://docs.python.org/3/library/datetime.html#timedelta-objects"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Calendar and date arithmetic

```python
import calendar
from datetime import date, timedelta

calendar.monthrange(2028, 2)            # (1, 29): weekday of the 1st (Mon=0), days in month
calendar.isleap(2100)                   # False (century rule)
calendar.weekday(2026, 11, 3)           # 1 -> Tuesday

def end_of_month(d): return d.replace(day=calendar.monthrange(d.year, d.month)[1])

def add_months(d: date, n: int) -> date:
    y, m = divmod(d.month - 1 + n, 12)
    y, m = d.year + y, m + 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))     # Jan 31 + 1 month = Feb 28/29

d = date(2026, 11, 3)
d + timedelta(days=30)                  # timedelta has days/seconds only, no months or years
d.isocalendar()                         # (year, week, weekday): ISO week; year can differ from d.year near New Year
(date(2027, 1, 1) - d).days             # difference in days

def age(born: date, today: date) -> int:
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def business_days(start: date, end: date, holidays=frozenset()):
    d = start
    while d < end:
        if d.weekday() < 5 and d not in holidays: yield d
        d += timedelta(days=1)
```

## Gotchas
- `date.replace(month=...)` raises `ValueError` on Jan 31 -> Feb; clamp the day.
- Feb 29 + 1 year: `replace(year=...)` fails in non-leap years; decide whether to use Feb 28 or Mar 1 per business rule and write a test.
- `%U`, `%W` (week numbers) differ from ISO `%V`; use `%G-W%V-%u` for ISO.
- Naive vs aware datetimes: adding a `timedelta` to an aware datetime does no time zone adjustment (the wall-clock fields move); compute in UTC when you need elapsed time.
- `calendar.setfirstweekday` is global state.
- 3.12+ `calendar.Month`/`calendar.Day` enums (`calendar.MONDAY`).

## Verify
- [ ] Table-driven tests: month ends, leap days, year boundaries (Dec 31 + 1 day), ISO week 53 years like 2026-12-31.

## Checked

- 2026-11-03: checked against the CPython docs `library/calendar.rst` and `library/datetime.rst`: `monthrange`, `isleap`, `weekday` (0 is Monday), `setfirstweekday`, 3.12 `Month`/`Day` enums, `isocalendar`, `%U`/`%W` versus `%G`/`%V`/`%u`, `date.replace`, no time zone adjustment in aware datetime arithmetic.
- Removed: third-party package suggestions (dateutil, numpy, pandas, holidays) and the 23/25-hour DST remark.

Method: documentation only; no commands were run.
