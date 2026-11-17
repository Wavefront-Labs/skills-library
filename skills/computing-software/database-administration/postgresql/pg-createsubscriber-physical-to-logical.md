---
id: computing-software.database-administration.postgresql.pg-createsubscriber-physical-to-logical
name: pg-createsubscriber-physical-to-logical
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-createsubscriber, logical-replication, physical-standby, major-version-upgrade, pg17]
level: practitioner
status: docs-checked
description: "Convert a PostgreSQL physical standby into a logical subscriber with pg_createsubscriber (PG17) to skip the initial table copy for big databases."
sources:
  - https://www.postgresql.org/docs/current/app-pgcreatesubscriber.html
  - https://www.postgresql.org/docs/current/logical-replication.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Converting a physical standby with pg_createsubscriber

Initial data copy (`copy_data = true`) for a multi-TB database can take days and bloat the publisher. `pg_createsubscriber` turns an existing physical standby into a logical subscriber at a consistent LSN, so no initial table copy is needed. The docs target large databases and recommend ordinary logical replication with `copy_data` for smaller ones.

## Requirements
- Target is a physical standby of the source with the same system identifier, on the same major version as pg_createsubscriber; it must **not already be running** (the tool starts it itself and errors out if it is running).
- Source: `wal_level = logical`, `max_replication_slots` at least the number of databases plus existing slots, `max_wal_senders` at least the number of databases plus existing WAL senders; the source must accept connections from the target and must not be in recovery.
- Target: `max_active_replication_origins` and `max_logical_replication_workers` at least the number of databases, `max_worker_processes` greater than that number, local connections accepted; the target user needs privileges to create subscriptions and to use `pg_replication_origin_advance()`.

## Run
```bash
pg_createsubscriber --dry-run \
  -D <STANDBY_DATA_DIR> \
  -P "host=pg1 port=5432 user=postgres" \
  -d appdb -d billing \
  --publication=pub_app --publication=pub_billing \
  --subscription=sub_app --subscription=sub_billing \
  --verbose
# then the same without --dry-run
```
The number of `--publication`, `--subscription` and `--replication-slot` names must match the number of databases and follow the same order (or omit them for generated names; `--all` creates one subscription per database). What it does: creates a `FOR ALL TABLES` publication and a replication slot per database on the source, sets `recovery_target_lsn` to the last slot's LSN with `promote` as the action, creates the subscriptions (not enabled until the replication progress is set to that start point), drops the replicated publications on the target, drops the standby's `primary_slot_name` slot and failover slots, and finally updates the target's system identifier with pg_resetwal.

## After conversion
```sql
-- on the new subscriber
SELECT subname, subenabled FROM pg_subscription;
SELECT * FROM pg_stat_subscription;
-- on the source
SELECT slot_name, active, confirmed_flush_lsn FROM pg_replication_slots;
```
For a major upgrade, see the logical replication upgrade chapter: pg_upgrade attempts to migrate logical slots (old cluster 17.0 or later) and subscription dependencies, subject to documented prerequisites.

## Gotchas
- Only the databases you name (or all with `--all`) get subscriptions.
- All logical replication restrictions still apply after conversion; avoid DDL on the source while the tool runs, since DDL is not replicated.
- If the tool fails after the target was promoted, the docs say the data directory is likely not recoverable and a new standby should be created.
- If it fails earlier, publications and slots created on the source are removed, but removal can fail if the target cannot reach the source; a warning lists leftovers.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): pg_createsubscriber reference (description, options `-a`, `-d`, `-D`, `-n`, `-P`, `--publication`, `--subscription`, `--replication-slot`, name-count rule, the prerequisites list for source and target, the "How It Works" steps including recovery target LSN, drop of replicated publications and standby slots, and the pg_resetwal system identifier update, and the warnings) and the logical replication upgrade section on pg_upgrade migrating slots and subscriptions. Corrected: the target must be stopped (the tool errors if it is running), and the multi-database example now gives one publication and subscription name per database as the docs require. Removed the PG17 version gate, the OS-user and cascading-standby remarks, which the documentation does not give.
Method: documentation only; no commands were run.
