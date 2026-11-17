---
id: computing-software.software-engineering.cobol.accept-from-date
name: accept-from-date
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, accept-from-date, cobol-dates, date-yyyymmdd, y2k-windowing]
level: practitioner
status: docs-checked
description: "Read system date/time with ACCEPT and choose 4-digit-year forms over the legacy 2-digit forms."
sources:
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ACCEPT FROM DATE, DAY, TIME and century windowing
**Goal:** get the date without a Y2K bug.
```cobol
ACCEPT WS-DATE-6  FROM DATE            *> YYMMDD
ACCEPT WS-DATE-8  FROM DATE YYYYMMDD
ACCEPT WS-JULIAN  FROM DAY YYYYDDD
ACCEPT WS-TIME    FROM TIME            *> HHMMSSnn
ACCEPT WS-DOW     FROM DAY-OF-WEEK
```
- Formats: `DATE` yymmdd, `DATE YYYYMMDD` yyyymmdd, `DAY` yyddd (Julian), `DAY YYYYDDD` yyyyddd, `TIME` hhmmssnn including hundredths of a second.
- `FUNCTION CURRENT-DATE` returns a 21-character structure: year, month, day, hour, minutes, seconds, hundredths, and a signed GMT offset in hours and minutes.
- Windowing 2-digit years: `FUNCTION YEAR-TO-YYYY(yy [, yy-cutoff [, yy-execution-time]])`, `DATE-TO-YYYYMMDD(yymmdd [, ...])` and `DAY-TO-YYYYDDD(yyddd [, ...])`; `TEST-DATE-YYYYMMDD` and `TEST-DAY-YYYYDDD` check values.

## Gotchas
- Two-digit `ACCEPT FROM DATE` gives no century; use the YYYYMMDD form or a windowing function.

## Self-check
Compare `ACCEPT FROM DATE YYYYMMDD` with `FUNCTION CURRENT-DATE(1:8)`; they must match.

## Checked
2026-11-02. Checked against the GnuCOBOL Programmer's Guide (ACCEPT FROM DATE/TIME, CURRENT-DATE, YEAR-TO-YYYY, DATE-TO-YYYYMMDD, DAY-TO-YYYYDDD). Removed: the earlier gated note (IBM EVALUATE text was misattributed), the `1 = Monday` day-of-week value, IBM DATEPROC statements, and the advice on test-date overrides.

Method: documentation only; no commands were run.
