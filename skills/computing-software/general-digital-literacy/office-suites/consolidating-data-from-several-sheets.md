---
id: computing-software.general-digital-literacy.office-suites.consolidating-data-from-several-sheets
name: consolidating-data-from-several-sheets
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, ss-data, consolidate-data, 3d-reference, combine-sheets]
level: intro
status: docs-checked
description: "Combine figures from several worksheets or workbooks into one summary with 3D SUM references, Data > Consolidate, IMPORTRANGE, or by stacking lists with VSTACK."
sources:
  - https://support.microsoft.com/en-us/excel/consolidate-data-in-multiple-worksheets
  - https://support.microsoft.com/en-us/office/create-a-3-d-reference-to-the-same-cell-range-on-multiple-worksheets-40ca91ff-9dcb-4ad1-99d2-787d0bc888b6
  - https://support.microsoft.com/en-us/office/vstack-function-a4b86897-be0f-48fc-adca-fcc10d795a9c
  - https://support.google.com/docs/answer/3093340
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Combine data from several sheets

## Same layout on every sheet: 3D reference
- Sheets Jan, Feb, Mar with totals in B5: `=SUM(Jan:Mar!B5)`. Inserting, copying, deleting or
  moving sheets relative to the first and last sheet changes what the formula includes.
- Tip: add blank sheets named `Start` and `End` and use `=SUM(Start:End!B5)`; drag sheets in and out
  of the sandwich.

## Different layouts: Data > Consolidate (Excel)
1. On a summary sheet, click the top-left destination cell.
2. **Data > Consolidate**. Function: Sum (the default), Average, Count...
3. Add each source range. Each range should be a list with headers in the first row and no blank
   rows or columns.
4. *Create links to source data* makes the result update when the sources change; it is not
   available when the source and destination are on the same sheet.

## Stack lists into one table
- Microsoft 365 and Excel 2024: `=VSTACK(Jan!A2:D100, Feb!A2:D100)` appends the ranges vertically.

## Other workbooks
- Excel workbook links can pull data from other workbooks (see Microsoft's "Create workbook links").
- Google Sheets: `=IMPORTRANGE("spreadsheet URL","Jan!A1:D50")`; the first time, click *Allow
  access* (the source's owner must grant it).

## Gotchas
- 3D references add the same cell on each sheet, so every sheet needs the same layout.
- Without *Create links to source data* the consolidated result does not update.
- Keep data as one long table where possible; pivots then do the summarising.

## Verify
- [ ] Summary total equals the sum of each sheet's total checked by hand once.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft Consolidate data and 3-D reference pages (SUM(Sales:Marketing!B3) pattern, sheets moved relative to the end sheets change the result, Create links to source data, same-sheet limitation, source ranges with headers and no blank rows or columns, SUM default function), VSTACK page (Microsoft 365 and Excel 2024), Google IMPORTRANGE help (Allow access prompt, permission needed from the source).
Method: documentation only; no commands were run.
