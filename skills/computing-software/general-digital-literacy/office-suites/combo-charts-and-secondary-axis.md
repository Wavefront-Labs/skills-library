---
id: computing-software.general-digital-literacy.office-suites.combo-charts-and-secondary-axis
name: combo-charts-and-secondary-axis
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, charts, secondary-axis, combo-chart, dual-axis, chart-types]
level: practitioner
status: docs-checked
description: "Plot two measures with different scales, such as revenue and margin %, as a combo chart with a secondary axis in Excel or Google Sheets."
sources:
  - https://support.microsoft.com/en-us/office/excelexp/add-or-remove-a-secondary-axis-in-a-chart-in-excel
  - https://support.microsoft.com/en-us/office/excelexp/add-or-remove-titles-in-a-chart
  - https://support.google.com/docs/answer/9142593?hl=en
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Combo charts and a secondary axis

**When:** two series with very different values or mixed kinds of data (price and volume, £ sales and %
margin). On one axis, the small series is a flat line at zero.

## Excel
1. Select the chart › **Chart Design › Change Chart Type** › **Combo** › *Clustered Column - Line on
   Secondary Axis*.
2. Tick **Secondary Axis** for the series to move, set its type to **Line** › OK.
3. Add **axis titles** for both axes (Chart Design › Add Chart Element › Axis Titles) so readers know
   which is which.
4. To remove the secondary axis, click it and press Delete.

## Google Sheets
Double-click the chart › Setup › Chart type **Combo chart** (lines and bars). Then **Customize › Series**
› pick the series › change its axis location.

## Gotchas
- Dual-axis charts can mislead: two arbitrary scales can make any two lines look correlated. Start
  both at zero or show two small charts side by side when the relationship matters.
- Colour each axis label to match its series.

## Verify
- [ ] Both series readable, each axis titled with units, legend matches the colours.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365) and Google Docs Editors Help as
  published on that date: Change Chart Type › Combo › Clustered Column - Line on Secondary Axis, the
  Secondary Axis checkbox, deleting the axis, Add Chart Element › Axis Titles, Sheets combo chart and
  series axis location.

Method: documentation only; no commands were run.
