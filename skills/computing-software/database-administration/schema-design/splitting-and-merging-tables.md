---
id: computing-software.database-administration.schema-design.splitting-and-merging-tables
name: splitting-and-merging-tables
category: computing-software
field: database-administration
product: schema-design
tags: [database-administration, schema-design, split-table, merge-tables, vertical-partitioning, database-refactoring, schema-migrations]
level: practitioner
status: draft
description: "Split a table vertically or by entity, or merge two tables, on a live system using the refactoring-databases steps: new structure, backfill, sync, switch readers, contract."
sources:
  - https://databaserefactoring.com/SplitTable.html
  - https://databaserefactoring.com/MergeTables.html
  - https://martinfowler.com/bliki/ParallelChange.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Splitting and merging tables

## Why split
- Vertical split: wide table where a few big or rarely used columns (blobs, JSON, profile text) bloat every row read; or columns with different access/security needs (PII in a separate table with tighter grants).
- Entity split: one table secretly holds two concepts (`customers` holding both people and companies with half-null columns).

## Split procedure (live)
1. Create the new table with its own PK (often the same key, 1:1):
```sql
CREATE TABLE customer_profiles (customer_id bigint PRIMARY KEY REFERENCES customers ON DELETE CASCADE,
  bio text, preferences jsonb);
```
2. Backfill in batches: `INSERT INTO customer_profiles SELECT id, bio, preferences FROM customers WHERE id BETWEEN $1 AND $2 ON CONFLICT DO NOTHING;`
3. Keep in sync during transition: triggers on the old table, or dual writes in the application (with a reconciliation job).
4. Switch readers to the new table (feature flag); then switch writers.
5. Contract: drop old columns after the transition period (`ALTER TABLE customers DROP COLUMN bio, DROP COLUMN preferences`), which in PostgreSQL is metadata-only (space reclaimed by later rewrites/VACUUM FULL/pg_repack).

## Merge procedure
Two tables representing the same concept (`customers_legacy` and `customers`):
1. Define the merged schema and mapping rules (conflicting values, duplicate detection, key mapping table `old_id → new_id`).
2. Create/extend the target, backfill with the mapping, keep a sync from both sources.
3. Repoint foreign keys: add new FK columns, backfill via mapping, swap.
4. Replace the old table with a view over the merged one for the transition period, then drop.

## Tips
- Keep the 1:1 key identical in vertical splits so joins are trivial and the old shape can be exposed by a view joining both.
- Verify sync with periodic checksums: `SELECT count(*), sum(hashtext(bio)) ...` on both sides.
- Large tables: batch sizes tuned to replication lag; pause on lag alarms.

## Verify
Reconciliation query returns zero differences between old and new representations before switching readers and again before contract.
