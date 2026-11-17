---
id: computing-software.data-science-and-analytics.bi-tools.tableau-relationships-extracts
name: tableau-relationships-extracts
category: computing-software
field: data-science-and-analytics
product: bi-tools
tags: [tableau-relationships, tableau-extracts, tableau-joins-vs-relationships, tableau-dashboards]
level: practitioner
status: docs-checked
description: "Choose relationships over joins, build extracts with filters and incremental refresh, and keep data source granularity clear."
sources:
  - https://help.tableau.com/current/pro/desktop/en-us/datasource_relationships_learnmorepage.htm
  - https://help.tableau.com/current/pro/desktop/en-us/extracting_data.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data sources
- Relationships are the recommended first approach: no up-front join type, tables stay separate in the logical layer, and Tableau builds the appropriate joins per viz from the fields in use, querying only needed tables. Use joins (in the physical layer, via double-clicking a logical table) only when you need to; joined physical tables are merged into one fixed table that can drop unmatched values or duplicate aggregates when fields sit at different levels of detail.
- Relationships need matching data types on the related fields, cannot use geographic fields, circular relationships, or published data sources. Data source filters limit join culling. Multi-fact relationship models are available from version 2024.2.
- Extracts use the .hyper format (.tde is deprecated). They give offline access in Tableau Desktop, and can be filtered, aggregated (with date roll-up), limited to top N rows or sampled to shrink them; keep the default logical tables storage to keep those options.
- Refresh an extract fully (replaces all content) or incrementally (only new rows since the last refresh, based on a column). Incremental refresh is not available if Aggregation is enabled; you cannot append to extracts with more than one logical table.
## Gotchas
- Know the grain of each table; joins on non-unique keys or fields at different levels of detail can duplicate aggregate values.
- Connecting directly to a .hyper file loses table structure and relationships (stored in the data source file) and the link back to the original source, so it cannot be refreshed.
## Verify
- [ ] Total sales in Tableau equals the source system total.

## Checked
Confirmed on the relationships page: relationships versus joins behaviour and recommendation, requirements and limitations. Confirmed on the extract page: .hyper format, offline access, filters/aggregation/top N/sampling, full versus incremental refresh and its limits, direct .hyper connection caveats. Removed: "live connections move cost to the source database" (not stated) and the scheduled refresh wording, which the page does not cover; the extract page was read selectively (grep and refresh/aggregation sections), not every section.
Method: docs-checked 2026-11-09 against the Tableau Help relationships-vs-joins page (grep and requirement sections) and extract data page (selected sections).
