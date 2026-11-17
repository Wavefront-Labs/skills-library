---
id: computing-software.data-engineering.trino.trino-materialized-view-grace-period
name: trino-materialized-view-grace-period
category: computing-software
field: data-engineering
product: trino
tags: [materialized-view, grace-period, when-stale, refresh-materialized-view, create-materialized-view]
level: advanced
status: docs-checked
description: "Create Trino materialized views with GRACE PERIOD and WHEN STALE INLINE or FAIL, and know that refresh is needed to populate and reset staleness."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/sql/create-materialized-view.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino materialized view grace period

Syntax: `CREATE [ OR REPLACE ] MATERIALIZED VIEW [ IF NOT EXISTS ] view_name [ GRACE PERIOD interval ] [ WHEN STALE ( INLINE | FAIL ) ] [ COMMENT string ] [ WITH properties ] AS query`. `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.

After creation you must run `REFRESH MATERIALIZED VIEW` to populate it. The view is a physical copy of the query results at refresh time, so reads avoid repeating aggregation and joins.

Grace period: how long the stored data is used. Within it, reads are fast but may lag the base tables. After it, the data is computed on the fly from the query, so it is slower but current. Unspecified, the grace period is infinite, so all queries fall within it. Every refresh resets the start of the grace period.

`WHEN STALE`, applied outside the grace period:
- `INLINE` (default): expand like a logical view and read fresh data.
- `FAIL`: queries fail with an error.
This clause needs connector support; a connector without it errors on any value other than `INLINE`.

```sql
CREATE MATERIALIZED VIEW orders_summary
GRACE PERIOD INTERVAL '1' HOUR
WHEN STALE FAIL
AS
    SELECT orderdate, sum(totalprice) AS price
    FROM orders
    GROUP BY orderdate;
```

`WITH` properties are connector specific (for Iceberg, for example `partitioning = ARRAY['mktsegment', 'nationkey']`). Inspect definitions with `SELECT * FROM system.metadata.materialized_views` and available properties in `system.metadata.materialized_view_properties`.

## Checked

Method: 2026-11-08 docs-only read of the cited source page(s) in full. All claims match the page; unchanged.
