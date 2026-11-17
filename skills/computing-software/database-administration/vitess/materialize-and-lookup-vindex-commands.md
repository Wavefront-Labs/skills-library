---
id: computing-software.database-administration.vitess.materialize-and-lookup-vindex-commands
name: materialize-and-lookup-vindex-commands
category: computing-software
field: database-administration
product: vitess
tags: [materialize, lookupvindex, vreplication, rollups, table-settings, materialized-views]
level: practitioner
status: docs-checked
description: "Create materialized copies and rollups with Materialize (table-settings JSON, query limits) and know that LookupVindex create uses VReplication to backfill a lookup vindex."
sources:
  - https://vitess.io/docs/25.0/reference/vreplication/materialize/
  - https://vitess.io/docs/25.0/reference/vreplication/lookupvindex/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Materialize` is the low-level VReplication command for generalised materialization; targets can be copies, aggregations or views, kept in near-real-time sync. Prefer `MoveTables` to copy tables to another keyspace and `Reshard` to change sharding.

Query limits for `source_expression`: a SELECT on a single table (no JOIN), only `=`, `<`, `<=`, `>`, `>=`, `<>`, `!=`, `IN`, `BETWEEN` (no OR or LIKE), no DISTINCT, no derived table, aliases on expressions (`select hour(c1) as c1_hour from t1`), and GROUP BY must not reference an aggregate. Avoid MySQL 8.0+ `INSTANT ADD COLUMN` on source tables; it can break the workflow.

Lifecycle: `create`, then `show` or `status` (`Materialize --target-keyspace <ks> show --workflow <wf>`), then use the target once it is Replicating.

Example from the page:

```
vtctldclient --server localhost:15999 Materialize --workflow product_sales --target-keyspace commerce create --source-keyspace commerce --table-settings '[{"target_table": "sales_by_sku", "create_ddl": "create table sales_by_sku (sku varchar(128) not null primary key, orders bigint, revenue bigint)", "source_expression": "select sku, count(*) as orders, sum(price) as revenue from corder group by sku"}]' --cells zone1 --cells zone2 --tablet-types replica
```

`--table-settings` is a required JSON array of `target_table`, `source_expression` and optional `create_ddl` (a DDL string, or `copy` to reuse the source schema). `--cells` defaults to the local cell; `--tablet-types` defaults to `in_order:REPLICA,PRIMARY`.

`LookupVindex create` creates and backfills a lookup vindex for an existing, possibly large, table using VReplication until it is in sync; after that normal transactional updates of the owner table maintain it.

## Checked

2026-11-04. Query limits, example, option defaults and notes on the Materialize page; LookupVindex description on the LookupVindex page.

Method: documentation only; no commands were run.
