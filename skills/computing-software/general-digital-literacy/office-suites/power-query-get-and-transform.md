---
id: computing-software.general-digital-literacy.office-suites.power-query-get-and-transform
name: power-query-get-and-transform
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, sort-and-filter, power-query, get-and-transform, refresh-data, combine-files]
level: advanced
status: docs-checked
description: "Import and clean data with Excel Power Query: load from CSV, web or a folder, remove columns, change types, unpivot and refresh with one click."
sources:
  - https://support.microsoft.com/en-us/excel/about-power-query-in-excel
  - https://support.microsoft.com/en-us/office/connection-properties-9d3599a9-e9b3-461d-99b2-c5505ddae6e0
  - https://support.microsoft.com/en-us/accessibility/excel/keyboard-shortcuts-in-excel
  - https://support.microsoft.com/en-us/excel/import-and-shape-data-in-excel-for-mac-power-query
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Get and transform data (Power Query) basics

**When:** you receive the same messy export every week. Record the clean-up once, then **Refresh**.

## Load
**Data › Get Data** (the Get & Transform Data group) connects to the web, files, databases and
Excel tables in the workbook, and opens the Power Query Editor.

## Common steps (each becomes an *Applied Step* in the Query Settings pane)
- Each transformation is recorded as a step you can view and change.
- **Merge Queries** links rows from two queries by a common column (a lookup join); **Append
  Queries** stacks the rows of one query onto another.
- **Close & Load** (Home tab, Close group) loads the result; you can also right-click a query in
  the Queries & Connections pane and choose Load To.

## Refresh
**Data › Refresh All** (Ctrl+Alt+F5 on Windows). In the query's properties (Data › Queries &
Connections › Connections tab › right-click › Properties › Usage) you can set *Refresh every n
minutes*.

## Gotchas
- Steps reference column names; if the source renames a column, the step errors.
- Availability: Excel for Windows, Mac and the web, with narrower support on Mac and web; Excel 2016
  and 2019 for Mac do not support it.

## Verify
- [ ] Row count after load matches the source minus intended filters; refresh with a new file works.

## Checked

2026-10-27. Documentation checked against the current pages listed in sources. Microsoft About Power Query in Excel (Data tab, Get and Transform group; Applied Steps in Query Settings; Close and Load on the Home tab; Append stacks rows, Merge joins on a common column; available in Excel for Windows, Mac and the web, not in Excel 2016 or 2019 for Mac), Connection properties (Query Properties Usage tab, Refresh every n minutes), keyboard shortcuts (Ctrl+Alt+F5 refreshes all data).
Method: documentation only; no commands were run.
