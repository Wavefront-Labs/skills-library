---
id: computing-software.database-administration.supabase.database-backups-pitr
name: database-backups-pitr
category: computing-software
field: database-administration
product: supabase
tags: [backups, pitr, restore, wal-g, retention]
level: practitioner
status: docs-checked
description: "Supabase backups and Point-in-Time Recovery: retention by plan, restore caveats, WAL archiving every two minutes and how PITR pricing works."
sources:
  - https://supabase.com/docs/guides/platform/backups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand what can be restored and how far back.

Daily backups are automatic on Pro (7 days), Team (14 days) and Enterprise (up to 30 days). Free projects should regularly export with the CLI `db dump` command and keep off-site copies.

Caveats:
- Deleting a project permanently removes its data, including backups in S3.
- Daily backups do not store passwords for custom roles; reset them after a restore.
- Backups exclude Storage API objects (only metadata lives in the database), so restoring does not bring back objects deleted later.
- Projects on Postgres `15.8.1.079` and newer use physical backups; older ones must upgrade first.
- Restoring makes the project inaccessible; downtime grows with database size.
- Drop subscriptions and replication slots before a restore and recreate them afterwards (the Realtime slot is handled automatically).
- Pick the closest backup before your target time; earlier ones may lose more data.

PITR is an add-on for Pro, Team and Enterprise, needing at least the Small compute add-on. Enabling it stops daily backups. It combines physical snapshots with WAL archiving via WAL-G. WAL files are backed up every two minutes by default, or immediately when over a size threshold, none during inactivity. Worst-case RPO is two minutes. Restores must fall between the earliest and latest recovery points: the latest physical backup is downloaded and WAL replayed to the chosen time.

Pricing depends on the recovery retention period (7, 14 or 28 days); see Supabase's pricing page for current figures.

After disabling PITR, new backups are physical only: still usable for restoration but not available for direct download; for a downloadable copy take a manual logical backup with the Supabase CLI or `pg_dump`.

## Checked

2026-11-04: Read the Database Backups guide in full (rendered text was truncated at the top, so the page's Markdown source on GitHub was read too). Confirmed retention by plan, caveats, physical-backup version, restore process, PITR requirements and WAL-G behaviour. Removed the dollar figures (prices change; the page's pricing table is not kept) and corrected the post-PITR download wording.
Method: documentation only; no commands were run.
