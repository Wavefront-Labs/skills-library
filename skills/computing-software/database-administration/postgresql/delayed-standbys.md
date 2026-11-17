---
id: computing-software.database-administration.postgresql.delayed-standbys
name: delayed-standbys
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, recovery-min-apply-delay, delayed-replica, standby, human-error-recovery, pitr]
level: practitioner
status: docs-checked
description: "Run a PostgreSQL standby that applies WAL hours behind with recovery_min_apply_delay, and use it to recover from a dropped table or bad UPDATE."
sources:
  - https://www.postgresql.org/docs/current/runtime-config-replication.html#GUC-RECOVERY-MIN-APPLY-DELAY
  - https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-RECOVERY-CONTROL
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Delayed standbys (recovery_min_apply_delay)

A standby that replays commits only after a delay gives you a window to recover from human error (DROP TABLE, bad migration) without a full PITR restore.

## Setup
```ini
# standby postgresql.conf (reload)
recovery_min_apply_delay = '4h'
primary_conninfo = 'host=pg1 user=replicator application_name=pg-delayed'
primary_slot_name = 'pg_delayed'
```
WAL is still **received** immediately; only **apply** of commit records waits until `commit timestamp + delay`.
A bare number is milliseconds. The delay starts once the standby has reached a consistent state and ends when the standby is promoted. `recovery_min_apply_delay` can be set in `postgresql.conf` (reload); the `recovery_target_*` parameters can only be set at server start.

## When disaster strikes
```sql
-- on the delayed standby, immediately
SELECT pg_wal_replay_pause();
SELECT pg_is_wal_replay_paused(), pg_last_xact_replay_timestamp();
```
Then roll forward to just before the mistake:
```ini
recovery_min_apply_delay = 0
recovery_target_time = '2026-10-18 10:41:00+00'   # just before the DROP
recovery_target_action = 'pause'
```
Restart the standby (recovery_target_* changes need restart), confirm data, then either `pg_dump -t` the table and load it on the primary, or promote the standby if the primary is unusable.

## Sizing / side effects
- pg_wal on the standby (or the slot on the primary) must hold at least `delay x WAL rate`. A 4h delay at 50 MB/s is ~720 GB.
- Do not count it as an HA failover target: after promotion the standby ends recovery without further waiting, but the WAL it has not yet applied is the delay's worth of recent changes, so catch it up first (or use it only for recovery).
- With `synchronous_commit = remote_apply` and this standby in `synchronous_standby_names`, every commit waits to be applied, that is, for the full delay. Never make a delayed standby synchronous.
- Feedback from a delayed standby is itself delayed (`hot_standby_feedback`), which the docs warn can cause bloat on the primary; use both together with care.

## Verify
```sql
-- primary
SELECT application_name, replay_lag FROM pg_stat_replication WHERE application_name = 'pg-delayed';
```
`replay_lag` should hover around the configured delay; far more means apply cannot keep up.

## Gotchas
- The delay is measured from the primary's commit timestamp; clock skew between hosts shifts it.
- Only commit records are delayed; a long-running transaction's changes appear as soon as its commit passes the delay.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): `recovery_min_apply_delay` (default 0, milliseconds without units, delay measured from the primary's WAL timestamp against the standby clock, commit records only, begins at consistent state and ends at promotion, WAL accumulates in the standby `pg_wal`, `hot_standby_feedback` delayed, `remote_apply` commits wait), the Recovery Target parameters (set at server start only; `recovery_target_action` default `pause`), and the `pg_wal_replay_pause` and `pg_last_xact_replay_timestamp` functions. Removed the earlier run-based timing figures, which were not re-confirmable from documentation.
Method: documentation only; no commands were run.
