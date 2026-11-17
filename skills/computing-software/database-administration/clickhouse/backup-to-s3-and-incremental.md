---
id: computing-software.database-administration.clickhouse.backup-to-s3-and-incremental
name: backup-to-s3-and-incremental
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, backup, s3, incremental, base-backup, restore]
level: practitioner
status: docs-checked
description: "Back up ClickHouse to an S3 endpoint with BACKUP ... TO S3(...), take incrementals with base_backup, and restore from the incremental."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/operations_/backup_restore/02_s3_endpoint.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# backup to s3 and incremental
The destination is `S3('<s3 endpoint>/<directory>', '<access key id>', '<secret access key>', '<extra_credentials>')`. You need an S3 endpoint, an access key ID and a secret access key.

A base backup (incrementals need one to start from):
```sql
BACKUP TABLE test_db.test_table TO S3(
'https://backup-ch-docs.s3.us-east-1.amazonaws.com/backups/base_backup',
'<access key id>',
'<secret access key>'
)
```
An incremental backup holds the difference between the base backup and the table's current content. It adds `SETTINGS base_backup` and must go to a different directory than the base, on the same endpoint:
```sql
BACKUP TABLE test_db.test_table TO S3(
'https://backup-ch-docs.s3.us-east-1.amazonaws.com/backups/incremental_backup',
'<access key id>',
'<secret access key>'
)
SETTINGS base_backup = S3(
'https://backup-ch-docs.s3.us-east-1.amazonaws.com/backups/base_backup',
'<access key id>',
'<secret access key>'
)
```
Each BACKUP returns an id and status `BACKUP_CREATED`. Restore by naming only the incremental; the base is included automatically:
```sql
RESTORE TABLE test_db.test_table AS test_db.test_table_restored FROM S3(
'https://backup-ch-docs.s3.us-east-1.amazonaws.com/backups/incremental_backup',
'<access key id>',
'<secret access key>'
)
```
The docs verify the restore with `SELECT count()` on the restored table (1,100 rows after inserts of 1,000 and 100) and a `throwIf` comparison of `groupArray(tuple(*))` of both tables.

## Checked
2026-11-03. Confirmed against the "BACKUP / RESTORE to or from an S3 endpoint" page. Removed: the `allow_concurrent_backups` and `allow_concurrent_restores` server settings, the credentials-in-query-log gotcha and named-collection advice, and `system.backups` status checks, none of which are on the page. The page's own RESTORE example names the source table `data` (apparently a typo for `test_db.test_table`); this skill uses the latter, as in the local-disk page.
Method: documentation only; no commands were run.
