---
id: computing-software.general-digital-literacy.office-suites.dates-showing-as-numbers-or-hashes
name: dates-showing-as-numbers-or-hashes
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, cell-formatting, dates-as-numbers, hash-signs, number-stored-as-text, date-format]
level: intro
status: docs-checked
description: "Fix spreadsheet cells that show ##### or numbers like 45678 instead of dates, and dates stuck as text that will not sort or calculate."
sources:
  - https://support.microsoft.com/en-us/office/how-to-correct-a-error-bf801d0a-2a6e-44bd-a70e-0f780ae8f11e
  - https://support.microsoft.com/en-us/excel/convert-dates-stored-as-text-to-dates
  - https://support.microsoft.com/en-us/excel/set-automatic-data-conversions
  - https://support.microsoft.com/en-us/excel/date-systems-in-excel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dates showing as numbers or #####

## ##### in a cell
- Column too narrow: drag the right border of the column header wider (or use Shrink to fit, or a
  shorter date format such as Short Date).
- Negative date/time result (e.g. end before start): Excel cannot show negative dates or times;
  check the formula order.

## 45678 instead of a date
The value is right; the format is General/Number. Select, then **Ctrl+1 › Number › Date** (or
Home › Number Format › Short Date).

## Date that will not sort or calculate (it is text)
Symptoms: left-aligned, a green triangle in the cell corner (it marks a date stored as text),
`=ISNUMBER(A2)` is FALSE, sorting is alphabetical.
Fixes:
1. `=DATEVALUE(A2)` in a blank helper cell (General format), fill down, copy the results and paste
   them as values over the text dates, then apply a date format.
2. Mixed separators (2026.10.18): Find & Replace `.` with `/` first.

## Avoid it next time
- Excel's *Automatic Data Conversion* options (File › Options › Data) can stop entries such as
  JAN1 turning into dates, leading zeros being dropped and long numbers being cut to 15 digits.
  They do not apply to data imported through Power Query.
- Format a column as Text before typing IDs that look like dates.

## Verify
- [ ] Sort the column oldest to newest: order is chronological, and `=ISNUMBER()` is TRUE throughout.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft ##### page (column too narrow; negative date or time; Short Date from the Number Format menu), Convert dates stored as text (green triangle marks text dates; DATEVALUE then paste values and format), Set automatic data conversions (File, Options, Data; options for leading zeros, long numbers, E notation and letter-number text such as JAN1 becoming dates; not applied to Power Query imports).
Method: documentation only; no commands were run.
