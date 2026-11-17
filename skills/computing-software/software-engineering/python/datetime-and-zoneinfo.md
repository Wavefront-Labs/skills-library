---
id: computing-software.software-engineering.python.datetime-and-zoneinfo
name: datetime-and-zoneinfo
category: computing-software
field: software-engineering
product: python
tags: [python, python-stdlib, python-datetime, zoneinfo, timezones, utc, iso-8601, dst]
level: practitioner
status: verified
description: "Handle dates and times safely: aware vs naive datetimes, UTC storage, zoneinfo conversions, DST gaps and folds, ISO 8601 parsing and monotonic timing."
sources:
  - https://docs.python.org/3/library/datetime.html
  - https://docs.python.org/3/library/zoneinfo.html
  - https://peps.python.org/pep-0495/
  - https://peps.python.org/pep-0615/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# datetime and zoneinfo

**Goal:** timestamps that are unambiguous, convert correctly across time zones and DST, and serialise losslessly.

## 1. Always aware, store UTC
```python
from datetime import datetime, timedelta, UTC     # UTC alias is 3.11+; else timezone.utc
from zoneinfo import ZoneInfo

now = datetime.now(UTC)                  # aware
local = now.astimezone(ZoneInfo("Europe/Paris"))
stamp = now.isoformat()                  # '2026-10-16T09:30:00.123456+00:00'
back = datetime.fromisoformat(stamp)     # 3.11+ parses most ISO 8601 incl. 'Z'
```
- `datetime.utcnow()` and `utcfromtimestamp()` return **naive** values and are deprecated (3.12). Never use them.
- Ordering naive against aware datetimes raises `TypeError` (`can't compare offset-naive and offset-aware datetimes`), which is a feature: fix the naive source. `==` does not raise: it returns `False`.

## 2. Wall-clock scheduling in a zone
```python
tz = ZoneInfo("America/New_York")
meeting = datetime(2026, 11, 1, 9, 0, tzinfo=tz)      # attach zone with tzinfo=, never .replace on aware UTC values
next_week = meeting + timedelta(days=7)               # same wall time 09:00, offset changes across DST
```
Arithmetic on aware datetimes in the same zone is wall-clock arithmetic; for exact elapsed time convert to UTC first.

## 3. DST gaps and folds (PEP 495)
- Gap: `2026-03-08 02:30` does not exist in New York; zoneinfo returns an object anyway (offset from before the gap). Normalise via round-trip through UTC and validate if user input.
- Fold: `2026-11-01 01:30` happens twice; `fold=0` = first (EDT), `fold=1` = second (EST).
```python
datetime(2026, 11, 1, 1, 30, tzinfo=tz, fold=1).utcoffset()   # -5:00
```

## 4. Dates, parsing and formatting
```python
from datetime import date
date.fromisoformat("2026-10-16"); date.today()        # local date, beware in servers
datetime.strptime("16/10/2026 14:05", "%d/%m/%Y %H:%M").replace(tzinfo=ZoneInfo("Europe/London"))
f"{now:%Y-%m-%d %H:%M %Z}"
```
Use ISO 8601 / RFC 3339 for interchange; `%Z` names are ambiguous for parsing.

## 5. Durations and timing
`timedelta` for calendar-free durations. Months/years need `dateutil.relativedelta`. For measuring elapsed time use `time.monotonic()` / `perf_counter()`, never wall clock (NTP adjustments).

## Gotchas
- `ZoneInfo` needs tz data: on Windows and slim containers install the `tzdata` package.
- Do not use fixed offsets (`timezone(timedelta(hours=-5))`) for places; offsets change with DST and law.
- `datetime.timestamp()` on a naive value assumes local time.
- Databases: use `timestamptz` (Postgres) and an aware driver configuration; MySQL `DATETIME` stores no zone.
- `datetime` is a subclass of `date`: `isinstance(dt, date)` is True; check `datetime` first.

## Verify
- Tests freeze time (time-machine/freezegun) on a DST transition day and assert UTC instants and displayed local times for both sides of the change.

## Checked
- Python 3.14.0: `isoformat` sample shape, `fromisoformat` accepting `Z` and basic format, `utcnow()`/`utcfromtimestamp()` returning naive values with `DeprecationWarning`, the naive-vs-aware ordering `TypeError` and `==` False, `2026-11-01 09:00` plus 7 days giving `09:00-05:00` with a 7-day UTC difference, the New York gap (offset before the gap, round trip to 03:30 EDT), `fold=1` giving -5:00 and `fold=0` -4:00, Paris and London conversions, `%Z` formatting and the `%Z` parse failure for `EST`, `isinstance(dt, date)`, fixed-offset versus zone hours, `UTC is timezone.utc`. `ZoneInfo('Europe/Paris')` failed with `No time zone found` on a Windows Python without the `tzdata` package. Release notes: `datetime.UTC` and broader `fromisoformat` in 3.11, `utcnow` deprecation in 3.12. Database and time-freezing advice is not re-tested.
