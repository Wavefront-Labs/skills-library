---
id: computing-software.database-administration.postgresql.converting-a-table-to-partitioned
name: converting-a-table-to-partitioned
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, declarative-partitioning, table-partitioning, convert-to-partitioned, attach-partition, zero-downtime, schema-migration]
level: advanced
status: verified
description: "Turn a large existing PostgreSQL table into a partitioned one with minimal downtime: attach the old table as a partition with a pre-validated CHECK, then move data in batches."
sources:
  - https://www.postgresql.org/docs/current/ddl-partitioning.html
  - https://www.postgresql.org/docs/current/sql-altertable.html#SQL-ALTERTABLE-ATTACH-PARTITION
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Converting an existing table to partitioned

There is no `ALTER TABLE ... PARTITION BY`. You build a new partitioned parent and move the
existing table under it.

## Approach A: attach the old table as one big partition (fast, low risk)
```sql
-- 1. Constraint matching the future partition bound, added without a long lock
ALTER TABLE events ADD CONSTRAINT events_old_bound
  CHECK (created_at >= '2000-01-01' AND created_at < '2026-11-01') NOT VALID;
ALTER TABLE events VALIDATE CONSTRAINT events_old_bound;     -- SHARE UPDATE EXCLUSIVE, online

-- 1b. The old primary key (id) cannot be a partition's key, so build the composite one online first
CREATE UNIQUE INDEX CONCURRENTLY events_id_created_uq ON events (id, created_at);

-- 2. Short transaction: rename, swap the primary key, create parent
BEGIN;
SET lock_timeout = '3s';
ALTER TABLE events RENAME TO events_legacy;
ALTER TABLE child DROP CONSTRAINT child_eid_fkey;              -- every FK that referenced events(id)
ALTER TABLE events_legacy DROP CONSTRAINT events_pkey;
ALTER TABLE events_legacy ADD PRIMARY KEY USING INDEX events_id_created_uq;
CREATE TABLE events (LIKE events_legacy INCLUDING DEFAULTS)    -- not INCLUDING CONSTRAINTS (see gotchas)
  PARTITION BY RANGE (created_at);
ALTER TABLE events ADD PRIMARY KEY (id, created_at);
ALTER TABLE events ATTACH PARTITION events_legacy
  FOR VALUES FROM ('2000-01-01') TO ('2026-11-01');   -- skips the scan thanks to the valid CHECK
CREATE TABLE events_2026_11 PARTITION OF events FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');
ALTER SEQUENCE events_id_seq OWNED BY events.id;
COMMIT;
```
New rows go to new monthly partitions; the legacy partition ages out or is split later
(detach, then move ranges into proper partitions in batches).

## Approach B: new table + backfill + swap (when you need real partitions now)
1. Create partitioned `events_new` with all partitions and indexes.
2. Dual-write: trigger on `events` copying INSERT/UPDATE/DELETE to `events_new`, or use
   logical replication into it.
3. Backfill in batches by key range (`INSERT ... SELECT ... WHERE id BETWEEN ...`), with
   `ON CONFLICT DO NOTHING`.
4. Verify counts per range, then in one short transaction rename tables and drop the trigger.

## Things that change
- Primary keys/unique constraints must include the partition key: `PRIMARY KEY (id)` becomes
  `PRIMARY KEY (id, created_at)`. Foreign keys **referencing** the table must reference the
  full key (PG12+ allows FKs to partitioned tables).
- Sequences: `LIKE ... INCLUDING DEFAULTS` reuses the same sequence via the default (it keeps its
  old name, here `events_id_seq`, and stays owned by the legacy table's column until you run
  `ALTER SEQUENCE ... OWNED BY events.id`).
- Foreign keys that referenced the old table follow the rename and now point at `events_legacy`;
  drop and recreate them against the new parent (referencing a partitioned table needs PG12+,
  and the referenced columns must be a unique key, so include the partition key).
- Indexes: create them on the parent (`CREATE INDEX ON ONLY events ...` plus per-partition
  `CONCURRENTLY` and `ATTACH PARTITION` of indexes avoids long locks).
- Grants, triggers, RLS policies, publications must be recreated on the parent.

## Gotchas
- `INCLUDING CONSTRAINTS` copies the temporary bound CHECK onto the new parent, and every new partition inherits it: the first insert into `events_2026_11` failed with `violates check constraint "events_old_bound"`. Leave it out (NOT NULL is copied anyway) and recreate any real CHECKs on the parent.
- Adding `PRIMARY KEY (id, created_at)` to the parent while the legacy table still has `PRIMARY KEY (id)` fails with `multiple primary keys for table "events_legacy" are not allowed`: swap the key first as above.
- Queries without the partition key in WHERE now scan all partitions.
- `ATTACH PARTITION` takes SHARE UPDATE EXCLUSIVE on the parent (PG12+) but ACCESS EXCLUSIVE
  on the table being attached; the rename step needs a brief exclusive lock.
- Test ORMs: some cache table OIDs or rely on `RETURNING` behaviours.

## Verify
`SELECT tableoid::regclass, count(*) FROM events GROUP BY 1;` shows rows per partition;
EXPLAIN of key queries shows partition pruning.

## Checked
PostgreSQL 17.6, 2,000-row table with an FK child: the corrected Approach A script runs end to end; `ATTACH PARTITION` logs `partition constraint for table "events_legacy" is implied by existing constraints` (no scan); new rows route to `events_2026_11`; `\d` shows the sequence default shared and `ALTER SEQUENCE ... OWNED BY events.id` accepted; attaching a table to an existing parent held ShareUpdateExclusiveLock on the parent and AccessExclusiveLock plus ShareLock on the attached table. The original script (with `INCLUDING CONSTRAINTS` and the old primary key) failed in the two ways described under Gotchas. Approach B was not run end to end (it is a procedure).
