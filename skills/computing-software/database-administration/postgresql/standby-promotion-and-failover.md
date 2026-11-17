---
id: computing-software.database-administration.postgresql.standby-promotion-and-failover
name: standby-promotion-and-failover
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, streaming-replication, hot-standby, pg-promote, standby-promotion, failover, switchover, timeline, manual-failover]
level: advanced
status: verified
description: "Fail over or switch over a PostgreSQL primary manually: pick the most advanced standby, fence the old primary, promote with pg_promote, and repoint the others."
sources:
  - https://www.postgresql.org/docs/current/warm-standby-failover.html
  - https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-RECOVERY-CONTROL
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Promoting a standby

**Goal:** a new primary with the least data loss and no chance of two primaries
accepting writes.

## Planned switchover (zero loss)
1. Stop writes at the app or pooler (PgBouncer `PAUSE`).
2. Stop the primary cleanly: `pg_ctl stop -m fast`. A fast shutdown waits until
   connected walsenders have sent the shutdown checkpoint.
3. On the chosen standby confirm it received everything: its `pg_last_wal_replay_lsn()` must be at or past the old
   primary's final checkpoint (`pg_controldata` "Latest checkpoint location"). It is the *end* of that record, so it
   is slightly higher (seen: checkpoint location `0/30008A8`, standby replay `0/3000920`).
4. Promote: `SELECT pg_promote(wait => true, wait_seconds => 60);` (or `pg_ctl promote`).
5. Repoint apps; turn the old primary into a standby (`standby.signal` +
   `primary_conninfo` to the new one). After a clean shutdown with all WAL received it reattached without pg_rewind
   (log: `End of WAL reached on timeline 1`, `new target timeline is 2`); an old primary that kept writing past the
   fork point cannot (see the timelines skill) and needs `pg_rewind` or a rebuild.

## Unplanned failover
1. **Fence** the old primary first: stop it, block its port, or cut it from the
   VIP/DNS. If it may come back and accept writes, you will have split brain.
2. Choose the standby with the highest received LSN:
   ```sql
   SELECT pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn(), pg_last_xact_replay_timestamp();
   ```
3. Promote it. It starts a new timeline (`selected new timeline ID: N`).
4. Point other standbys at it: change `primary_conninfo` and reload (PG13+, no
   restart). With `recovery_target_timeline = 'latest'` (default) they follow the
   timeline switch via the archive or streaming.
5. Rebuild or `pg_rewind` the old primary before it rejoins.

## Gotchas
- Data committed on the old primary but not received by the standby is lost
  (async). Quantify it by comparing LSNs if the old host is readable.
- Replication slots are not copied to standbys (except PG17 failover slots for
  logical); recreate physical slots on the new primary for remaining standbys.
- Unlogged tables are not replicated (docs): the standby cannot read them (`cannot access temporary or unlogged relations during recovery`),
  so expect them empty after promotion.
- Use an HA manager (Patroni) for automatic failover; manual steps are for
  understanding and for when automation is broken.

## Verify
`SELECT pg_is_in_recovery();` false on the new primary; `pg_stat_replication`
on it lists the remaining standbys streaming; old primary is fenced or a standby.

## Checked
- PostgreSQL 18.6 scratch clusters: `SELECT pg_promote(wait => true, wait_seconds => 60)` returned `t`, `pg_is_in_recovery()` became f, the log said `selected new timeline ID: 2` and `00000002.history` appeared in `pg_wal`; `pg_ctl promote` printed `server promoted`. A cascaded standby (streaming from the promoted node) logged `fetching timeline history file for timeline 2 from primary server` and `new target timeline is 2`, i.e. `recovery_target_timeline = latest` followed the switch. Planned switchover test: after `pg_ctl stop -m fast` on the primary, `pg_controldata` showed `Latest checkpoint location: 0/30008A8` and the standby had `pg_last_wal_receive_lsn() = pg_last_wal_replay_lsn() = 0/3000920`; the standby promoted with all 10001 rows; the old primary with `standby.signal` and `primary_conninfo` streamed from the new primary on timeline 2. The new primary had zero rows in `pg_replication_slots` (slots are not copied). `pg_last_wal_receive_lsn()`, `pg_last_wal_replay_lsn()`, `pg_last_xact_replay_timestamp()` ran. An unlogged table on the primary raised `cannot access temporary or unlogged relations during recovery` on the standby.
- Docs/release notes: PgBouncer usage page (`PAUSE [db]`), release 13 (`primary_conninfo`/`primary_slot_name` changeable by reload), release 17 (logical failover control), app-pg-ctl (`fast` waits for walsenders to receive the shutdown checkpoint per the warm-standby page), create-table page (unlogged tables not replicated).
- Patroni is mentioned only as a pointer, not as a verified claim.
