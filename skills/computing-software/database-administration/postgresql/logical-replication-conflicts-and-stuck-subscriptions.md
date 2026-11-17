---
id: computing-software.database-administration.postgresql.logical-replication-conflicts-and-stuck-subscriptions
name: logical-replication-conflicts-and-stuck-subscriptions
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-logical-replication, logical-replication-conflicts, alter-subscription-skip, disable-on-error, pg-stat-subscription-stats, replication-origin, unique-violation]
level: practitioner
status: docs-checked
description: "Diagnose and clear a PostgreSQL logical replication subscription stuck on a conflict: read the error, fix data or ALTER SUBSCRIPTION SKIP, and prevent retry storms."
sources:
  - https://www.postgresql.org/docs/current/logical-replication-conflicts.html
  - https://www.postgresql.org/docs/current/sql-altersubscription.html
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-SUBSCRIPTION-STATS
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logical replication conflicts and stuck subscriptions

**Goal:** get an apply worker that keeps failing on the same change moving again without silent data loss.

## Symptom
Subscriber log repeats every few seconds:
```
ERROR:  duplicate key value violates unique constraint "orders_pkey"
CONTEXT:  processing remote data for replication origin "pg_16395" during message type "INSERT"
          for replication target relation "public.orders" in transaction 7421, finished at 0/1A2B3C4D
```
Apply stops; publisher slot retains WAL and grows the disk.
```sql
SELECT subname, apply_error_count, sync_error_count FROM pg_stat_subscription_stats;
SELECT slot_name, active, pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)) FROM pg_replication_slots; -- publisher
```

## Fix options, best first
1. **Fix the data on the subscriber** so the change applies (delete the duplicate row that someone wrote locally, add the missing parent row). Apply resumes automatically.
2. **Skip the transaction** with `ALTER SUBSCRIPTION ... SKIP`, using the `finished at` LSN from the log:
   ```sql
   ALTER SUBSCRIPTION sub_orders DISABLE;
   ALTER SUBSCRIPTION sub_orders SKIP (lsn = '0/1A2B3C4D');
   ALTER SUBSCRIPTION sub_orders ENABLE;
   ```
   The whole remote transaction is skipped, not just the failing row; reconcile those rows by hand.
3. Alternatively `SELECT pg_replication_origin_advance('pg_16395', '0/1A2B3C4E');` with the subscription disabled (node name from the log, here `pg_16395`; the LSN is the next LSN after the finish LSN).

## Prevent retry storms
```sql
ALTER SUBSCRIPTION sub_orders SET (disable_on_error = true);   -- disables the subscription on error instead of retrying
```
Alert on `pg_subscription.subenabled = false` and on slot lag at the publisher.

## Causes worth fixing at the source
- Writes to replicated tables on the subscriber: revoke INSERT/UPDATE/DELETE from app roles there.
- Schema drift: DDL is not replicated; apply DDL on the subscriber first (additive), then the publisher.
- Sequences are not replicated; resync before cutover.

## Gotchas
- A missing row on UPDATE or DELETE is reported as the `update_missing` / `delete_missing` conflict types (see the Conflicts page for your version) and counted in `pg_stat_subscription_stats`. Run row-count/checksum comparisons periodically.

## Verify
`apply_error_count` stops increasing, `pg_stat_subscription.latest_end_lsn` advances, and the publisher slot lag shrinks.

## Checked

2026-10-28. Confirmed against PostgreSQL docs (version 18): logical replication Conflicts page (skip a transaction with ALTER SUBSCRIPTION ... SKIP using the finish LSN, pg_replication_origin_advance with node name such as pg_16395 and next LSN, disable_on_error, update_missing and delete_missing conflicts), ALTER SUBSCRIPTION page, pg_stat_subscription_stats (apply_error_count). Removed unconfirmed: all version gates (15+, pre-15, before 18), the replica-identity error note, the SKIP exact-LSN condition.

Method: documentation only; no commands were run.
