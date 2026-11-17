---
id: computing-software.database-administration.postgresql.monitoring-replication-lag
name: monitoring-replication-lag
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, streaming-replication, pg-stat-replication, pg-stat-wal-receiver, replica-lag, monitoring, alerting]
level: practitioner
status: verified
description: "Measure PostgreSQL replication lag in bytes and time from pg_stat_replication and the standby, tell network, disk and replay lag apart, and alert correctly."
sources:
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-REPLICATION-VIEW
  - https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-WAL-RECEIVER-VIEW
  - https://www.postgresql.org/docs/current/warm-standby.html#STREAMING-REPLICATION-MONITORING
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Monitoring replication lag

## On the primary: the four LSNs
```sql
SELECT application_name, client_addr, state, sync_state,
       pg_wal_lsn_diff(pg_current_wal_lsn(), sent_lsn)   AS send_lag_b,
       pg_wal_lsn_diff(sent_lsn, write_lsn)              AS net_write_lag_b,
       pg_wal_lsn_diff(write_lsn, flush_lsn)             AS fsync_lag_b,
       pg_wal_lsn_diff(flush_lsn, replay_lsn)            AS replay_lag_b,
       write_lag, flush_lag, replay_lag                  -- intervals (PG10+)
FROM pg_stat_replication;
```
Where the gap sits tells you the bottleneck:
| Large gap | Cause |
|---|---|
| current -> sent | walsender can't read/send fast enough (CPU, primary I/O) |
| sent -> write | network bandwidth/latency |
| write -> flush | standby disk fsync slow |
| flush -> replay | replay slow, or **paused by a query conflict** (`max_standby_streaming_delay`), or `recovery_min_apply_delay` |

`write_lag/flush_lag/replay_lag` are time intervals measured from commit; the docs say they stay visible for a short time
after the standby has caught up and then show NULL (on 18.6: still a few ms 16 s after the last write, NULL by about a minute), which is fine (no lag).

## On the standby
```sql
SELECT status, sender_host, written_lsn, flushed_lsn, latest_end_time,
       last_msg_receipt_time FROM pg_stat_wal_receiver;   -- no received_lsn column since PG13
SELECT now() - pg_last_xact_replay_timestamp() AS replay_delay,
       pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn(),
       pg_is_wal_replay_paused();
```
`now() - pg_last_xact_replay_timestamp()` grows during **idle periods** on the primary even
with zero lag, because there is nothing to replay. Alert on it only together with
`pg_last_wal_receive_lsn() <> pg_last_wal_replay_lsn()`, or generate a heartbeat write
(e.g. update a one-row table every 10 s) and measure its age on the standby.

## Slots
```sql
SELECT slot_name, active, wal_status,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained
FROM pg_replication_slots;
```
`wal_status = 'lost'` means the standby can no longer catch up from this slot.

## Alerts worth having
- Standby missing from `pg_stat_replication` (disconnected) for > 1 min.
- `replay_lag` > your RPO/read-staleness budget (e.g. 30 s) for 5 min.
- Retained WAL per slot > 50% of `max_slot_wal_keep_size` or free disk.
- `sync_state` changed from `sync` (a synchronous standby dropped, commits may hang or degrade).

## Gotchas
- Long reporting queries on a standby with `max_standby_streaming_delay = -1` can pause replay
  for hours; that shows as flush->replay lag only.
- Large DDL (index builds, `VACUUM FULL`) produces bursts of WAL; short lag spikes are normal.

## Verify
Generate load (`pgbench`) and watch the byte gaps rise and drain; disconnect the standby
and confirm the alert fires.

## Checked
- PostgreSQL 18.6 primary with a streaming standby: after inserting 100000 rows the `pg_stat_replication` query returned `send_lag_b` 4341208, `net_write_lag_b` 393216, `fsync_lag_b` 0, `replay_lag_b` 40 and sub-100 ms `write_lag`/`flush_lag`/`replay_lag`, and the byte gaps drained; the intervals were `00:00:00.0003`-ish 16 s later and NULL (`||`) after about a minute. The standby query returned `pg_last_wal_receive_lsn()` / `pg_last_wal_replay_lsn()` / `pg_is_wal_replay_paused()` = f; `now() - pg_last_xact_replay_timestamp()` grew to 7.5 s on an idle primary with zero lag (as the skill says). `pg_stat_wal_receiver` columns `written_lsn`, `flushed_lsn`, `latest_end_time`, `last_msg_receipt_time` exist (no `received_lsn`); the slot query returned `reserved`, `active = t`.
- Docs: monitoring-stats (`write_lag` etc., the idle-then-NULL wording), view-pg-replication-slots (`wal_status` values), hot-standby / runtime-config-replication (`max_standby_streaming_delay`, `recovery_min_apply_delay`).
- Alert thresholds are suggestions, not documented values.
