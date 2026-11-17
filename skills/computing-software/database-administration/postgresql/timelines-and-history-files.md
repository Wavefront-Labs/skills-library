---
id: computing-software.database-administration.postgresql.timelines-and-history-files
name: timelines-and-history-files
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, continuous-archiving, timeline-history, recovery-target-timeline, pitr, promotion]
level: advanced
status: verified
description: "How promotion and PITR fork PostgreSQL timelines, how .history files and recovery_target_timeline pick a path, and fixing 'timeline is not a child' errors."
sources:
  - https://www.postgresql.org/docs/current/continuous-archiving.html#BACKUP-TIMELINES
  - https://www.postgresql.org/docs/current/runtime-config-wal.html#RUNTIME-CONFIG-WAL-RECOVERY-TARGET
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timelines and history files

## Concept
Every time a cluster ends recovery and starts accepting writes (standby promotion, or the end
of a point-in-time recovery), it starts a **new timeline ID** (TLI). WAL segment names begin
with the TLI: `00000002000000A3000000F1` is timeline 2. This keeps the WAL of the old
history and the new history from overwriting each other in the archive.

On promotion the server writes `0000000N.history` to `pg_wal` and the archive:
```
1	0/A3F1C2D8	no recovery target specified
```
"Timeline 2 branched from timeline 1 at LSN 0/A3F1C2D8."

## recovery_target_timeline
| Value | Behaviour |
|---|---|
| `latest` (default since PG12) | follow the newest timeline found in the archive |
| `current` | stay on the timeline of the base backup |
| a number | follow that specific timeline |
With `latest`, a restore follows whatever promotion happened last, which is usually right for
a standby, but **wrong** when you are restoring to a time *before* a failover on the old
branch: then set the timeline explicitly.

## Common errors
- `requested timeline 3 is not a child of this server's history` - the base backup or data
  directory is on a branch that timeline 3 did not fork from (e.g. an old primary that kept
  writing after a standby was promoted). Fix: `pg_rewind` the old node or rebuild it.
- `could not start WAL streaming: ERROR:  requested starting point 0/27000000 on timeline 1 is not in this server's history` with `DETAIL:  This server's history forked from timeline 1 at 0/26003CF8.` (seen when a former primary that wrote past the fork tried to follow the new one), followed by
- `new timeline 2 forked off current database system timeline 1 before current recovery point
  - the node replayed past the fork point; same fix.
- PITR repeated several times leaves timelines 2, 3, 4 in the archive; a later restore with
  `latest` may follow an abandoned experiment, so set `recovery_target_timeline` explicitly when you do not want the newest
  branch. The docs call history files small and cheap to keep indefinitely, and you can add comments to them.

## Inspecting
```bash
ls $ARCHIVE/*.history; cat $ARCHIVE/00000003.history
pg_controldata $PGDATA | grep -i timeline
```
```sql
SELECT timeline_id, redo_lsn FROM pg_control_checkpoint();
SELECT received_tli FROM pg_stat_wal_receiver;     -- on a standby
```

## Gotchas
- Archive the `.history` files like segments: the docs say they are necessary to pick the right segment files when recovering from an archive that holds several timelines.
- Third-party backup tools have their own options for choosing the target timeline; read their documentation.
- A cascaded standby follows the new timeline automatically only if it can fetch the
  history file (streaming or archive).

## Verify
After a restore or promotion, `pg_control_checkpoint()` shows the expected timeline (after the end-of-recovery checkpoint; it still showed 1 right after `pg_promote`) and
`pg_wal` contains the new `.history` file, also present in the archive.

## Checked
- PostgreSQL 18.6: promoting a standby with `pg_promote` logged `selected new timeline ID: 2`, created `00000002.history` containing `1<TAB>0/26003CF8<TAB>no recovery target specified`, and `pg_wal` then held both `000000010000000000000026` and `000000020000000000000026` (timeline in the first 8 hex digits); `pg_control_checkpoint()` showed timeline 1 immediately after `pg_promote` and 2 after the next checkpoint; `pg_controldata` listed `Latest checkpoint's TimeLineID`; `pg_stat_wal_receiver.received_tli` exists. A former primary that had written past the fork and was started as a standby of the new primary logged `requested starting point 0/27000000 on timeline 1 is not in this server's history`, `This server's history forked from timeline 1 at 0/26003CF8` and `new timeline 2 forked off current database system timeline 1 before current recovery point 0/270000A0`; with `recovery_target_timeline = '2'` the log said `requested timeline 2 is not a child of this server's history` and with `'3'` `recovery target timeline 3 does not exist`. A cascaded standby fetched the history file over streaming (`fetching timeline history file for timeline 2 from primary server`) and logged `new target timeline is 2`.
- Docs/release notes: release 12 (`recovery_target_timeline` now defaults to `latest`, was `current`), runtime-config-wal (`current`, `latest`, numeric), continuous-archiving (history files archived like segments, cheap to keep, can be commented).
- The `could not find history file` error and the pgBackRest/WAL-G remark were removed (not reproduced).
