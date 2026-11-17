---
id: mathematics.applied-data-analysis-and-visualization.excel.pivot-tables-and-descriptive-analysis
name: pivot-tables-and-descriptive-analysis
category: mathematics
field: applied-data-analysis-and-visualization
product: excel
tags: [excel, microsoft-excel, spreadsheet, pivot-table, pivottable, excel-table, structured-references, groupby, pivotby, sumifs, countifs, averageifs, median, percentile, quartile, frequency, histogram, analysis-toolpak, descriptive-statistics, slicers, calculated-field, show-values-as, distinct-count, data-model, power-query, refresh, google-sheets, libreoffice-calc, data-analysis]
level: practitioner
status: draft
description: "Summarise data correctly in Excel: tables as the source, pivot tables with the right aggregation, distinct counts and % views, formula cross-checks, medians and histograms, and refresh traps."
sources: ["Microsoft Support: Create a PivotTable to analyze worksheet data", "Microsoft Support: GROUPBY and PIVOTBY functions", "Microsoft Support: Use the Analysis ToolPak"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pivot tables and descriptive analysis in Excel

**Goal:** go from a raw sheet to correct grouped summaries and distributions, with a
cross-check so a wrong pivot doesn't make it into a report. (Lookups, dynamic arrays and
auditing for finance models are in
`business-finance.corporate-finance.excel.finance-lookups-dynamic-arrays-and-auditing`.)

## 1. Prepare the source
- One header row, one record per row, no blank rows/columns, no merged cells, no
  subtotal rows inside the data.
- Convert it to a **Table**: select a cell › `Ctrl+T` › name it (Table Design › Table Name,
  e.g. `Sales`). Pivots and formulas built on a Table grow with new rows; ranges don't.
- Check types: numbers stored as text (green triangle, left-aligned) are silently ignored
  by SUM and counted, not summed, by pivots. Fix with Data › Text to Columns › Finish, or `VALUE()`.

## 2. Build the pivot
Insert › PivotTable › From Table/Range › New worksheet.
- Rows = grouping, Values = measure, Columns = a second grouping (keep it small),
  Filters/**Slicers** for interactive subsetting.
- **Check the aggregation:** a numeric field defaults to Sum; if any cell is blank or text
  it defaults to **Count**. Value Field Settings › Summarize Values By.
- **Average** in a pivot is the mean of underlying rows, not the mean of subgroup averages —
  usually what you want; know which one you are reporting.
- **Distinct count:** tick "Add this data to the Data Model" when creating the pivot; then
  Value Field Settings offers Distinct Count (desktop Excel for Windows; availability on
  Mac/web has differed — check your version).
- **Show Values As** › % of Grand Total / % of Column Total / % Difference From — for shares
  and change without helper columns.
- Group dates (right-click › Group › Months/Years) and numbers (bins of fixed width).
- **Median isn't a pivot aggregation** (outside the Data Model with DAX). Use formulas.

## 3. Formula cross-checks and extra statistics
- Grouped totals: `=SUMIFS(Sales[Amount], Sales[Region], "North")`, `COUNTIFS`, `AVERAGEIFS`.
  Pick two pivot cells and reproduce them — if they disagree, find out why before sharing.
- Median by group (Excel 365/2021): `=MEDIAN(FILTER(Sales[Amount], Sales[Region]="North"))`.
- Excel 365 also has `GROUPBY` and `PIVOTBY` — formula-based pivots that recalc
  automatically (e.g. `=GROUPBY(Sales[Region], Sales[Amount], MEDIAN)`); rollout started
  in 2024, so confirm your build has them.
- Spread: `STDEV.S` (sample) vs `STDEV.P` (population) — sample is usually right.
  `QUARTILE.INC`/`PERCENTILE.INC` match most textbooks; `.EXC` versions differ at small n.

## 4. Distributions
- Insert › Chart › Histogram (2016+), then set bin width explicitly (Format Axis) — the
  automatic bins can hide shape.
- Or `=FREQUENCY(data, bins)` (spills in 365) for a table you control.
- **Analysis ToolPak** (File › Options › Add-ins › Excel Add-ins › Analysis ToolPak):
  Data › Data Analysis › Descriptive Statistics gives a summary block. Its output is
  **static** — it doesn't update when data changes.

## 5. Refresh and other traps
- Pivots don't update automatically: Data › **Refresh All** (`Ctrl+Alt+F5`) after data changes.
  Consider PivotTable Options › Data › "Refresh data when opening the file".
- `GETPIVOTDATA` formulas appear when you click a pivot cell from a formula — useful
  (stable) or annoying (turn off via PivotTable Analyze › Options › Generate GetPivotData).
- Filtered/hidden rows: `SUBTOTAL`/`AGGREGATE` ignore them, `SUM` doesn't.
- Google Sheets and LibreOffice Calc have pivots with similar concepts but different menus;
  GROUPBY/PIVOTBY are Excel-only.

## Uncertainty notes
Menu paths are from recent Windows Excel 365; Mac and web differ in places. Function
availability (GROUPBY/PIVOTBY, distinct count on Mac) changes with updates — verify on the
user's build.

## Verify
- [ ] Source is a named Table with clean types (no numbers-as-text).
- [ ] Every value field shows the intended aggregation (Sum vs Count).
- [ ] At least two pivot figures reproduced with SUMIFS/COUNTIFS.
- [ ] Medians/percentiles from formulas, with function variant noted.
- [ ] Pivot refreshed after the last data change; static ToolPak output re-run if data changed.
