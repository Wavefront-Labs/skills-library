---
id: computing-software.general-digital-literacy.office-suites.pivotcharts
name: pivotcharts
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, ss-charts, pivot-chart, pivot-tables, slicers]
level: intro
status: docs-checked
description: "Build a PivotChart in Excel or a chart from a pivot table in Google Sheets, filter it with field buttons and slicers, and keep it in sync as the data refreshes."
sources:
  - https://support.microsoft.com/en-us/excel/get-started/create-a-pivotchart
  - https://support.microsoft.com/en-us/excel/overview-of-pivottables-and-pivotcharts
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.microsoft.com/en-us/excel/get-started/create-a-pivottable-to-analyze-worksheet-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# PivotCharts

## Excel
- From data: click inside the table, **Insert > PivotChart**, choose where to place it, OK, then
  select the fields to display.
- From an existing pivot: click a cell in the PivotTable, **Insert > PivotChart**, pick a chart
  type, OK.
- Filtering the PivotTable (including with slicers) also filters the chart.
- New data: **Data > Refresh All** (Ctrl+Alt+F5 on Windows). An Excel table as the source picks up new
  rows when you refresh.
- Excel for Mac: some chart types (treemap, statistical, combo) do not work with PivotTables.

## Gotchas
- A PivotChart cannot be changed to an xy (scatter), stock or bubble chart; copy values to a
  normal range for those.
- Unlike a standard chart, a PivotChart's data range cannot be changed in the Select Data Source
  dialog; change the PivotTable instead.
- Changing the pivot layout changes the chart; make a second pivot for a second view.

## Verify
- [ ] Refresh after adding a test row and the chart changes accordingly.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft Create a PivotChart page (Insert, PivotChart from a table or from a PivotTable; filtering the PivotTable filters the chart; Mac and web notes), Overview of PivotTables and PivotCharts (a PivotChart cannot be changed to xy scatter, stock or bubble types), keyboard shortcuts (Ctrl+Alt+F5 refreshes all data), PivotTable page (Excel tables recommended as the source).
Method: documentation only; no commands were run.
