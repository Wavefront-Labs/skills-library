---
id: computing-software.database-administration.yugabytedb.snapshot-external-storage-move
name: snapshot-external-storage-move
category: computing-software
field: database-administration
product: yugabytedb
tags: [snapshots, export-snapshot, import-snapshot, ysql-dump, catalog-version, external-backup, restore]
level: advanced
status: docs-checked
description: "Move a YSQL snapshot to another cluster or storage: verify catalog version, dump schema with ysql_dump, export_snapshot, copy tablet snapshot files, then import."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/backup-restore/snapshot-ysql.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/manage/backup-restore/export-import-data-ysql.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Moving a snapshot to external storage

Backup (the schema and the data are saved separately):
1. Record the catalog version: `SELECT yb_catalog_version();`
2. Dump metadata:
```
./postgres/bin/ysql_dump -h <ip> --include-yb-metadata --serializable-deferrable --create --schema-only --dbname <database_name> --file <database_name>_schema.sql
```
3. Create the snapshot (`create_database_snapshot ysql.<database_name>`) and note its id.
4. Check `yb_catalog_version()` again. If it changed, DDL ran in between, so the dump and the snapshot may not match; start over.
5. Export snapshot metadata:
```
yb-admin --master_addresses <masters> export_snapshot <snapshot_id> <database_name>.snapshot
```
6. Copy the metadata file, the schema dump and the snapshot directories of every tablet (each tablet's `.snapshots` directory) to storage.

Restore on the target cluster:
1. Create the database from the dump: `ysqlsh -h 127.0.0.1 --echo-all --file=<database_name>_schema.sql`
2. `yb-admin ... import_snapshot <database_name>.snapshot <database_name>`; it prints a mapping from old to new tablet and table ids.
3. Copy the tablet snapshot files into the new tablets' snapshot directories using that mapping.
4. Run `restore_snapshot` with the new snapshot id.

## Checked

2026-11-04. Confirmed against the YSQL snapshot backup page: yb_catalog_version check, ysql_dump flags, export_snapshot, copying each tablet's .snapshots directory, ysqlsh schema restore, import_snapshot with the old-to-new id mapping, and restore_snapshot. Removed the version-compatibility sentence, which that page does not state.

Method: documentation only; no commands were run.
