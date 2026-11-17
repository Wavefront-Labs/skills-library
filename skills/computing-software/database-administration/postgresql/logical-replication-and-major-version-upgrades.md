---
id: computing-software.database-administration.postgresql.logical-replication-and-major-version-upgrades
name: logical-replication-and-major-version-upgrades
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, logical-replication, publication, subscription, pg_dump, major-version-upgrade, pg_upgrade, zero-downtime-migration, replication-slots, ddl, sequences]
level: advanced
status: docs-checked
description: "Build a logical-replication subscriber for near-zero-downtime major version upgrades or cross-platform moves, and avoid the gaps it doesn't cover."
sources:
  - https://www.postgresql.org/docs/current/logical-replication.html
  - https://www.postgresql.org/docs/current/logical-replication-restrictions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostgreSQL logical replication for near-zero-downtime upgrades

**Goal:** move a database to a new major version (or new host/cloud) with minutes,
not hours, of write downtime, using built-in logical replication instead of
`pg_upgrade` in place.

## 1. Why not just pg_upgrade
`pg_upgrade` works in place on one server (see its reference page for its downtime
and rollback behaviour). Logical
replication lets the new version run side by side, catch up while the old one keeps
serving traffic, and gives a rollback path (just don't cut over) at the cost of more
setup and some feature gaps.

## 2. Setting it up
On the source (must be `wal_level = logical`):
```sql
CREATE PUBLICATION pub_all FOR ALL TABLES;
-- or scope it: CREATE PUBLICATION pub_app FOR TABLE orders, customers;
```
On the target, create the schema first (`pg_dump --schema-only`, apply it), then:
```sql
CREATE SUBSCRIPTION sub_app CONNECTION 'host=source dbname=app' PUBLICATION pub_app;
```
This does an initial COPY of existing data, then streams changes. Watch
`pg_stat_subscription` and `pg_stat_replication` (on the source) for lag.

## 3. What logical replication does NOT carry
This is the part that bites people assuming it behaves like physical replication:
- **No DDL replication.** Every schema change (new column, new table) must be
  applied by hand on both sides, in the right order, or the subscription breaks
  with a column-mismatch error and stops applying.
- **Sequences are not replicated.** After cutover, every sequence on the target is
  behind; `SELECT setval()` each one from the source's current value before
  allowing writes, or the app gets duplicate-key errors immediately.
- **Large objects are not replicated.** The restrictions page lists no workaround other
  than storing the data in normal tables.
- Row filters (a `WHERE` on a published table) have their own rules (see the Row Filters
  section of the logical replication chapter); test with representative DDL before
  relying on this for cutover.

## 4. Cutover sequence
1. Let the subscription catch up until `pg_stat_subscription.latest_end_lsn`
   converges with the source's current WAL position and `pg_stat_replication`
   on the source shows the walsender caught up (`replay_lag` near zero).
2. Stop writes on the source (brief app-level pause or read-only mode).
3. Confirm the last transactions replicated (compare row counts / checksums on a
   few hot tables).
4. Fix sequences on the target (step 3 above).
5. Repoint the application connection string. This is the only "downtime" — seconds
   to low minutes, not the hours a full dump/restore would take.
6. Drop the subscription on the target and the publication on the source once
   confident; keep the old primary readable as a fallback for a day.

## 5. Common failures
- Subscription silently stops applying after a DDL mismatch — check the log and whether
  `pg_stat_subscription_stats.apply_error_count` is increasing; fix the schema, then
  `ALTER SUBSCRIPTION ... REFRESH PUBLICATION` if tables were added.
- Replication slot on the source grows unbounded WAL if the subscriber falls behind
  or is dropped without `DROP SUBSCRIPTION` cleaning it up — monitor
  `pg_replication_slots` disk usage, same risk as an abandoned physical slot.

## Verify
- [ ] `wal_level = logical` on the source, confirmed with `SHOW wal_level`.
- [ ] `pg_stat_subscription` shows the subscription as active with lag trending to zero.
- [ ] A test DDL change was applied manually on both sides and did not break the subscription.
- [ ] Sequences on the target were resynced before the first post-cutover write.
- [ ] The publication/subscription pair was dropped after cutover so no orphaned slot remains.

## Checked

2026-10-28. Confirmed against the PostgreSQL current docs (version 18): logical replication restrictions page (DDL and schema not replicated, pg_dump --schema-only for the initial schema, sequence data not replicated, large objects not replicated), monitoring statistics (pg_stat_subscription.latest_end_lsn, pg_stat_replication.replay_lag, pg_stat_subscription_stats.apply_error_count), ALTER SUBSCRIPTION ... REFRESH PUBLICATION, Row Filters section. Fixed: pg_stat_subscription_stats has no last_error column (apply_error_count is the documented counter). Removed unconfirmed: pg_upgrade --link timing and binary requirements, the restart-required note, per-table COPY consistency claim, TRUNCATE/PG11 and materialized-view notes, generated/identity column note, the seeding-from-LSN tip.

Method: documentation only; no commands were run.
