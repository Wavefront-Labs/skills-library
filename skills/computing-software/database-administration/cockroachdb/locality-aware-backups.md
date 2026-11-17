---
id: computing-software.database-administration.cockroachdb.locality-aware-backups
name: locality-aware-backups
category: computing-software
field: database-administration
product: cockroachdb
tags: [locality-aware-backups, cockroach-locality, backup-regions, show-locality, strict-option]
level: advanced
status: docs-checked
description: "Write CockroachDB backups to per-region buckets using COCKROACH_LOCALITY URIs and restore from them, including incrementals and the default URI ordering."
sources:
  - https://www.cockroachlabs.com/docs/stable/take-and-restore-locality-aware-backups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep each region's backup data in a bucket in that region.

Create: pass a list of URIs; one carries `COCKROACH_LOCALITY=default` and others carry URL-encoded node localities.
```sql
BACKUP INTO
  ('s3://us-east-bucket?COCKROACH_LOCALITY=default',
   's3://us-west-bucket?COCKROACH_LOCALITY=region%3Dus-west');
```
Here nodes with locality `region=us-west` write to the west bucket and all others to the default bucket. The locality query parameter must be URL-encoded (`=` becomes `%3D`). Find a node's locality with `SHOW LOCALITY;`.

Restore: list all URIs, with the default URI first:
```sql
RESTORE FROM LATEST IN ('s3://us-east-bucket', 's3://us-west-bucket');
```
If you moved the backup, the first URI must be the new location of the files originally written to the default. To restore a specific backup use `RESTORE FROM {subdirectory} IN (...)`.

Incrementals follow the same form: `BACKUP INTO LATEST IN (<uris>)` appends to the `incrementals` directory of the latest full backup, or `BACKUP INTO {subdirectory} IN (<uris>)`.

Gotchas:
- Backups try to match data to the right bucket but can be forced to write to the default bucket in edge cases such as unhealthy nodes; the page says to use an option at backup creation to make the backup fail in these cases (its name is not shown in the readable copy, so look it up on the page).

Verify: `SHOW BACKUPS IN '<default collection URI>';` lists the backup, and `SHOW BACKUP FROM LATEST IN (<uris>)` works against the URI list.

## Checked
2026-11-03. Confirmed on the locality-aware backups page: `COCKROACH_LOCALITY=default` and URL-encoded `region%3Dus-west` URIs, default bucket fallback for edge cases such as unhealthy nodes, restore listing all URIs with the default URI first, `SHOW BACKUPS IN` and `SHOW BACKUP FROM LATEST IN (...)`, and `SHOW LOCALITY`. Removed: the STRICT option name, the credentials note and the architecture pointer.
Method: documentation only; no commands were run.
