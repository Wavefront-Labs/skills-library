---
id: computing-software.qa-testing-engineering.test-case-design.backup-and-restore-verification
name: backup-and-restore-verification
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [backup-restore-testing, reliability-testing, recoverability-testing, restore-drill, point-in-time-recovery, rpo]
level: practitioner
status: docs-checked
description: "Verify backups by restoring them: scheduled restore drills, point-in-time recovery, integrity checks, timing against RTO and restoring single objects."
sources:
  - https://www.postgresql.org/docs/current/continuous-archiving.html
  - https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup and restore verification

**Goal:** prove backups are restorable, complete and fast enough. A backup never restored is a hope, not a backup.

## Drill procedure
1. Pick a backup (latest and a random older one).
2. Restore to an isolated environment (never over production).
   - PostgreSQL PITR: a base backup plus archived WAL, stopping at `recovery_target_time` (PostgreSQL continuous archiving docs).
   - Managed services: restore snapshot/point-in-time to a new instance (RDS `restore-db-instance-to-point-in-time`); AWS Backup restore testing plans automate this.
3. **Integrity checks**: row counts and checksums for key tables vs a recorded reference; application smoke test against the restored DB; your database's own consistency-check tool.
4. **Timing**: total restore time, including download and index rebuild, vs RTO.
5. **Granular restore**: one deleted record/file/mailbox; the most common real request.
6. Record and automate on a fixed schedule.

## Scope
Databases, object storage (versioning, cross-region copies), file shares, configuration and secrets (are they backed up?), infrastructure as code state, encryption keys (backups encrypted with a deleted key are useless).

## Gotchas
- Backups excluded new tables or volumes added after the backup job was configured.
- Restore works but app cannot connect: credentials and network config were not part of the procedure.

## Verify
Drill log with backup id, restore duration, integrity check results and sign-off, at the agreed frequency.

## Checked

2026-10-28 Confirmed against: PostgreSQL continuous archiving docs (base backup, WAL archiving, `recovery_target_time`); AWS Backup restore testing page (restore testing plans, restore jobs, validation); botocore rds model (RestoreDBInstanceToPointInTime exists). Removed or generalised: the `pg_restore --jobs` example, `pg_amcheck`/DBCC CHECKDB, the sample timestamp, and the monthly cadence (not sourced).

Method: documentation only; no commands were run.
