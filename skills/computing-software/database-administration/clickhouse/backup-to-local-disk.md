---
id: computing-software.database-administration.clickhouse.backup-to-local-disk
name: backup-to-local-disk
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, backup, restore, disk, allowed-disk, base-backup]
level: practitioner
status: docs-checked
description: "Back up and restore ClickHouse tables to a configured backup disk: allowed_disk config, incremental, password, tar and partition options."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/operations_/backup_restore/01_local_disk.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# backup to local disk
The Disk backup engine needs a destination file, e.g. `/etc/clickhouse-server/config.d/backup_disk.xml`, that defines a disk and adds it to the backups allow-list:
```xml
<clickhouse>
    <storage_configuration>
        <disks>
            <backups>
                <type>local</type>
                <path>/backups/</path>
            </backups>
        </disks>
    </storage_configuration>
    <backups>
        <allowed_disk>backups</allowed_disk>
        <allowed_path>/backups/</allowed_path>
    </backups>
</clickhouse>
```
Back up and restore (the restore works if the table is empty):
```sql
BACKUP TABLE test_db.test_table TO Disk('backups', '1.zip')
RESTORE TABLE test_db.test_table FROM Disk('backups', '1.zip')
RESTORE TABLE test_db.test_table AS test_db.test_table_renamed FROM Disk('backups', '1.zip')
```
Each returns an id and a status (`BACKUP_CREATED`, `RESTORED`). Restore into a non-empty table fails unless `SETTINGS allow_non_empty_tables=true`, which mixes old and restored data and can duplicate rows.

Incremental: take a base backup, then set `base_backup`; the base must stay available to restore any incremental.
```sql
BACKUP TABLE test_db.test_table TO Disk('backups', 'd.zip')
BACKUP TABLE test_db.test_table TO Disk('backups', 'incremental-a.zip')
SETTINGS base_backup = Disk('backups', 'd.zip')
```
Other options from the page: `SETTINGS password='...'` (zip/zipx only; other formats give `BAD_ARGUMENTS`), tar archives via the file suffix (`.tar`, `.tar.gz`, `.tgz`, `.tar.bz2`, `.tar.lzma`, `.tar.zst`, `.tzst`, `.tar.xz`; no password), `compression_method='lzma', compression_level=3`, and `BACKUP TABLE test_db.partitioned PARTITIONS '1', '4' TO Disk('backups', 'partitioned.zip')` with the same `PARTITIONS` clause on RESTORE. An S3 disk (`s3_plain`) can be used the same way but should not be used for MergeTree itself.

## Checked
2026-11-03. Confirmed against the "BACKUP / RESTORE to disk" page. Removed: `ASYNC`, `ALL`, `system.backups` and `system.backup_log` polling, the "backup path not allowed" error text, the separate-volume advice, and the Verify step, none of which are on the page.
Method: documentation only; no commands were run.
