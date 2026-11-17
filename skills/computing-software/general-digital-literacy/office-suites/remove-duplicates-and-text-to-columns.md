---
id: computing-software.general-digital-literacy.office-suites.remove-duplicates-and-text-to-columns
name: remove-duplicates-and-text-to-columns
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, sort-and-filter, remove-duplicates, text-to-columns, split-text, data-cleanup, trim-whitespace, unique-function]
level: intro
status: docs-checked
description: "Clean imported lists by removing duplicate rows, splitting one column into several with Text to Columns or SPLIT, and trimming stray spaces."
sources:
  - https://support.microsoft.com/en-us/excel/get-started/filter-for-unique-values-or-remove-duplicate-values
  - https://support.microsoft.com/en-us/excel/get-started/split-text-into-different-columns-with-the-convert-text-to-columns-wizard
  - https://support.google.com/docs/answer/6325535
  - https://github.com/LibreOffice/help/blob/master/source/text/scalc/01/12090104.xhp
  - https://github.com/LibreOffice/help/blob/master/source/text/scalc/01/text2columns.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Remove duplicates and split text to columns

**Goal:** turn a messy pasted list into clean, one-value-per-cell data.

## Remove duplicates
- **Excel:** click in data › Data › **Remove Duplicates** › tick the columns that define a
  duplicate (e.g. only Email) › OK. A row counts as a duplicate only if all ticked columns match.
- **Google Sheets:** Data › Data cleanup › **Remove duplicates**. The same menu has *Trim
  whitespace* and *Cleanup suggestions*.
- **Calc:** Standard Filter › Options › *No duplications*.
- Non-destructive: `=UNIQUE(A2:C500)` (Microsoft 365, Excel 2021/2024, Sheets, LibreOffice 24.8+)
  lists distinct rows elsewhere.

## Split one column
- **Excel:** select the column › Data › **Text to Columns** › choose the delimiter and a
  destination. Make sure empty columns exist to the right, or data is overwritten.
- **Sheets:** Data › **Split text to columns**, or `=SPLIT(A2,",")`.
- **Calc:** Data › Text to Columns.

## Gotchas
- Excel judges duplicates by the displayed value, so the same date shown in two formats counts as
  unique; Sheets treats values that differ only in case as duplicates. Differences such as a
  trailing space are not matched: `TRIM` first (`=TRIM(A2)`).
- Remove Duplicates deletes rows permanently; Microsoft recommends copying the data first.
- Names don't split cleanly (van der Berg, two first names); check results by eye.

## Verify
- [ ] Row count after cleanup matches `=COUNTA(UNIQUE(...))` of the key column.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft pages on removing duplicates (Data, Remove Duplicates deletes permanently, copy the data first, a row is a duplicate only if all ticked columns match, judged by displayed value) and Text to Columns (Data, Text to Columns; leave empty columns to the right), Google Sheets help (Data, Data cleanup, Remove duplicates, Trim whitespace, Cleanup suggestions; Data, Split text to columns; values differing only in case count as duplicates), UNIQUE availability (Microsoft, Google, LibreOffice 24.8), LibreOffice help sources (Standard Filter options, No duplications; Data, Text to Columns).
Method: documentation only; no commands were run.
