---
id: computing-software.data-engineering.metabase.dashboard-linked-filters
name: dashboard-linked-filters
category: computing-software
field: data-engineering
product: metabase
tags: [linked-filters, parent-filter, foreign-key, dashboard-filters, field-filter]
level: advanced
status: docs-checked
description: "Restrict one Metabase dashboard filter by another with linked filters: required child types, column and foreign key requirements, and silent-failure limitations."
sources:
  - https://www.metabase.com/docs/latest/dashboards/linked-filters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Setup: click the pencil icon to edit the dashboard, then the gear icon on the child filter. In the **Linked filters** tab select one or more parent filters.

Types: the child must be an ID, Location or Text or Category filter. Parents can be any filter type.

Requirements:
- Filters must map to database columns, not custom columns or summaries.
- The columns must share a table, or be connected by a foreign key in the table metadata, directly or through intermediate tables.

Limitations and gotchas:
- Unconnected columns produce no error. "Metabase won't show an error", and the child filter is simply not restricted.
- Only table metadata counts. Joins defined in models or questions are ignored, so the child may still list values the underlying question excludes.
- Native SQL needs a field filter variable; basic SQL variables cannot be linked.
- Filters whose value source is "Custom List" or "From another model or question" cannot be linked.

If a child list does not narrow, the page says to check that the table relationships are set up (same table, or foreign keys in the table metadata) and points to a separate linked-filters troubleshooting guide. The page's example: a model that excludes San Francisco does not stop the city filter listing it, because the filter only knows table metadata and its sample values.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Replaced an invented debug procedure with what the page says. Otherwise unchanged.
