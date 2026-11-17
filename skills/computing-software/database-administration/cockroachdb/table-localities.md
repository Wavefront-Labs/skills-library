---
id: computing-software.database-administration.cockroachdb.table-localities
name: table-localities
category: computing-software
field: database-administration
product: cockroachdb
tags: [table-localities, regional-by-row, regional-tables, global-tables, crdb-region]
level: practitioner
status: docs-checked
description: "Pick a CockroachDB table locality: REGIONAL BY TABLE, REGIONAL BY ROW or GLOBAL, with index behaviour, hash-sharded index caveat and when each fits."
sources:
  - https://www.cockroachlabs.com/docs/stable/table-localities
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: match each table's data placement to its access pattern in a multi-region database.

Localities:
- Regional (by table): low-latency reads and writes for the whole table from one home region (default: the database's primary region); slower from other regions.
- Regional by row: each row has a home region, so different rows are fast from different regions. Region is held in the `crdb_region` column, or in a column you specify with `REGIONAL BY ROW AS {column}`.
- Global: optimized for low-latency reads from all regions. Writes are slower from any region because they use a non-blocking transaction protocol with a timestamp in the future; observed write latency depends on the `--max-offset` setting.

When to choose:
- Regional: your application needs low-latency reads and writes from a single region (per table or per row) and can accept higher latency elsewhere.
- Global: read-mostly reference data that is rarely updated but needed in every region, and you accept slower writes.

Indexes on `REGIONAL BY ROW` tables: the region column behaves as a prefix of indexes (this also applies to GIN indexes), which affects how unique constraints are enforced; the docs link a worked example for adding a unique index. Hash-sharded indexes work on these tables as long as `crdb_region` is not one of the hash-sharded index columns.

To change the region expression of an existing regional by row table, use the documented "modify the region column or its expression" procedure.

## Checked

2026-11-03. Confirmed against the table localities page: three localities, primary region default, `crdb_region` and `REGIONAL BY ROW AS`, non-blocking protocol and `--max-offset`, GLOBAL use case, index prefix and hash-sharded caveat, region expression change procedure. Removed: invented verification step.
Method: documentation only; no commands were run.
