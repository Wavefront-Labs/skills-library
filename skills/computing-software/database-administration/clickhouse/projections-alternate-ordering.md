---
id: computing-software.database-administration.clickhouse.projections-alternate-ordering
name: projections-alternate-ordering
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, projections, add-projection, materialize-projection, optimize-use-projections]
level: practitioner
status: docs-checked
description: "Add a ClickHouse projection for an alternate sort order or pre-aggregation, materialize it for old parts and confirm it in system.query_log."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/data-modeling/projections/1_projections.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# projections alternate ordering
A projection stores an extra, differently ordered or pre-aggregated copy of a table's data inside the same table parts; the optimizer picks it automatically when it is cheaper. Use it to give a table a second sort order (the main ORDER BY can't change after creation) or a cheap rollup.

```sql
ALTER TABLE nyc_taxi.trips_with_projection
ADD PROJECTION prj_tip_amount
(
    SELECT *
    ORDER BY tip_amount, dateDiff('minutes', pickup_datetime, dropoff_datetime)
);
ALTER TABLE nyc_taxi.trips_with_projection MATERIALIZE PROJECTION prj_tip_amount;
```
`ADD PROJECTION` covers new inserts; `MATERIALIZE PROJECTION` builds it for existing parts (a mutation, so heavy). Aggregate projections use `SELECT town, avg(price) ... GROUP BY town`.

Confirm usage:
```sql
SELECT query, projections FROM system.query_log WHERE query_id = '<query_id>';
```
and compare with `SETTINGS optimize_use_projections = 0` (the setting is on by default).

Trade-offs: projections are applied only to queries on that table, unlike materialized views, which write to a separate target table (see the comparison skill). Per the ClickHouse comparison page, projections do not work with FINAL queries and are only available for MergeTree-family engines.

Gotcha: `MATERIALIZE PROJECTION` is what builds the projection for data already in the table.

## Checked
2026-11-03. Confirmed against the ClickHouse docs pages "Projections" and "Materialized views versus projections": ADD and MATERIALIZE PROJECTION, `optimize_use_projections` enabled by default, automatic selection by the optimizer, the FINAL and engine limits. Removed: storage and insert-cost figures, the `SELECT *` size claim and the EXPLAIN output claim, none stated on those pages.
Method: documentation only; no commands were run.
