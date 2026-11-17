---
id: computing-software.general-digital-literacy.office-suites.chart-trendlines
name: chart-trendlines
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, charts, trendline, linear-trend, moving-average, forecast]
level: practitioner
status: docs-checked
description: "Add a linear, moving-average or exponential trendline to an Excel or Google Sheets chart, show R-squared, and forecast forward carefully."
sources:
  - https://support.microsoft.com/en-us/office/excelexp/add-a-trend-or-moving-average-line-to-a-chart
  - https://support.google.com/docs/answer/6075154?hl=en&co=GENIE.Platform%3DDesktop
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trendlines

## Excel
1. Select the chart and add a **Trendline** from the chart elements. If the chart has more than one
   series and none is selected, Excel asks which series to use (Add Trendline dialog).
2. Open the **Format Trendline** pane (Format › Current Selection › Format Selection) and pick a type:
   **Exponential**, **Linear**, **Logarithmic**, **Polynomial**, **Power** or **Moving Average** (set
   the period).
3. Set **Forward** / **Backward** to project the line beyond the data; you can also name the trendline.
- A moving average has fewer points than the series: total points minus the period.
- On a scatter chart a moving average follows the order of the x values; sort them first.

## Google Sheets
Double-click the chart › **Customize › Series** › tick **Trendline** (bar, line, column or scatter
charts). Types: linear, exponential, polynomial (choose degree), logarithmic, power series, moving average
(choose periods). Options include labels and **R squared** (closer to 1 = closer fit; only available when
the chart has a legend).

## Gotchas
- Polynomial trendlines bend wildly outside the data; avoid long forecasts.
- A trend is not a cause; label forecasts as estimates.

## Verify
- [ ] The slope makes sense in real units (for example +120 sales per month).

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365) and Google Docs Editors Help as
  published on that date: Excel trendline types, Format Trendline pane, Forward/Backward forecast, moving
  average point count and scatter ordering; Sheets trendline chart types, trendline types and the R
  squared legend requirement.

Method: documentation only; no commands were run.
