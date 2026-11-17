---
id: computing-software.database-administration.postgresql.monitoring-logical-replication
name: monitoring-logical-replication
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, logical-replication, pg-stat-subscription, pg-stat-subscription-stats, replication-slots, monitoring, replica-lag]
level: practitioner
status: docs-checked
description: "Monitor logical replication health: apply lag from slots and pg_stat_subscription, sync state per table, apply errors, and slots that silently retain WAL."
sources:
  - https://www.postgresql.org/docs/current/logical-replication-monitoring.html
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-SUBSCRIPTION
  - https://www.postgresql.org/docs/current/view-pg-replication-slots.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring logical replication

## Publisher side: the slot is the truth
```sql
SELECT slot_name, active, active_pid, wal_status,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)) AS lag_bytes,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn))        AS retained_wal,
       inactive_since                                                            -- newer versions only
FROM pg_replication_slots WHERE slot_type = 'logical';

SELECT application_name, state, replay_lag FROM pg_stat_replication;   -- walsenders for subscriptions
-- decoding cost per slot: spills to disk when a transaction exceeds logical_decoding_work_mem
SELECT slot_name, spill_txns, spill_bytes, stream_txns, total_txns FROM pg_stat_replication_slots;
```
- `confirmed_flush_lsn` lagging = subscriber not keeping up or stopped.
- `retained_wal` growing while `active = false` = subscriber down; the primary's disk is at risk.
- High `spill_bytes` = big transactions; consider raising `logical_decoding_work_mem` (the stats docs say the spill counters allow tuning it).

## Subscriber side
```sql
SELECT subname, pid, relid::regclass, received_lsn, latest_end_lsn,
       last_msg_receipt_time, latest_end_time
FROM pg_stat_subscription;                        -- relid not null = tablesync worker
SELECT subname, apply_error_count, sync_error_count, stats_reset
FROM pg_stat_subscription_stats;                  -- newer versions only
```
`sync_error_count` counts errors during initial table synchronization; tables that stay unsynchronised for hours are big copies or failing (check the log).

## Errors
The subscriber log shows the conflict that stopped the apply worker.
`apply_error_count` in `pg_stat_subscription_stats` counts errors while applying changes.

## Alerts
- Slot `active = false` for longer than your tolerance, or retained WAL above a threshold.
- `lag_bytes` above budget for a sustained period.
- `apply_error_count` / `sync_error_count` delta > 0.

## Gotchas
- Lag can grow during big DDL-free batch updates because each row change is decoded and
  applied individually.

## Verify
Insert a heartbeat row on the publisher with `now()` and read it on the subscriber; its age
is your end-to-end apply lag.

## Checked

2026-10-28. Confirmed against the PostgreSQL pg_replication_slots page and the statistics views page: wal_status, confirmed_flush_lsn, inactive_since, pg_stat_replication_slots spill_txns and spill_bytes (tunable with logical_decoding_work_mem), pg_stat_subscription_stats apply_error_count and sync_error_count. Removed: PG14/15/17 version tags, pg_subscription_rel state letters and the not-ready query, pg_subscription and disable_on_error claims, streaming = on/parallel advice, the sample error text and the 5 and 10 minute thresholds (not confirmed in the fetched pages).

Method: documentation only; no commands were run.
