---
id: computing-software.data-science-and-analytics.bi-tools.tableau-dashboard-design-performance
name: tableau-dashboard-design-performance
category: computing-software
field: data-science-and-analytics
product: bi-tools
tags: [tableau-dashboard-actions, tableau-performance-recording, dashboard-layout]
level: practitioner
status: docs-checked
description: "Use filter actions, fixed-size dashboards, efficient filters and the performance recorder to keep Tableau dashboards responsive."
sources:
  - https://help.tableau.com/current/pro/desktop/en-us/perf_checklist.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dashboards
- Most slow dashboards come from too many charts on one dashboard or too much data at once. Keep it simple, use fewer sheets, and let users drill down incrementally (guided analysis) with filter actions rather than many filters.
- Use fixed-size dashboards (they need no re-rendering for different window sizes). Use the same level of detail on multiple sheets to allow query batching.
- Reduce marks, hide unused fields, aggregate, and prefer extracts (with extract and data source filters) when real-time data is not needed.
- Start with the performance recorder to see where time goes (long-running queries, many queries, slow calculations, complex rendering); tune in Tableau Desktop first, as publishing to Tableau Server will not improve performance.
## Gotchas
- Filtering is one of the most common causes of slow workbooks. The Only Relevant Values option runs a query each time other filters change, filters applied to multiple worksheets create multiple queries, and Keep only / Exclude on discrete items can be heavy. Enable Show Apply Button on multi-select filters.
- Context filters run before other filters (forcing an order of operations) but no longer improve query performance.
- COUNTD is one of the slowest functions; booleans and integers are faster than strings and dates; MIN and MAX perform better than AVG and ATTR.
- Custom geocoding can massively inflate workbook size.
## Verify
- [ ] Recording shows no single step dominating load time.

## Checked
Confirmed on the Tableau workbook performance checklist: general tips, data source advice, view and dashboard advice, filtering and calculation notes, performance recorder, Server advice. Removed: the dead dashboard actions source (404) and every claim that depended on it (highlight and URL actions, layout advice), the Help menu path for the recorder, the "key numbers top-left" and "one audience" design claims, and "quick filters showing all values" (the page names Only Relevant Values instead).
Method: docs-checked 2026-11-09 against the Tableau Help performance checklist page, read in full.
