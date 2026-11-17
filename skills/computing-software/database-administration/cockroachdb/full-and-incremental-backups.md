---
id: computing-software.database-administration.cockroachdb.full-and-incremental-backups
name: full-and-incremental-backups
category: computing-software
field: database-administration
product: cockroachdb
tags: [backup, full-backup, incremental-backup, backup-collections, gc-ttl, restore]
level: practitioner
status: docs-checked
description: "Take full and incremental CockroachDB backups into a collection URI, restore from LATEST, handle GC TTL, and exclude table data from backups."
sources:
  - https://www.cockroachlabs.com/docs/stable/take-full-and-incremental-backups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a reliable backup chain you can restore tables, databases or the whole cluster from.

Collections: a backup collection lives at a collection URI. Full backups sit at the root in date-based paths (for example `2022/02/09-155340.13/`); incremental backups go in an `/incrementals` directory. `SHOW BACKUPS IN '{collectionURI}'` lists full backup subdirectories.

Commands:
```sql
BACKUP INTO '{collectionURI}';                 -- full
BACKUP INTO LATEST IN '{collectionURI}';       -- incremental on the latest full
RESTORE FROM LATEST IN '{collectionURI}';      -- full cluster
RESTORE DATABASE bank FROM LATEST IN '{collectionURI}';
RESTORE TABLE bank.customers FROM LATEST IN '{collectionURI}';
RESTORE DATABASE bank FROM {subdirectory} IN '{collectionURI}';
```
The page recommends nightly full backups of the cluster; incrementals form chains between fulls and are typically smaller and faster. Consistent backup of a live database example: `BACKUP DATABASE movr INTO '...' AS OF SYSTEM TIME '-10s';` and restore under a new name with `WITH new_db_name = new_movr`.

GC TTL gotcha: with revision history, if the target's GC TTL (`ttlseconds` in the replication zone) is shorter than your incremental frequency, revisions can be garbage collected before the next backup and you get a `protected ts verification error`. Set the GC period to at least the backup frequency with buffer.

Exclude data: `ALTER TABLE movr.user_promo_codes SET (exclude_data_from_backup = true);` the table is restored with schema but no rows.

Prefer schedules (`CREATE SCHEDULE ... FOR BACKUP`) over hand-run jobs for production.

Verify: `SHOW BACKUPS IN` and `SHOW BACKUP FROM LATEST IN` list the expected chain.

## Checked
2026-11-03. Confirmed on the full and incremental backups page: date-based full paths, `/incrementals` directory, `BACKUP INTO LATEST IN`, the `BACKUP DATABASE movr ... AS OF SYSTEM TIME '-10s'` and `new_db_name` examples, nightly full backups and scheduled backups recommendation, GC TTL at least the incremental frequency, and `exclude_data_from_backup`. Removed: the periodic restore test advice.
Method: documentation only; no commands were run.
