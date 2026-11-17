---
id: computing-software.database-administration.cockroachdb.point-in-time-restore
name: point-in-time-restore
category: computing-software
field: database-administration
product: cockroachdb
tags: [point-in-time-restore, revision-history, as-of-system-time, backup, restore]
level: practitioner
status: docs-checked
description: "Take CockroachDB backups with revision_history and restore to a chosen timestamp with RESTORE ... AS OF SYSTEM TIME, including the limits of what is restored."
sources:
  - https://www.cockroachlabs.com/docs/stable/take-backups-with-revision-history-and-restore-from-a-point-in-time
  - https://www.cockroachlabs.com/docs/stable/take-full-and-incremental-backups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: recover to a specific moment, for example just before a bad deploy or accidental delete.

Take the backup with revision history, which records changes over time rather than only the latest state:
```sql
BACKUP INTO '{collectionURI}' AS OF SYSTEM TIME '-10s' WITH revision_history;
```
Restore to a timestamp inside the covered window:
```sql
RESTORE FROM '/2021/12/13-211056.62' IN '{collectionURI}' AS OF SYSTEM TIME '2021-12-13 10:00:00';
```

Important behaviour: `RESTORE` brings back only the latest data in the object, or the data as of the `AS OF SYSTEM TIME` you give. It does not restore historical revisions, even if the backup captured them. The revision history is used to reconstruct a chosen point, not to rebuild the version history inside the restored cluster.

Dependencies on GC: if the GC TTL of the target is shorter than the frequency of incremental backups with revision history, the revisions can be garbage collected before they are backed up and the incremental backup fails. Configure the GC period (`ttlseconds`) to at least the incremental frequency, ideally with a buffer. Incremental backups created by a schedule protect their revision data, which allows a lower GC TTL.

Verify: after restore, query the affected rows and confirm they match the chosen timestamp.

## Checked
2026-11-03. Confirmed on the revision history page and the full and incremental backups page: `BACKUP ... WITH revision_history` example, the `RESTORE FROM '/2021/12/13-211056.62' IN ... AS OF SYSTEM TIME` example, restore returns only latest data and no historical revisions, GC TTL versus incremental frequency and schedule protection. Removed: the `protected ts verification error` name, the Common Errors and restore-rules cross-references, and the SHOW BACKUP verify step.
Method: documentation only; no commands were run.
