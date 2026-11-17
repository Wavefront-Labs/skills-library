---
id: computing-software.database-administration.oracle-database.rman-backup-validation
name: rman-backup-validation
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, rman, rman-validate, restore-validate, block-corruption, backup-verification, v-database-block-corruption]
level: practitioner
status: docs-checked
description: "Prove Oracle backups are restorable with RMAN VALIDATE and RESTORE ... VALIDATE, and find corrupt blocks in datafiles before you need a restore."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/validating-database-files-backups.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/rcmrf/VALIDATE.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RMAN backup validation

## Two different checks
| Command | Reads | Proves |
|---|---|---|
| `VALIDATE DATABASE` / `BACKUP VALIDATE DATABASE` | live datafiles | no physical (and optionally logical) corruption **now** |
| `RESTORE DATABASE VALIDATE` | backup pieces that a restore would use | those backups exist, are readable and not corrupt |
None of them writes datafiles.

## Validate the live database
```
RMAN> VALIDATE CHECK LOGICAL DATABASE;
```
Results go to `V$DATABASE_BLOCK_CORRUPTION`:
```sql
SELECT file#, block#, blocks, corruption_type FROM v$database_block_corruption;
```
Fix listed blocks with block media recovery: `RMAN> RECOVER CORRUPTION LIST;`

## Validate the backups
```
RMAN> RESTORE DATABASE VALIDATE;                 -- most recent usable backup set
RMAN> RESTORE DATABASE VALIDATE CHECK LOGICAL;
RMAN> RESTORE ARCHIVELOG ALL VALIDATE;
RMAN> RESTORE CONTROLFILE VALIDATE;
RMAN> RESTORE DATABASE UNTIL TIME "TO_DATE('2026-10-17 22:00','YYYY-MM-DD HH24:MI')" VALIDATE;
RMAN> VALIDATE BACKUPSET 1234;
```
Output ends with `Finished restore at ...` and no `ORA-19505` errors. For tape/SBT
this exercises the media manager path too.

## Schedule
- Weekly `RESTORE DATABASE VALIDATE` + `RESTORE ARCHIVELOG ... VALIDATE` for the retention window.
- Monthly or quarterly: an actual restore to a scratch host (or `DUPLICATE`) and open it; only
  that proves the full procedure, keys (TDE wallet), and timing.
- `CROSSCHECK BACKUP;` before validation to mark missing pieces `EXPIRED`.

## Gotchas
- Validation reads every block: heavy I/O on backup storage; run off-peak and with channels
  matching what storage handles.
- TDE/encrypted backups need the wallet open for VALIDATE to read them.
- `BACKUP VALIDATE` checks datafiles, not existing backups (a common confusion).

## Verify
Scheduled job output contains no errors, `v$database_block_corruption` is empty, and the
restore-test log shows the database opened with expected row counts.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: VALIDATE, BACKUP ... VALIDATE and RESTORE ... VALIDATE, CHECK LOGICAL, V$DATABASE_BLOCK_CORRUPTION, RECOVER CORRUPTION LIST, VALIDATE BACKUPSET, RESTORE DATABASE VALIDATE and RESTORE ARCHIVELOG ALL VALIDATE (Backup and Recovery User Guide, validating files and backups).

Removed or corrected: RESTORE PREVIEW section, BLOCK range and tablespace SECTION SIZE validate examples, RESTORE SPFILE VALIDATE, ORA-19870 and the time-based archivelog validate form (not found in the cited pages).

Method: documentation only; no commands were run.
