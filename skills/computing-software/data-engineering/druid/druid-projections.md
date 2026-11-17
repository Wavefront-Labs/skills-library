---
id: computing-software.data-engineering.druid.druid-projections
name: druid-projections
category: computing-software
field: data-engineering
product: druid
tags: [projections, pre-aggregation, aggregate-projection, experimental, grouping-columns]
level: advanced
status: docs-checked
description: "Define aggregate projections in Druid segments for common query shapes (experimental), use or bypass them, and compact with them."
sources:
  - https://github.com/apache/druid/blob/master/docs/querying/projections.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Projections are experimental and not recommended for production. A projection is a pre-aggregation computed and stored in the segment. Unlike rollup, which discards source rows, projections leave source dimensions in place and queryable. Queries whose shape matches a projection process fewer rows, so build projections for commonly used queries.

## Definition

A projection (type `aggregate`, with a `name`) has:
- `virtualColumns`: computed columns, for example an expression column `__gran` = `timestamp_floor(__time, 'PT1H')` with `outputType` `LONG`.
- `groupingColumns`: the columns that sort the projection; each must exist in the datasource or the virtual columns. Definition order sets the sort order, always ascending.
- `aggregators`: the aggregations, such as `HLLSketchBuild` on `user`, and `longSum` on `added` and `deleted`.

A query that groups by the same shape (`TIME_FLOOR(__time,'PT1H')`, `channel`, `page`) with matching aggregators (`APPROX_COUNT_DISTINCT_DS`, `SUM`) uses the projection. The names in the docs example (`channel`, `page`, `added`) are illustrative.

## Where to create

- Ingestion spec (`projectionsSpec` block) or SQL ingestion; SQL-based ingestion also needs the `druid-catalog` extension loaded.
- The catalog for an existing datasource (recommended): table `properties.projections`, each entry with a `spec`; grouping columns can carry `multiValueHandling` and `createBitmapIndex`.
- A compaction spec for an existing datasource.

## Limitations

- Float source columns need double aggregators (for example `doubleSum`).
- The projection aggregator must match the query's aggregator for the projection to be used. Output types can differ between ingestion and query time (for example `cardinality`: string at ingestion, long at query time).
- Source columns are unaffected, so storage grows.
- Projection dimensions become part of the datasource; removing a projection requires reingesting the data.

## Using projections

Druid uses a matching projection automatically. Query context overrides: `useProjection` (name; the query fails if it does not match), `forceProjections` (default false; if true the query fails when nothing matches), `noProjections` (true disables all projections for the query).

## Compaction

For a datasource with projections, compaction must use `spec.type: catalog`. For Coordinator duties send a config with `type` `catalog`, `dataSource`, `engine` (the page shows `native`) and the usual skip/priority fields. For compaction supervisors wrap it as `type` `autocompact` with that object under `spec`.

## Checked

2026-11-08. Read the cited projections page in full. Rewrote the draft with creation locations, limitations, query context parameters and compaction requirements; removed an unsourced version-control suggestion. The page's ingestion-spec example is empty, so none is given.

Method: documentation only; no commands were run.
