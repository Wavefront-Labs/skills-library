---
id: computing-software.general-digital-literacy.office-suites.choosing-a-chart-type
name: choosing-a-chart-type
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, charts, chart-types, bar-chart, line-chart, pie-chart, scatter-plot, combo-chart, change-chart-type]
level: intro
status: docs-checked
description: "Pick the chart type that fits the question (comparison, trend, share, relationship), change chart type and avoid misleading pies, 3D and truncated axes."
sources:
  - https://support.microsoft.com/en-us/excel/change-the-chart-type-of-an-existing-chart
  - https://support.microsoft.com/en-us/office/excelexp/add-or-remove-a-secondary-axis-in-a-chart-in-excel
  - https://support.google.com/docs/answer/63824?hl=en
  - https://help.libreoffice.org/latest/en-US/text/schart/00/00000004.html
  - https://datavizcatalogue.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing the right chart type

**Goal:** the chart answers the reader's question at a glance.

| Question | Use | Avoid |
|---|---|---|
| Compare categories (sales by region) | **Bar/column**, sorted | Pie with many slices |
| Change over time (monthly visits) | **Line** (columns for few periods) | Unordered bars |
| Part of a whole, 2-5 parts | **Pie/doughnut** or 100% stacked bar | Pies over 5 slices |
| Relationship of two numbers | **Scatter** | Line chart of unsorted X |
| Two measures with different scales | **Combo** (column + line on secondary axis) | Two charts misaligned |
| Distribution | Histogram or box plot | Average alone |

Long category names? Use a horizontal **bar** chart so labels read without tilting.

## Change type
- Excel: select the chart › **Chart Design › Change Chart Type** (or right-click the chart area ›
  Change Chart Type). The **Combo** category sets a type per series and can put one on a secondary axis.
- Google Sheets: double-click the chart › **Setup** › *Chart type*.
- LibreOffice Calc: double-click the chart › **Format › Chart Type**.

## Honest charts
- Bar/column axes start at **zero**; a truncated axis exaggerates differences. Lines may start
  elsewhere if labelled clearly.
- No 3D effects: they distort sizes.
- Same colour for the same thing across charts; highlight the one bar that matters, grey the rest.
- Pie slices must add to 100%; don't pie "% satisfied" across unrelated questions.

## Verify
- [ ] Someone unfamiliar can say the main message in one sentence after 5 seconds.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365), Google Docs Editors Help and
  LibreOffice help (master) as published on that date: Change Chart Type on Chart Design and the chart
  area context menu, Combo with secondary axis, Sheets Setup › Chart type, Calc Format › Chart Type.

Method: documentation only; no commands were run.
