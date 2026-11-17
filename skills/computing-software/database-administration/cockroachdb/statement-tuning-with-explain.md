---
id: computing-software.database-administration.cockroachdb.statement-tuning-with-explain
name: statement-tuning-with-explain
category: computing-software
field: database-administration
product: cockroachdb
tags: [explain, statement-tuning, full-table-scan, secondary-index, storing-columns]
level: practitioner
status: docs-checked
description: "Tune CockroachDB statements with EXPLAIN: spot FULL SCAN spans, add a secondary index, and store extra columns to avoid index joins."
sources:
  - https://www.cockroachlabs.com/docs/stable/sql-tuning-with-explain
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use plan output to turn slow lookups into index scans.

Workflow:
1. Run the plan: `EXPLAIN SELECT * FROM users WHERE name = 'Cheyenne Smith';`
2. Read the scan node. `table: users@users_pkey` with `spans: FULL SCAN` means no usable index on the filter column, so every row is read. `distribution: full` also hints at a distributed scan.
3. Add a secondary index: `CREATE INDEX ON users (name);` and re-run `EXPLAIN`. Expected improvement: `table: users@users_name_idx`, `spans: [/'Cheyenne Smith' - /'Cheyenne Smith']`, `distribution: local`.
4. If the query selects more columns than the index covers, the plan adds an index join back to the primary index (a second lookup per row). Drop and recreate the index storing the extra column so it covers the query:
```sql
CREATE INDEX ON users (name) STORING (credit_card);
```
After this, `EXPLAIN SELECT name, credit_card FROM users WHERE name = 'Cheyenne Smith';` shows only the single index scan.

The page works on the MovR demo (`cockroach demo movr --num-users 1250000`) so you can reproduce plans safely before touching production.

## Checked

2026-11-03. Confirmed against the SQL tuning with EXPLAIN page: the MovR demo command, `FULL SCAN` plan, `users_name_idx` plan with `distribution: local`, index join and `STORING` fix. Removed: unsourced index-cost advice, the `EXPLAIN ANALYZE` aside and the Statements page latency check.
Method: documentation only; no commands were run.
