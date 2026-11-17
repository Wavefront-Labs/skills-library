---
id: computing-software.database-administration.vitess.instant-ddl-and-partition-rotation
name: instant-ddl-and-partition-rotation
category: computing-software
field: database-administration
product: vitess
tags: [online-ddl, instant-ddl, prefer-instant-ddl, partitioning, range-partition, algorithm-instant]
level: advanced
status: docs-checked
description: "Use MySQL INSTANT DDL from Vitess: --prefer-instant-ddl, eligibility prediction, the special_plan marker, and ADD/DROP PARTITION on RANGE tables."
sources:
  - https://vitess.io/docs/25.0/user-guides/schema-changes/instant-ddl-migrations/
  - https://vitess.io/docs/25.0/user-guides/schema-changes/ddl-strategy-flags/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`ALTER TABLE ... ALGORITHM=INSTANT` is available in both unmanaged and managed migrations. Unmanaged: send it via `ApplySchema` with `direct` or `mysql` strategies, or through a VTGate connection. Naively attempting INSTANT and falling back is common, but Vitess can do better.

With the `vitess` strategy Vitess normally prefers an Online DDL (which is revertible). The `--prefer-instant-ddl` flag tells it to use INSTANT where possible. Vitess predicts eligibility from the existing schema and the requested change using its knowledge of MySQL limitations; if eligible and the flag is set, it adds `ALGORITHM=INSTANT`, otherwise any `ALGORITHM` directive is ignored. An INSTANT migration has no shadow table, no artifacts and is not revertible.

```sql
set @@ddl_strategy='vitess --prefer-instant-ddl';
alter table corder add column name varchar(32);
```

`show vitess_migrations like '<uuid>'` lists it as usual, with `options: --prefer-instant-ddl` and `special_plan: {"operation":"instant-ddl"}`.

Partitioning (RANGE partitioned tables and partition rotation):
- `ADD PARTITION` creates a new empty hidden table, as fast as CREATE TABLE, so Vitess always runs it directly on MySQL. Not revertible; no flag controls this.
- `DROP PARTITION` is meant to discard rows, which an Online DDL copy would defeat, so Vitess always runs it directly. Not revertible.
- No special behaviour exists for other partitioning schemes or operations.

The `--fast-range-rotation` flag instructs Vitess to run such a migration directly against MySQL when it is on a RANGE partitioned table and contains only a single ADD or DROP PARTITION; the migration is then not revertible.

## Checked

2026-11-08. Read in full: INSTANT DDL migrations page and ddl_strategy flags page (vitess.io docs 25.0, via the website repo markdown). Confirmed: unmanaged and managed use, `--prefer-instant-ddl`, eligibility prediction, no shadow table or revert, the special_plan marker and the partition notes (INSTANT DDL page); `--fast-range-rotation` conditions (flags page). Fixed: the flag sentence now states its conditions and that the result is not revertible.

Method: documentation only; no commands were run.
