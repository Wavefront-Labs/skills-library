---
id: computing-software.data-engineering.metabase.metrics
name: metrics
category: computing-software
field: data-engineering
product: metabase
tags: [metrics, semantic-layer, dimensions, metric-formula, metrics-explorer]
level: practitioner
status: docs-checked
description: "Define reusable Metabase metrics in the semantic layer: creation paths, required formula, dimension curation, and limits such as query-builder-only use and join advice."
sources:
  - https://www.metabase.com/docs/latest/data-modeling/semantic-layer/metrics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Creation: press Cmd/Ctrl+K and search "New metric", or use Browse, Metrics, **+**. In Data Studio use Semantic layer, **+ New**, Metric. Start from a table, saved question, model or another metric. The formula is required; joins and filters are allowed before it. Save to a collection, then curate its dimensions.

Usage: metrics appear under **Summarize, Metrics** in the query builder. You can break them out by dimensions, combine them and use them in custom expressions. The Metrics explorer compares metrics and does math with them. Marking a metric verified is for Pro and Enterprise plans; caching individual metrics is also plan-gated (the page shows a plans notice).

Limitations:
- A metric works only on the data source it was defined on, not on models or questions built from it.
- Metrics exist only in the query builder; use snippets for reusable SQL.
- A formula must aggregate a column, so row-level calculations are not allowed.
- Joins and filters in definitions are not recommended (filter conflicts in the query builder); for multiple tables, make a transform and build the metric on its table. Use CountIf, SumIf or DistinctIf for conditional aggregations.
- You cannot restrict metric creation to users who lack data permissions.

Gotchas:
- Editing a definition immediately changes every question that uses it.
- Dashboard filters can't use a dimension you remove.
- Without a default dimension, a metric displays as a single number.
- Curating dimensions does not change the query builder's filter and summarize pickers; it affects the Metrics explorer, the About tab and dashboard filters.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Reworded the plan-gating, join and dimension-removal claims to match the page. Otherwise unchanged.
