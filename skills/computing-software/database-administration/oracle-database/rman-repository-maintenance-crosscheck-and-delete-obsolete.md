---
id: computing-software.database-administration.oracle-database.rman-repository-maintenance-crosscheck-and-delete-obsolete
name: rman-repository-maintenance-crosscheck-and-delete-obsolete
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rman, delete-obsolete, report-need-backup, crosscheck, retention-policy, archivelog-deletion-policy, expired-backups]
level: practitioner
status: docs-checked
description: "Keep the RMAN repository honest: retention and archivelog deletion policies, CROSSCHECK, DELETE EXPIRED/OBSOLETE, and REPORT NEED BACKUP / UNRECOVERABLE checks."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/maintaining-rman-backups.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/reporting-on-rman-operations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RMAN repository maintenance

## Policies first
```
RMAN> SHOW ALL;
RMAN> CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 14 DAYS;   -- or REDUNDANCY n
RMAN> CONFIGURE ARCHIVELOG DELETION POLICY TO BACKED UP 2 TIMES TO DISK;
```
Recovery window = keep whatever is needed to recover to any point in the last 14 days (so the
level 0 before the window start is kept). The FRA uses the policies to auto-delete reclaimable files under space pressure.

## Crosscheck: repository vs reality
Someone deleted files with `rm`, or tape expired them: the repository still lists them.
```
RMAN> CROSSCHECK BACKUP;
RMAN> CROSSCHECK COPY;
RMAN> CROSSCHECK ARCHIVELOG ALL;
RMAN> LIST EXPIRED BACKUP;          -- marked EXPIRED: not found
RMAN> DELETE NOPROMPT EXPIRED BACKUP;
RMAN> DELETE NOPROMPT EXPIRED ARCHIVELOG ALL;
```
EXPIRED pieces that you find again can be re-cataloged (`CATALOG START WITH '/backup/'`) and crosschecked back to AVAILABLE.

## Obsolete: no longer needed by policy
```
RMAN> REPORT OBSOLETE;
RMAN> DELETE NOPROMPT OBSOLETE;
```
Backups with `KEEP UNTIL` / `KEEP FOREVER` (archival backups) are never obsolete.

## The weekly maintenance job
```
RUN {
  CROSSCHECK BACKUP; CROSSCHECK ARCHIVELOG ALL;
  DELETE NOPROMPT EXPIRED BACKUP; DELETE NOPROMPT EXPIRED ARCHIVELOG ALL;
  DELETE NOPROMPT OBSOLETE;
}
```
Run it after the backup, log the output. With a recovery
catalog, also `RESYNC CATALOG` and run `DELETE OBSOLETE` from each target connection.

## Gotchas
- Never remove backups or archive logs with OS commands; use RMAN so the repository stays correct.
- `DELETE OBSOLETE` without a recovery catalog relies on control file records within `control_file_record_keep_time`.
- Deleting archive logs not yet applied/shipped to a standby breaks Data Guard: the deletion policy protects you only if configured.

## Verify
`LIST EXPIRED BACKUP` is empty, and FRA usage (`v$recovery_area_usage`) is stable week to week.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: CROSSCHECK, REPORT/DELETE OBSOLETE, retention policy RECOVERY WINDOW, CONFIGURE ARCHIVELOG DELETION POLICY ... BACKED UP n TIMES, KEEP FOREVER (needs a recovery catalog), CONTROL_FILE_RECORD_KEEP_TIME (Backup and Recovery User Guide, managing the repository).

Removed or corrected: REPORT NEED BACKUP / UNRECOVERABLE / SCHEMA section, APPLIED ON ALL STANDBY deletion policy, per-device DELETE OBSOLETE override (not found in the cited pages).

Method: documentation only; no commands were run.
