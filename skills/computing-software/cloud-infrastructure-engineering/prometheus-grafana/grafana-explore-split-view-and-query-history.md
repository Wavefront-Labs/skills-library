---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-explore-split-view-and-query-history
name: grafana-explore-split-view-and-query-history
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [explore-split-view, explore-workflow, grafana-explore, signal-correlation, query-history]
level: practitioner
status: docs-checked
description: "Use Grafana Explore query history (retention, starring, search, filters) and the Query inspector tabs (Stats, Query, JSON, Data, Error) to investigate slow or wrong queries."
sources: ["https://grafana.com/docs/grafana/latest/explore/", "https://grafana.com/docs/grafana/latest/explore/query-management/", "https://grafana.com/docs/grafana/latest/explore/explore-inspector/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana Explore: query history and the Query inspector

Explore is the starting point for querying, analysing and aggregating data in Grafana without first building a dashboard.
Its documentation also has sections on logs, traces and the correlations editor (not covered here).

## Query history
- Open Explore and click **Query history**; the pane opens at the bottom with tabs **Query history**, **Starred** and **Settings**.
- History is stored in the Grafana database and is not shared with other users. Retention is two weeks; older queries are
  deleted automatically, except **starred** queries.
- Per query: run or re-run, create or edit a comment, copy the query, copy a shortened link, delete, star, or add it to your
  saved queries. Newest first by default; switch to Oldest first with the sort box; search by keyword (comments are searched too).
- Filter by one or more data sources (queries on the Mixed data source appear only when filtering for "Mixed"), or by date
  with the vertical slider. In the Starred tab you can switch the data source and run a starred query.
- Settings tab: toggle which tab is the default active one. Settings are global and apply to both panels in split mode.

## Query inspector
Run a query in Explore and click **Query inspector**; the pane opens at the bottom with these tabs:
- **Stats**: how long the query takes, how many queries were sent, rows returned and trace IDs (read-only).
- **Query**: raw request and response and when Grafana queried the data source (click Refresh to resend).
- **JSON**: Panel data, or DataFrame JSON (from query) without transformations or field configuration.
- **Data**: raw results; Series joined by time for multiple queries, Formatted data, Download for Excel, Download CSV.
- **Error**: only visible if the query returns an error.
Use Stats and Query together to see whether time goes to the backend or elsewhere.

## Verify
- [ ] The queries you rely on are starred, or they disappear after two weeks.
- [ ] A slow query's Stats tab was checked before blaming the data source.

## Checked
Checked 2026-11-07. Read in full: the Explore landing page, the Query management in Explore page and the Query inspector in
Explore page. Removed as not stated on these pages: the access requirements (`viewers_can_edit`, `datasources:explore`),
the `x` shortcut, the split/sync-time/trace-link/add-to-dashboard workflow steps, the `[query_history]` and `[explore]` and
`[short_links]` configuration keys and the 14-day wording (the page says two weeks), the Grafana 12 query library flag, the share URL formats, and the
Logs-in-Explore features. Those belong to the Get started, Logs in Explore and Traces in Explore pages, which I did not read.
Method: documentation only; no commands were run.
