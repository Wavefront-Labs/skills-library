---
id: computing-software.software-engineering.cobol.intrinsic-date-time
name: intrinsic-date-time
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, intrinsic-date-time, cobol-intrinsic, function-current-date, integer-of-date, date-of-integer, when-compiled]
level: practitioner
status: docs-checked
description: "Get the current timestamp and do date arithmetic with CURRENT-DATE, INTEGER-OF-DATE and DATE-OF-INTEGER."
sources:
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Date and time intrinsic functions
**Goal:** day arithmetic without Y2K bugs.
```cobol
01 WS-NOW.
   05 WS-YYYYMMDD PIC 9(8).
   05 WS-HHMMSSCC PIC 9(8).
   05 WS-GMT      PIC X(5).
MOVE FUNCTION CURRENT-DATE TO WS-NOW
COMPUTE WS-DAYS = FUNCTION INTEGER-OF-DATE(20251102)
COMPUTE WS-NEW  = FUNCTION DATE-OF-INTEGER(WS-DAYS + 30)
COMPUTE WS-GAP  = FUNCTION INTEGER-OF-DATE(WS-D2) - FUNCTION INTEGER-OF-DATE(WS-D1)
```
- `CURRENT-DATE` returns a 21-character structure: year, month, day, hour, minutes, seconds, hundredths of a second, then the GMT offset as a signed hours field plus minutes.
- `INTEGER-OF-DATE` converts a YYYYMMDD date to the number of days since 1600/12/31; `DATE-OF-INTEGER` converts back (DATE-OF-INTEGER(1) is 16010101, and 0 is returned for values below 1 or above 3067671).
- `INTEGER-OF-DAY` and `DAY-OF-INTEGER` do the same for Julian YYYYDDD.
- `WHEN-COMPILED`, `YEAR-TO-YYYY`, `DATE-TO-YYYYMMDD` and `DAY-TO-YYYYDDD` (windowing with an optional cutoff) are also available.

## Gotchas
- `CURRENT-DATE`'s time has hundredths of a second, not milliseconds.

## Self-check
`DATE-OF-INTEGER(INTEGER-OF-DATE(20240228) + 2)` must be 20240301 (2024 is a leap year).

## Checked
2026-11-02. Checked against the GnuCOBOL Programmer's Guide function entries CURRENT-DATE, DATE-OF-INTEGER, INTEGER-OF-DATE, INTEGER-OF-DAY and the function list. Removed: the MOD-based day-of-week recipe (not stated), and the claim that INTEGER-OF-DATE returns 0 for an invalid date (only DATE-OF-INTEGER's 0 result is documented).

Method: documentation only; no commands were run.
