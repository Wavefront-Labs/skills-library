---
id: computing-software.general-digital-literacy.office-suites.sparklines
name: sparklines
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, ss-formatting, sparklines, excel, google-sheets]
level: intro
status: docs-checked
description: "Add sparklines, tiny in-cell trend charts, in Excel or Google Sheets with the SPARKLINE function, and set markers and axis limits so rows compare fairly."
sources:
  - https://support.microsoft.com/en-us/excel/get-started/use-sparklines-to-show-data-trends
  - https://support.microsoft.com/en-us/office/analyze-trends-in-data-using-sparklines-be6579cf-a8e3-471a-a459-873614413ce1
  - https://support.google.com/docs/answer/3093289
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sparklines

## Excel
1. Select a blank cell next to the data (one per row).
2. **Insert > Sparklines > Line**, **Column** or **Win/Loss**.
3. Enter the data range (e.g. `B2:M2` for the row) and the location; OK.
4. On the Sparkline tab, tick the markers you want (for example high and low points).
- **Hidden & Empty Cells**: show empty cells as gaps, zeros or connect the points with a line, and
  choose whether hidden rows and columns are included.
- Sparklines update automatically when the source data changes.

## Google Sheets
- Formula: `=SPARKLINE(B2:M2)` and fill down.
- Options: `=SPARKLINE(B2:M2, {"charttype","column"; "ymin",0; "ymax",100})`.
- Chart types: `line` (default), `column`, `bar` (one value as a progress bar:
  `=SPARKLINE(C2,{"charttype","bar";"max",100})`), `winloss`.
- `ymin` and `ymax` set the vertical axis limits for line and column types; `max` sets the
  horizontal axis for bar.

## Use them well
- Best beside a table of figures to show trend direction at a glance; not for exact values.
- Win/loss suits positive/negative results (profit or loss months).
- Give rows the same scale (in Sheets, the same `ymin`/`ymax`) when you want them compared.

## Verify
- [ ] Rows that should be compared share the same axis limits.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft sparkline pages (Insert, Line, Column, Win/Loss; data range; Show group markers such as high and low points; Hidden & Empty Cells gaps, zero or connect), Google SPARKLINE help (charttype line default, bar, column, winloss; color, ymin, ymax, max, axis options; options syntax and the bar example with max).
Method: documentation only; no commands were run.
