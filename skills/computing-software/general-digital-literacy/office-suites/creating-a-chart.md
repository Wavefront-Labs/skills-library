---
id: computing-software.general-digital-literacy.office-suites.creating-a-chart
name: creating-a-chart
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, charts, create-chart, recommended-charts, insert-chart, chart-sheet, quick-analysis]
level: intro
status: docs-checked
description: "Create a chart from spreadsheet data in Excel, Google Sheets or LibreOffice Calc, starting from a clean data layout and using recommended charts."
sources:
  - https://support.microsoft.com/en-us/excel/get-started/create-a-chart-from-start-to-finish
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.google.com/docs/answer/63824?hl=en
  - https://help.libreoffice.org/latest/en-US/text/schart/00/00000004.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating a chart

**Goal:** a chart that shows the data correctly on the first try.

## Lay out the data
- First column = categories or dates (labels); following columns = one series each, with a header.
- No blank rows, no total row inside the range (select without it), numbers stored as numbers.

## Create
- **Excel:** select the range including headers › **Insert › Recommended Charts** (or pick a type; the
  *All Charts* tab lists every type). Keys: `Alt+F1` creates an embedded chart of the current range,
  `F11` creates it on a separate chart sheet, `Ctrl+Q` opens Quick Analysis for the selection.
- **Google Sheets:** select the cells › **Insert › Chart**. Double-click the chart to open the editor
  (*Setup* and *Customize*).
- **LibreOffice Calc:** select the cells › **Insert › Chart** to start the chart wizard (type, data range,
  data series, elements).

## Gotchas
- A label column plotted as a data series means the labels are not set: fix it in the data range / header
  options before styling.
- `Alt+F1` gives the default chart type, which may not suit the data; check it.

## Verify
- [ ] Hover a few points: values match the cells.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365), Google Docs Editors Help and
  LibreOffice help (master) as published on that date: Insert › Recommended Charts and All Charts,
  Alt+F1 / F11 / Ctrl+Q, Sheets Insert › Chart and editor tabs, Calc Insert › Chart wizard.

Method: documentation only; no commands were run.
