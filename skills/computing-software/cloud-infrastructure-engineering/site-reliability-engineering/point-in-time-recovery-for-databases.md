---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.point-in-time-recovery-for-databases
name: point-in-time-recovery-for-databases
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [point-in-time-recovery, pitr, wal-archiving, data-integrity, backup, restore-drill]
level: practitioner
status: docs-checked
description: "Design and drill point-in-time recovery (base backup plus continuous WAL archive) for PostgreSQL, with archive monitoring, retention and validation."
sources: ["https://sre.google/sre-book/data-integrity/", "https://www.postgresql.org/docs/current/continuous-archiving.html", "https://www.postgresql.org/docs/current/runtime-config-wal.html", "https://www.postgresql.org/docs/current/monitoring-stats.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Point-in-time recovery (PITR)

**Goal:** restore a database to just before a bad write (bug, bad migration, operator error), not just to last night.

The SRE Book (Data Integrity) calls this "point-in-time recovery" outside Google and "time-travel" inside it. Its
study of 19 Google data recovery efforts found the most common user-visible loss scenarios were deletion or loss of
referential integrity caused by software bugs, hardest when discovered weeks to months later. It also stresses that
replication is not recoverability: synced replicas push a corrupt row or errant delete to every copy.

## Ingredients (PostgreSQL continuous archiving)
1. A **base backup** (`pg_basebackup` is the easiest way to make one).
2. A **continuous sequence of archived WAL files** reaching back at least to the start of the backup. Set up and
   test WAL archiving before you take the first base backup.
3. Enough archive storage: the base backup may be bulky and a busy system generates a lot of WAL.
4. A restore procedure you have timed. The interval between base backups trades archive storage against replay
   time, since recovery replays all WAL since the last base backup.

## PostgreSQL
Enable archiving: `wal_level` of `replica` or higher, `archive_mode = on`, and either `archive_command` (shell
command) or `archive_library`, normally in `postgresql.conf`.

Restore: restore the base backup, set recovery settings in `postgresql.conf`, create an empty `recovery.signal`
file in the cluster data directory, and start the server. For example:
```conf
restore_command = 'cp /mnt/server/archivedir/%f %p'
recovery_target_time = '2026-11-02 09:14:00+00'
recovery_target_inclusive = off
recovery_target_action = 'pause'
```
- At most one of `recovery_target`, `recovery_target_lsn`, `recovery_target_name`, `recovery_target_time` or
  `recovery_target_xid` may be set.
- `recovery_target_inclusive` (default `on`) controls whether the transaction at exactly the target is included;
  `off` stops just before it.
- `recovery_target_action` defaults to `pause`, which lets you query to check the point is right; if not, shut
  down, set a later target and restart. `promote` ends recovery and accepts connections; `shutdown` stops the
  server. With `shutdown`, `recovery.signal` is not removed.
- The stop point must be after the end of the base backup; to recover to a time during a backup, use the previous
  base backup. Upon completion the server removes `recovery.signal`.
- You may want to restrict `pg_hba.conf` during recovery so users do not connect before you are sure it worked.
- By default recovery follows the latest timeline in the archive; `recovery_target_timeline` selects another.

## Operating it
- Restore into a side instance, extract the affected rows, merge back; full cutover only for total loss.
- Monitor archiving through `pg_stat_archiver` (it has `last_archived_time` and `last_failed_time`). Note that
  some archiver failures (killed by a signal, shell exit status above 125) abort the archiver and are not
  reported there, so also watch the server log.
- Test restores regularly: restore to a chosen time, run integrity checks and an application smoke test; record elapsed time.
- Protect backups from the same blast radius as production.
- Managed services (Amazon RDS, Cloud SQL, Azure) offer their own point-in-time restore; read the vendor docs for commands.

## Verify
A drill restores to the chosen timestamp and a known row inserted before/after is present/absent as expected.

## Checked

Checked 2026-11-09. Confirmed against the PostgreSQL continuous archiving, WAL runtime configuration and monitoring statistics pages, and the SRE Book Data Integrity page. Removed: the pgbackrest commands, the aws rds restore command, the monthly-test cadence, the immutability and separate-account advice, and the claim that targets cannot be rewound, none of which appeared on a page read.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
