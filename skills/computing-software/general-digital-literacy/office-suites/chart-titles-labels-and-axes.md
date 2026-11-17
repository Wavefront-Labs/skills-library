---
id: computing-software.general-digital-literacy.office-suites.chart-titles-labels-and-axes
name: chart-titles-labels-and-axes
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, charts, chart-elements, chart-title, data-labels, legend, axis-titles, gridlines, axis-scale]
level: intro
status: docs-checked
description: "Add and edit chart titles, axis titles, data labels, legends, gridlines and axis options in Excel, Google Sheets and LibreOffice Calc charts."
sources:
  - https://support.microsoft.com/en-us/office/excelexp/add-or-remove-titles-in-a-chart
  - https://support.microsoft.com/en-us/office/change-the-display-of-chart-axes
  - https://support.google.com/docs/answer/63824?hl=en
  - https://support.google.com/docs/answer/9142593?hl=en
  - https://help.libreoffice.org/latest/en-US/text/schart/00/00000004.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chart titles, labels, legends and axes

**Goal:** a chart that explains itself without the spreadsheet next to it.

## Excel
- Chart title: select the chart › the **+** button at its top-right › tick *Chart Title*, then type in
  the title box.
- Axis titles: **Chart Design › Add Chart Element › Axis Titles**. Pie and doughnut charts have no axes,
  so they cannot show axis titles.
- Axis details (tick marks, label position, number format): **Add Chart Element › Axes › More Axis
  Options** opens the *Format Axis* pane.

## Google Sheets
Double-click the chart › **Customize**:
- *Chart & axis titles*: pick which title to edit.
- *Series*: data labels, colours, axis location, trendline.
- *Legend*: position and text.
- *Gridlines and ticks*: major and minor gridline counts.

## LibreOffice Calc
Double-click the chart to edit it, then **Insert › Titles**, **Insert › Legend** or **Insert › Data
Labels**. Axis scale: **Format › Axis › Y Axis** › *Scale* tab.

## Writing good titles
- Say the finding, not just the subject: "Online sales doubled this year" beats "Sales by channel".
- Axis titles include units: "Revenue (£ thousands)".
- One series? Delete the legend; the title says what it is.
- Data labels on a few key points beat a dense gridline grid.

## Verify
- [ ] Printed in greyscale, the chart is still readable and labelled.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365), Google Docs Editors Help and
  LibreOffice help (master) as published on that date: the + chart elements button for titles, Add Chart
  Element › Axis Titles and › Axes › More Axis Options, no axis titles on pie/doughnut, Sheets Customize
  sections, Calc Insert › Titles / Legend / Data Labels and Format › Axis › Y Axis › Scale.

Method: documentation only; no commands were run.
