---
id: computing-software.data-science-and-analytics.bi-tools.dax-time-intelligence
name: dax-time-intelligence
category: computing-software
field: data-science-and-analytics
product: bi-tools
tags: [dax-time-intelligence, totalytd-sameperiodlastyear, rolling-average-dax]
level: practitioner
status: docs-checked
description: "Compute year-to-date, prior-year comparisons and rolling windows using a date table marked as the Date Table."
sources:
  - https://learn.microsoft.com/dax/time-intelligence-functions-dax
  - https://learn.microsoft.com/dax/totalytd-function-dax
  - https://learn.microsoft.com/dax/datesinperiod-function-dax
  - https://learn.microsoft.com/dax/sameperiodlastyear-function-dax
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time intelligence
```dax
Sales YTD = TOTALYTD ( [Total Sales], 'Date'[Date] )
Sales PY = CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
YoY % = DIVIDE ( [Total Sales] - [Sales PY], [Sales PY] )
Sales 3M = CALCULATE ( [Total Sales], DATESINPERIOD ( 'Date'[Date], MAX ( 'Date'[Date] ), -3, MONTH ) )
```
## Gotchas
- Before using time-intelligence functions, mark a table containing a date column as the Date Table.
- TOTALYTD takes an optional filter and an optional `year_end_date` string (default December 31) for fiscal years, for example "6/30".
- DATESINPERIOD: a negative `number_of_intervals` shifts backward; the interval is an unquoted enumeration (DAY, MONTH, QUARTER, YEAR; WEEK only with a calendar reference). It is suited to pass as a CALCULATE filter.
## Verify
- [ ] Cross-check one month YTD with a manual sum.

## Checked
Confirmed on the time intelligence function list: the Date Table marking requirement and the existence and descriptions of TOTALYTD, SAMEPERIODLASTYEAR and DATESINPERIOD. Confirmed on the TOTALYTD page: argument order and year_end_date; on DATESINPERIOD: arguments, negative shift, unquoted enumeration, CALCULATE use. Removed: "contiguous Date table (no gaps)" and "use the Date table's column in visuals, not the fact table's", which the pages do not state.
Method: docs-checked 2026-11-09 against the Microsoft Learn pages for time intelligence functions, TOTALYTD, DATESINPERIOD and SAMEPERIODLASTYEAR (syntax and remarks read).
