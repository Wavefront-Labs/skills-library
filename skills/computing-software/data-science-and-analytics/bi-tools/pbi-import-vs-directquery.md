---
id: computing-software.data-science-and-analytics.bi-tools.pbi-import-vs-directquery
name: pbi-import-vs-directquery
category: computing-software
field: data-science-and-analytics
product: bi-tools
tags: [import-vs-directquery, composite-model, aggregation-tables]
level: advanced
status: docs-checked
description: "Choose Power BI storage modes by data size, freshness and source capability, and mitigate DirectQuery limits with composite models and aggregations."
sources:
  - https://learn.microsoft.com/power-bi/connect-data/desktop-directquery-about
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage modes
- Import: the default recommendation; it uses Power BI's in-memory engine and has the richest feature set. Move beyond Import only for specific constraints (latency, size, governance, security, architecture).
- DirectQuery: data stays in the source and is queried at report time. Visual refresh latency depends entirely on the source (plus network or gateway overhead). Aim for common visual refresh under 5 seconds; over 30 seconds degrades usability.
- You cannot toggle a whole Import model to DirectQuery; build a composite model (for example Import dimensions plus DirectQuery fact tables, shared dimensions set to Dual). Tables switch between DirectQuery, Import and Dual only if all applied transformations fold.
- Mitigations: automatic aggregations and manual aggregation tables, incremental refresh, hybrid tables, dynamic M parameters, Dual mode for shared dimensions.
## Gotchas
- Power Query folding is required for scalable DirectQuery; transformations must condense into a single native query.
- Modelling limits: no automatic date hierarchy (create a Date table), time precision limited to seconds, calculated columns limited to row-level expressions that fold, no PATH functions, no clustering.
- Reporting limits: text columns over 32,764 characters unsupported; measure filters, TopN, Median, multi-select slicers and totals (especially DistinctCount) can add queries.
- Service limits: a 4-minute timeout per query; default 10 DirectQuery connections per file (adjust in Options, DirectQuery); upper limit 10 active connections per source for Pro, depends on semantic model SKU for Premium.
- Unless SSO is configured, DirectQuery uses stored credentials for all viewers; define RLS in the semantic model. With RLS each user runs separate tile queries, and RLS can reduce cache reuse.
## Verify
- [ ] Performance Analyzer shows acceptable visual query times.

## Checked
Confirmed on the DirectQuery page: import-by-default guidance, latency targets, composite model and table-mode switching rules, mitigation features, folding requirement, modelling and reporting limitations, connection defaults and limits, 4-minute timeout, SSO and RLS behaviour. Read lines 1-100 selectively and lines 99-246 in detail. Removed: Import size reduction advice (remove columns, cardinality, datetime precision, auto date/time), "size limits by capacity" for Import, none of which the page states.
Method: docs-checked 2026-11-09 against the Microsoft Learn DirectQuery about page (downloaded as text; grep plus lines 99-246 read).
