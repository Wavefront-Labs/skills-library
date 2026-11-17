---
id: computing-software.general-digital-literacy.office-suites.conditional-formatting
name: conditional-formatting
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, spreadsheets, cell-formatting, conditional-formatting, highlight-cells-rules, colour-scales, data-bars, custom-formula-rule, duplicate-values]
level: intro
status: docs-checked
description: "Highlight cells automatically by value with conditional formatting rules, colour scales, data bars, duplicates and custom formulas in Excel, Sheets and Calc."
sources:
  - https://support.microsoft.com/en-us/excel/use-conditional-formatting-to-highlight-information-in-excel
  - https://support.microsoft.com/en-us/excel/use-data-bars-color-scales-and-icon-sets-to-highlight-data
  - https://support.google.com/docs/answer/78413
  - https://github.com/LibreOffice/help/blob/master/source/text/scalc/01/05120000.xhp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Conditional formatting

**Goal:** make overdue, high, low or duplicate values stand out automatically.

## Excel
Select the range › Home › **Conditional Formatting**:
- Highlight Cells Rules, including **Duplicate Values**.
- **Data Bars** (longer bar = higher value), **Color Scales**, **Icon Sets** (three to five
  categories split by thresholds).
- New Rule › *Use a formula*: the formula starts with `=` and must return TRUE or FALSE, e.g.
  whole row red when column E is "Overdue": select A2:H100, rule `=$E2="Overdue"` (dollar on the
  column only).
- Manage Rules shows order and ranges; a rule higher in the list takes precedence.

## Google Sheets
Format › **Conditional formatting** › Apply to range › *Single color* (Format cells if... with a
condition, including **Custom formula is** `=$E2="Overdue"`) or *Color scale*.

## LibreOffice Calc
Format › **Conditional**. Each condition applies a cell style, and the style of the first
condition that is true is used; conditional formats do not overwrite manual formatting.

## Gotchas
- Too many colours carry no meaning; one or two rules usually do the job, and don't rely on
  colour alone (add a status column) for colour-blind readers.

## Verify
- [ ] Change a value across the threshold: formatting switches on and off.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft conditional formatting pages (Home, Conditional Formatting, Highlight Cells Rules, Duplicate Values; data bars, colour scales, icon sets; formula rules start with = and return TRUE or FALSE; higher rules in Manage Rules take precedence), Google Sheets help (Format, Conditional formatting; Single color and Color scale; Custom formula is), LibreOffice help sources (Format, Conditional; conditions apply cell styles, first true condition wins).
Method: documentation only; no commands were run.
