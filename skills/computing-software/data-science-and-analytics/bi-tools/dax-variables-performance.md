---
id: computing-software.data-science-and-analytics.bi-tools.dax-variables-performance
name: dax-variables-performance
category: computing-software
field: data-science-and-analytics
product: bi-tools
tags: [dax-variables, performance-analyzer, dax-studio]
level: advanced
status: docs-checked
description: "Use VAR/RETURN for readable and faster measures and diagnose slow visuals with Performance Analyzer and DAX query view."
sources:
  - https://learn.microsoft.com/power-bi/create-reports/desktop-performance-analyzer
  - https://learn.microsoft.com/dax/var-dax
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variables and tuning
```dax
Sales vs Target =
VAR s = [Total Sales]
VAR t = [Target]
RETURN IF ( NOT ISBLANK ( t ), DIVIDE ( s - t, t ) )
```
- A variable's value is calculated once and does not change when referenced again, so DAX does not recalculate it each time it is used; this improves readability and can improve performance.
- Variable names use a-z, A-Z, 0-9 only (not as first character), no delimiters or spaces, and cannot be reserved keywords or existing table names. A measure cannot refer to variables defined outside its own expression.
- Power BI Desktop: Optimize ribbon > Performance Analyzer > Start recording, interact with the report, then use Copy query or Run in DAX query view on a visual to time and inspect its DAX query. In the web, Edit the report, then View > Performance Analyzer.
- Durations are split into DAX query, Direct query, Visual display, Other and evaluated parameters; reported times include queue time on the UI thread. Export saves a .json file.
- DAX query performance depends on calculation complexity, the number of tables involved and their relationships.
## Verify
- [ ] Query duration before and after.

## Checked
Confirmed on the VAR page: evaluate-once behaviour and performance statement, naming rules, scoping rule. Confirmed on the Performance Analyzer page: ribbon and menu locations, recording, Copy query, Run in DAX query view, duration categories, JSON export, tip on complexity. Removed: the DAX Studio instruction (not on either page; replaced by DAX query view), the "prefer simple filters over FILTER / reduce cardinality" advice and the SUMX iterator warning, none stated in the cited pages.
Method: docs-checked 2026-11-09 against the VAR and Performance Analyzer pages on Microsoft Learn, both read in full.
