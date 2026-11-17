---
id: computing-software.general-digital-literacy.office-suites.filtering-spreadsheet-data
name: filtering-spreadsheet-data
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, sort-and-filter, filter-data, autofilter, filter-views, slicers, clear-filter, number-filters]
level: intro
status: docs-checked
description: "Show only matching rows with AutoFilter, number/text/date filters, Google Sheets filter views and slicers, and clear filters so nobody misses hidden rows."
sources:
  - https://support.microsoft.com/en-us/excel/get-started/filter-data-in-a-range-or-table-in-excel
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.microsoft.com/en-us/excel/functions/subtotal-function
  - https://support.google.com/docs/answer/3540681?hl=en
  - https://support.google.com/docs/answer/9245556?hl=en
  - https://help.libreoffice.org/latest/en-US/text/scalc/00/00000412.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Filtering data

**Goal:** see only the rows you care about, without deleting anything.

## Turn filters on
- Excel: click in the data › **Data › Filter** (`Ctrl+Shift+L` toggles AutoFilter). Arrows appear in the
  header row.
- Google Sheets: select the range › **Data › Create a filter** (or right-click › Create a filter).
- LibreOffice Calc: **Data › AutoFilter** (`Ctrl+Shift+L`).

## Use them
- Click a header arrow › untick values, or use **Text Filters / Number Filters / Date Filters**
  (Between, Less Than, Top 10...). Filtering several columns combines them.
- A changed filter icon on the header shows that a filter is applied.
- The Excel filter list shows only the first 10,000 unique entries.

## Clear
Excel: header arrow › **Clear Filter From "<column>"**; select **Data › Filter** again to remove all
filters. Sheets: **Data › Remove filter**.

## Shared sheets
In Google Sheets a normal filter is seen by **everyone** with access, and editors can change it. Use
**Data › Create filter view** for a filter that applies only to your view; save it with *Save View* and
share its link (copy the URL) if others need it. Viewers can make a temporary filter view that is not
saved.

## Slicers
Excel and Google Sheets both offer slicers: clickable filter buttons for tables, charts and pivot tables.

## Gotchas
- `SUM` still includes rows a filter hides; `=SUBTOTAL(9,B2:B500)` totals only the rows the filter
  shows (`109` also skips rows hidden by hand).
- A forgotten filter makes people think data is missing. Clear filters before saving and sharing.

## Verify
- [ ] The visible row count matches what you expect for the filter.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365), Google Docs Editors Help and
  LibreOffice help (master) as published on that date: Data › Filter and Ctrl+Shift+L, Number/Text/Date
  filters and Top 10, Clear Filter From, 10,000-entry list limit, SUBTOTAL 9/109 and filtered rows,
  Sheets Create a filter / Remove filter / Create filter view / sharing a view link / temporary views,
  Sheets slicers, Calc Data › AutoFilter and its shortcut.

Method: documentation only; no commands were run.
