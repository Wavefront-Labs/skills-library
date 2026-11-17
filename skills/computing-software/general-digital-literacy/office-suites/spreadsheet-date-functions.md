---
id: computing-software.general-digital-literacy.office-suites.spreadsheet-date-functions
name: spreadsheet-date-functions
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, formulas, functions, date-functions, datedif, networkdays, edate]
level: practitioner
status: docs-checked
description: "Calculate ages, deadlines and working days in Excel and Google Sheets with TODAY, DATE, DATEDIF, EDATE, EOMONTH, NETWORKDAYS and WORKDAY."
sources:
  - https://support.microsoft.com/en-us/office/datedif-function-25dba1a4-2812-480b-84dd-8b32a451b35c
  - https://support.microsoft.com/en-us/excel/functions/networkdays-intl-function
  - https://support.microsoft.com/en-us/excel/functions/weekday-function
  - https://support.microsoft.com/en-us/excel/functions/workday-function
  - https://support.microsoft.com/en-us/excel/functions/days-function
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.microsoft.com/en-us/excel/date-systems-in-excel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Date functions

Dates are serial numbers counted from 1 January 1900 in Excel's 1900 date system, so you can
subtract and add them.

| Need | Formula |
|---|---|
| Today / now | `=TODAY()` / `=NOW()` |
| Build a date | `=DATE(2026,10,18)` (safe across locales) |
| Days between | `=B2-A2` (format result as Number) or `=DAYS(B2,A2)` (end date first) |
| Age in years | `=DATEDIF(A2,TODAY(),"y")` (also "m", "d", "ym", "yd") |
| Same day N months later | `=EDATE(A2,3)` |
| Last day of month | `=EOMONTH(A2,0)` |
| Working days between | `=NETWORKDAYS(A2,B2,Holidays)` |
| Deadline in 10 working days | `=WORKDAY(A2,10,Holidays)` |
| Weekend not Sat/Sun | `=NETWORKDAYS.INTL(A2,B2,7)` (7 = Fri/Sat weekend) |
| Parts | `=YEAR(A2)`, `=MONTH(A2)`, `=DAY(A2)`, `=WEEKDAY(A2,2)` (Mon=1), `=ISOWEEKNUM(A2)` |
| Day name | `=TEXT(A2,"dddd")` |

`Holidays` = a named range listing public holiday dates.

## Shortcuts
Ctrl+; enters the current date as a fixed value; on Windows Ctrl+Shift+: enters the current time.

## Gotchas
- Microsoft describes DATEDIF as a legacy function kept for Lotus 1-2-3 workbooks that can give
  incorrect results in some cases; it advises against the "MD" unit.
- Text that looks like a date ("03/04/2026" imported from CSV) will not calculate; check with
  `=ISNUMBER(A2)`. Convert with `=DATEVALUE(A2)` in a helper column, format as a date, paste values.
- 03/04 means 3 April in the UK and March 4 in the US; use DATE() or ISO `2026-04-03` input.
- A result like 45678 just needs a date format; ##### means the column is too narrow or the result
  is a negative date or time.

## Verify
- [ ] Spot-check one result by counting on a calendar, including a holiday.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft pages for DATEDIF (legacy function for Lotus 1-2-3 workbooks, unit codes, MD warning), NETWORKDAYS.INTL (weekend 7 = Friday and Saturday), WEEKDAY (return type 2 = Monday 1), WORKDAY (holidays argument), EDATE, EOMONTH, ISOWEEKNUM, DAYS (end date first), date systems (1900 system counts from 1 January 1900), Excel keyboard shortcuts (Ctrl+; date, Ctrl+Shift+: time), and the ##### error page; Convert dates stored as text (DATEVALUE steps).
Method: documentation only; no commands were run.
