---
id: computing-software.general-digital-literacy.office-suites.sorting-spreadsheet-data
name: sorting-spreadsheet-data
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, sort-and-filter, sort-data, multi-level-sort, custom-sort, sort-range, expand-selection]
level: intro
status: docs-checked
description: "Sort spreadsheet data by one or several columns without scrambling rows, including custom sort orders, in Excel, Google Sheets and LibreOffice Calc."
sources:
  - https://support.microsoft.com/en-us/excel/sort-data-in-a-range-or-table-in-excel
  - https://support.google.com/docs/answer/3540681?hl=en
  - https://help.libreoffice.org/latest/en-US/text/scalc/01/12030100.html
  - https://help.libreoffice.org/latest/en-US/text/scalc/00/00000412.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sorting data

**Goal:** reorder rows while keeping each row's values together.

## One column
- Excel: select **one cell** in the column › **Data › Sort & Filter › Sort A to Z** (or Z to A).
- Google Sheets: right-click the column letter › **Sort sheet A to Z** (whole sheet), or select the range ›
  **Data › Sort range › Advanced range sorting options** › tick *Data has header row* › choose the column.
- Calc: click in the column › **Data › Sort Ascending**.

## Several levels
- Excel: **Data › Sort** › *Sort by* the first column, then **Add Level** for the next (for example Region
  A-Z, then Amount largest to smallest). *Order* includes **Custom List** (for example High, Medium, Low;
  create your own under File › Options › Advanced › General › Edit Custom Lists). *My data has headers*
  keeps the header row out of the sort.
- Calc: **Data › Sort** › *Sort Key 1, 2, 3*; the dialog adds another key when you use the last one.

## The classic disaster
Selecting a single column and sorting it sorts **only that column**, so names no longer match their
numbers. Excel warns: choose **Expand the selection** (not *Continue with the current selection*). If it
happened, Undo immediately, or restore from version history.

## Gotchas
- Numbers stored as text sort as text, character by character ("A1", "A100", "A11").
- Blank cells always go last, in both ascending and descending sorts.
- Add a helper column `1,2,3...` before sorting if you may need the original order back.

## Verify
- [ ] Spot-check three rows: each name still matches its own values.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365), Google Docs Editors Help and
  LibreOffice help (master) as published on that date: quick sort from one cell, Sort dialog with Add
  Level and Custom List, Edit Custom Lists path, My data has headers, the Expand the selection warning,
  text and blank-cell sort order; Sheets Sort sheet and Sort range with header option; Calc Sort
  Ascending and Sort Key behaviour.

Method: documentation only; no commands were run.
