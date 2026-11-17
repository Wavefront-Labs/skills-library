---
id: computing-software.database-administration.cockroachdb.restore-statement
name: restore-statement
category: computing-software
field: database-administration
product: cockroachdb
tags: [restore, restore-statement, schema-only, verify-backup-table-data, multi-region-restore]
level: practitioner
status: docs-checked
description: "Use RESTORE in CockroachDB: version limits, privileges, cluster/database/table restores, schema_only validation, DETACHED jobs and multi-region restore rules."
sources:
  - https://www.cockroachlabs.com/docs/stable/restore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restore data predictably and know the constraints before an incident.

Constraints:
- Cannot restore backups made by newer versions; a backup taken on one major version restores into a cluster on the same or the next major version (see the Restoring Backups Across Versions page).
- `RESTORE` is blocking; add `DETACHED` to run it as an asynchronous job. A restore that keeps hitting transient errors pauses instead of failing; then `RESUME` or `CANCEL` it. Failed or cancelled restores clean up partial data.
- No enterprise license required.
- Restore granularity is table; you cannot restore a subset of a table. Tables with `exclude_data_from_backup` restore without rows.

Privileges: members of `admin` can run every restore type; otherwise the current model uses the database-level `RESTORE` privilege, while the legacy model requires `admin` for a full cluster restore and write access (`CREATE` or `INSERT`) on affected objects for the rest. Managing the job (`PAUSE JOB`, `RESUME JOB`, `CANCEL JOB`) needs `admin` or `CONTROLJOB`; `VIEWJOB` allows viewing jobs.

Forms:
```sql
RESTORE FROM LATEST IN 'your_backup_collection_URI';
RESTORE DATABASE backup_database_name FROM LATEST IN 'your_backup_collection_URI';
RESTORE TABLE bank.customers FROM LATEST IN '{collectionURI}';
```
Full cluster restore drops `defaultdb` and `postgres` first. The owner of restored objects is the user running the restore; to restore users and grants, do a cluster restore into a fresh cluster with no user data. User-defined types must be compatible with an existing same-named type (enums need the same ordered values, created the same way); otherwise drop or rename the existing type.

Validation options: `RESTORE ... schema_only` checks the schema without user data; `verify_backup_table_data` additionally reads and checksums all data then discards it. `encryption_passphrase` decrypts encrypted backups.

Multi-region: region mismatches are flagged before restore; non-multi-region tables restore as `REGIONAL BY TABLE` in the destination primary region; restoring a partition of a `REGIONAL BY ROW` table is unsupported.

Check the job in `SHOW JOBS`.

## Checked

2026-11-03. Confirmed against the RESTORE page: version limits, blocking and `DETACHED`, pause on transient errors, cleanup, no enterprise license requirement, table-level granularity, `exclude_data_from_backup`, privileges, `defaultdb` and `postgres` drop, ownership, type compatibility, `schema_only`, `verify_backup_table_data`, multi-region rules. Removed: row-count verification and the re-grant and existing-objects claims.
Method: documentation only; no commands were run.
