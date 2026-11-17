---
id: computing-software.systems-network-administration.backup-and-recovery.automated-restore-verification
name: automated-restore-verification
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [automated-restore-verification, restore-testing, surebackup, scripted-restore, backup-validation, recovery-testing]
level: advanced
status: docs-checked
description: "Script automated restore verification: scheduled restores of canary files, PostgreSQL and SureBackup checks, results to monitoring, and alerting on failure."
sources:
  - https://helpcenter.veeam.com/docs/backup/vsphere/surebackup_job.html
  - https://restic.readthedocs.io/en/stable/050_restore.html
  - https://www.postgresql.org/docs/current/app-pgverifybackup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automated restore verification

**Goal:** every backup set is proven restorable on a schedule without someone remembering to do it.

## What to check (cheapest to strongest)
1. Backup job success (not a restore test).
2. File-level restore of known canary files with checksum compare.
3. PostgreSQL base backups: `pg_verifybackup` checks the backup against its `backup_manifest` (file checksums, required WAL). The PostgreSQL docs state it cannot include every check a running server performs, so still do test restores and confirm the databases work and hold the right data.
4. Full VM boot in isolation from backup (Veeam SureBackup, below).

## Example: restic canary
```sh
#!/bin/sh
set -eu
T=$(mktemp -d)
restic restore latest --target "$T" --include /srv/canary/canary.txt
echo "$(cat /srv/canary/canary.sha256)  $T/srv/canary/canary.txt" | sha256sum -c -
rm -rf "$T"
curl -fsS https://hc.example.net/ping/<uuid>   # dead-man switch
```
`restore latest` picks the latest snapshot; `--include` restricts the restore to a subset of files (it cannot be combined with `--exclude`). Use `restic ls latest` to find the exact path inside the snapshot. Write the canary file with a timestamp each day before backup; the restore check proves recency as well as integrity.

## Example: Veeam SureBackup
A SureBackup job runs in one of two modes: Full recoverability testing (starts machines from the application group, then the verified machines, in an isolated virtual lab directly from backup and tests live applications) or Backup verification and content scan only (integrity check and content analysis for malware or sensitive data; no virtual lab or application group needed). It can be run manually or scheduled. If its schedule overlaps the linked backup job, SureBackup waits for the backup job to finish; chain the jobs or set a timeout. A missing valid restore point for an application group machine fails the whole job; for a verified machine only that machine's verification fails. By default up to three machines are tested at once.

## Wire into monitoring
- Each test pushes success/failure and duration to your monitoring or a dead-man-switch check.
- Alert on failure and on **absence** of a result.
- Rotate which systems are tested so every system is covered within its test interval.

## Gotchas
- Testing only the newest point hides corruption in older chains; sample older points too.
- Sandboxes that can reach production (duplicate IPs, AD writes, emails sent) cause incidents; isolate.

## Verify
Dashboard shows last successful restore test per system within its interval; break a canary deliberately once to prove alerting fires.

## Checked

2026-11-09. Confirmed against the Veeam "SureBackup Job" page (two modes, application group/virtual lab behaviour, overlap handling, failure behaviour, three simultaneous machines by default), restic "Restoring from backup" (`restore latest`, `--target`, `--include`/`--exclude` mutually exclusive, `restic ls latest`) and PostgreSQL `pg_verifybackup` (manifest-based verification and the test-restore caveat). Removed: `restic check --read-data-subset`, Proxmox Backup Server verify jobs, Veeam health check, Nakivo, SQL Server `DBCC CHECKDB`/`WITH MOVE`/dbatools, SureBackup heartbeat/ping/script test details and masquerade network, Prometheus pushgateway/Zabbix names (not on cited pages).

Method: documentation only; no commands were run.
