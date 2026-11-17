---
id: computing-software.general-digital-literacy.office-suites.pivot-tables-basics
name: pivot-tables-basics
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, sort-and-filter, pivot-tables, pivottable, summarise-data, refresh-pivot, group-dates, value-field-settings]
level: intro
status: docs-checked
description: "Summarise a list with a PivotTable in Excel, Google Sheets or LibreOffice Calc: rows, columns, values, filters, grouping by month and refreshing after changes."
sources:
  - https://support.microsoft.com/en-us/excel/get-started/create-a-pivottable-to-analyze-worksheet-data
  - https://support.microsoft.com/en-us/office/refresh-pivottable-data-6d24cece-a038-468a-8176-8b6568ca9be2
  - https://support.microsoft.com/en-us/excel/get-started/group-or-ungroup-data-in-a-pivottable
  - https://support.microsoft.com/en-us/excel/change-the-source-data-for-a-pivottable
  - https://support.google.com/docs/answer/7572895
  - https://github.com/LibreOffice/help/blob/master/source/text/scalc/guide/datapilot_createtable.xhp
  - https://github.com/LibreOffice/help/blob/master/source/text/scalc/guide/datapilot_updatetable.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PivotTable basics

**Goal:** turn thousands of rows into a summary (sales by region by month) in a minute.

## Prepare
One header row, no blank rows or columns, one record per row. Ideally format it as an Excel table
first, which Microsoft recommends as the source because new rows are picked up when you refresh.

## Create
- **Excel:** click in data › Insert › **PivotTable**. Drag fields into Rows (Region), Columns
  (Month), Values (Amount) and Filters (Year).
- **Google Sheets:** Insert › Pivot table, then add rows, columns, values and filters in the editor.
- **Calc:** Insert › Pivot Table › *Current selection*; drag the field buttons into the layout
  areas (Filters, Column Fields, Row Fields, Data Fields).

## Adjust
- **Group dates (Excel):** right-click a value in the PivotTable › Group, then set the interval
  (for example months and years). Sheets: right-click a date cell › **Create pivot date group**.

## Refresh
After the source changes, Excel PivotTables need refreshing: right-click › **Refresh**, or Refresh All
to update every PivotTable in the workbook. In Calc choose **Data › Pivot Table › Refresh**.

## Gotchas
- If the source was a plain range, rows added below it are outside the pivot; change the source
  (PivotTable Analyze › Change Data Source) or use an Excel table.
- Don't type over pivot cells; build any extra calculations beside it.

## Verify
- [ ] Grand total equals `=SUM()` of the source column.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft PivotTable pages (Insert, PivotTable; Excel tables recommended so new rows are picked up on refresh; no blank rows or columns; right-click Refresh and Refresh All; Group via right-click; Change Data Source on the Analyze tab), Google Sheets help (Create pivot date group), LibreOffice help sources (Insert, Pivot Table, Current selection; Data, Pivot Table, Refresh recalculates after source changes).
Method: documentation only; no commands were run.
