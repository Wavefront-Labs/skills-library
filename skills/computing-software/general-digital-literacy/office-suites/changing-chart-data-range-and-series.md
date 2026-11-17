---
id: computing-software.general-digital-literacy.office-suites.changing-chart-data-range-and-series
name: changing-chart-data-range-and-series
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, charts, chart-data-range, select-data, chart-series, switch-row-column, ms-excel, google-sheets]
level: intro
status: docs-checked
description: "Change which cells a chart plots: edit the data range, add, remove or rename series, switch rows and columns, and set labels in Excel, Google Sheets and Calc."
sources:
  - https://support.microsoft.com/en-us/office/change-the-data-series-in-a-chart
  - https://support.microsoft.com/en-us/excel/get-started/create-a-chart-from-start-to-finish
  - https://support.google.com/docs/answer/63824?hl=en
  - https://help.libreoffice.org/latest/en-US/text/schart/01/wiz_data_range.html
  - https://help.libreoffice.org/latest/en-US/text/schart/01/wiz_data_series.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Change a chart's data range and series

**Goal:** the chart shows exactly the rows and columns you mean.

## Excel
- Click the chart › **Chart Design › Select Data** (or right-click the chart › *Select Data*). This
  selects the chart's data range and opens **Select Data Source**.
  - **Legend Entries (Series)**: pick a series and edit its *Name* and *Y values*, or rearrange series.
- **Chart Design › Switch Row/Column** when series and categories are the wrong way round.
- **Chart filters** (beside the chart) show or hide individual series and categories without changing
  the source range.

## Google Sheets
Double-click the chart › **Setup**:
- *Data range*: click the grid icon and select the cells.
- Headers in rows: *Use row N as headers*. Headers in columns: *Switch rows / columns* and *Use column N
  as headers*.

## LibreOffice Calc
Double-click the chart, then **Format › Data Ranges**:
- *Data Range* tab: one source range (it may combine several rectangular ranges), series in rows or
  columns, *First row as label* / *First column as label*.
- *Data Series* tab: change each series' range and label separately, and the range of the categories.

## Gotchas
- A label column (years, IDs) plotted as a data series means it is not set as labels: use the header
  options above.
- Totals rows inside the range dwarf every other bar; exclude them.

## Verify
- [ ] Legend names come from header cells, not "Series1".

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365), Google Docs Editors Help and
  LibreOffice help (master) as published on that date: Select Data / Select Data Source and Legend
  Entries editing, Switch Row/Column on Chart Design, chart filters, Sheets Setup data range and header
  options, Calc Format › Data Ranges with Data Range and Data Series tabs and first row/column labels.

Method: documentation only; no commands were run.
