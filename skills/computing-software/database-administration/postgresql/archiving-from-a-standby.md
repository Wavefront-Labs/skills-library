---
id: computing-software.database-administration.postgresql.archiving-from-a-standby
name: archiving-from-a-standby
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, archive-mode-always, wal-archiving, standby, restore-command, continuous-archiving, high-availability]
level: practitioner
status: docs-checked
description: "Archive WAL from a PostgreSQL standby with archive_mode=always so archiving survives failover, and use restore_command as a fallback when streaming falls behind."
sources:
  - https://www.postgresql.org/docs/current/warm-standby.html#CONTINUOUS-ARCHIVING-IN-STANDBY
  - https://www.postgresql.org/docs/current/runtime-config-wal.html#GUC-ARCHIVE-MODE
  - https://www.postgresql.org/docs/current/warm-standby.html#STREAMING-REPLICATION
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Archiving from a standby (archive_mode = always)

## archive_mode values
| Value | Primary | Standby |
|---|---|---|
| `off` | no archiving | — |
| `on` | archives | does **not** archive; after promotion it starts archiving only new WAL |
| `always` | archives | archives every segment it receives (streamed or restored) |

With `on`, a promoted standby archives only WAL and timeline history files it generated itself, so any WAL that never reached the archive from the old primary leaves a gap. The docs say a complete series needs all WAL archived before it reaches the standby; with streaming replication `always` on the standby archives what it receives. `archive_mode` cannot be enabled when `wal_level = minimal`.

## Setup
```ini
# standby postgresql.conf
archive_mode = always               # restart required
archive_command = 'test ! -f /archive/%f && cp %p /archive/%f'   # or your tool (pgBackRest/WAL-G)
```
Primary and standby writing to the **same** archive: identical segment names with identical content will collide. Make the command idempotent — if the file exists with the same checksum, return 0; if different, fail loudly. pgBackRest/WAL-G handle this; naive `test ! -f` returns failure on duplicates and stalls archiving forever. Either archive from only one node with `always`, or use a tool that dedups.

## restore_command as streaming fallback
```ini
# standby
primary_conninfo = 'host=pg1 user=replicator application_name=pg2'
restore_command  = 'cp /archive/%f %p'
```
Standby mode loops through three sources: `restore_command` from the archive, then `pg_wal`, then streaming from the primary; when streaming disconnects it goes back to the archive. So a standby that falls behind what the primary still retains can catch up from the archive.

## Verify
```sql
-- on the standby
SELECT archived_count, last_archived_wal, last_archived_time, failed_count, last_failed_wal FROM pg_stat_archiver;
SELECT pg_is_in_recovery(), pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn();
```

## Gotchas
- On a standby, `archive_command` failures make WAL accumulate in the standby's pg_wal; monitor its disk too.
- Timeline history files (`*.history`) must be archived; tools handle it, hand-written scripts sometimes filter them out.

## Checked
2026-10-25. Against PostgreSQL 18 documentation (REL_18_STABLE doc/src/sgml, branch head 2026-10-24; PostgreSQL 19 is still at release-candidate stage): high-availability chapter (Continuous Archiving in Standby: `always` versus `on`, shared-archive requirements for identical-content and race-free archiving, promotion behaviour; the standby restore loop), `archive_mode` and `archive_command` parameter text, and the `pg_stat_archiver` columns used in the verify query. Removed the quoted error and log-line texts, which the documentation does not give.
Method: documentation only; no commands were run.
