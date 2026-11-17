---
id: computing-software.general-digital-literacy.office-suites.chart-styles-and-colours
name: chart-styles-and-colours
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, ss-charts, chart-styles, chart-colours, chart-formatting]
level: intro
status: docs-checked
description: "Restyle a chart in Excel or Google Sheets: chart styles, colouring single series or points, removing clutter, and saving a reusable chart template (.crtx)."
sources:
  - https://support.microsoft.com/en-us/excel/get-started/create-a-chart-from-start-to-finish
  - https://support.microsoft.com/en-us/excel/save-a-custom-chart-as-a-template
  - https://support.google.com/docs/answer/63824?hl=en
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Chart styles and colours

## Excel
- Click the chart › **Chart Design** tab › pick a style from the gallery. A chart style is a set of
  complementary colours and effects applied to the whole chart.
- Reuse a look: right-click the chart › **Save as Template** (saves a `.crtx` chart template). Apply it
  later from the **Templates** folder on the *All Charts* tab of Insert Chart, or on an existing chart via
  Chart Design › Change Chart Type › Templates.
- A chart template stores its own colours: charts made from it keep the template's colours, not the
  current document theme's.

## Google Sheets
- Double-click chart › **Customize** › *Chart style* for the overall look (and *Reset layout* there).
- Single bar or point: right-click it on the chart › **Format Data Point**.

## Design rules that work
- Grey for context, one strong colour for the thing you are talking about.
- Remove chart junk: heavy gridlines, 3D effects, shadows, borders and redundant legends (label lines
  directly).
- Use colour-blind-safe palettes (avoid red/green pairs; vary lightness too).
- Keep the same colour for the same category across all charts in a report.

## Verify
- [ ] Chart still readable printed in greyscale and the key series stands out.

## Checked
- 2026-10-27, against Microsoft Support (Excel for Microsoft 365) and Google Docs Editors Help as
  published on that date: Chart Design style gallery, Save as Template (.crtx), Templates folder on All
  Charts and via Change Chart Type, template colour behaviour, Sheets Customize › Chart style and Format
  Data Point.

Method: documentation only; no commands were run.
