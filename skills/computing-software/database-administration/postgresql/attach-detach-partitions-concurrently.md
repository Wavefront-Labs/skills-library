---
id: computing-software.database-administration.postgresql.attach-detach-partitions-concurrently
name: attach-detach-partitions-concurrently
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, declarative-partitioning, table-partitioning, attach-partition, detach-partition-concurrently, partition-retention, check-constraint, lock-levels]
level: advanced
status: verified
description: "Add and retire PostgreSQL partitions on a live table: ATTACH with a pre-validated CHECK to skip the scan, and DETACH CONCURRENTLY for retention without blocking."
sources:
  - https://www.postgresql.org/docs/current/ddl-partitioning.html#DDL-PARTITIONING-DECLARATIVE-MAINTENANCE
  - https://www.postgresql.org/docs/current/sql-altertable.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ATTACH and DETACH partitions without downtime

**Goal:** load a partition offline and swap it in, and remove old data, without
blocking application queries.

## Attach with minimal locking
`CREATE TABLE ... PARTITION OF` takes `ACCESS EXCLUSIVE` on the parent (blocks
everything briefly, and waits behind any long query). `ATTACH PARTITION` takes
only `SHARE UPDATE EXCLUSIVE` on the parent (PG12+), so prefer:
```sql
CREATE TABLE measurements_2026_11 (LIKE measurements INCLUDING DEFAULTS INCLUDING CONSTRAINTS);
-- optional: bulk load it here
ALTER TABLE measurements_2026_11 ADD CONSTRAINT m_2026_11_chk
  CHECK (ts >= '2026-11-01' AND ts < '2026-12-01');        -- validated now, on the small table
ALTER TABLE measurements ATTACH PARTITION measurements_2026_11
  FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');         -- skips the validation scan
ALTER TABLE measurements_2026_11 DROP CONSTRAINT m_2026_11_chk;
```
Create the matching indexes on the new table first: attach then just links them
to the parent's partitioned indexes instead of building under lock.
If a default partition exists, it is scanned to prove no rows belong to the new
range: keep the default empty or add an equivalent CHECK to it.

## Detach for retention
```sql
ALTER TABLE measurements DETACH PARTITION measurements_2025_10 CONCURRENTLY;  -- PG14+
DROP TABLE measurements_2025_10;          -- or archive it first (pg_dump -t / COPY to object storage)
```
`CONCURRENTLY` runs in two transactions, cannot be inside a transaction block,
and is not allowed when a default partition exists. If interrupted, finish with
`ALTER TABLE measurements DETACH PARTITION measurements_2025_10 FINALIZE;`.

## Gotchas
- Always set `lock_timeout` (e.g. `'3s'`) on DDL sessions and retry: a waiting
  ACCESS EXCLUSIVE request blocks every later query behind it.
- Dropping a partition directly (`DROP TABLE part`) needs ACCESS EXCLUSIVE on the parent.
- Foreign keys referencing the partitioned table make detach validate references.

## Verify
`\d+ measurements` lists the partitions; `pg_locks` during the operation shows no
long `AccessExclusiveLock` waits on the parent.

## Checked
- PostgreSQL 17.6: `CREATE TABLE ... PARTITION OF` held `AccessExclusiveLock` on the parent and `ATTACH PARTITION` only `ShareUpdateExclusiveLock`; with a matching CHECK the attach log said the partition constraint is implied (no scan); `DETACH ... CONCURRENTLY` errors inside a transaction block and with a default partition present, works otherwise; `FINALIZE` errors when no detach is pending.
