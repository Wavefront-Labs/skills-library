---
id: computing-software.digital-forensics-incident-response.incident-response-process.restoring-from-known-good-backups
name: restoring-from-known-good-backups
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [restore-from-backup, backup-integrity, incident-recovery, ransomware, backup-recovery, dfir]
level: practitioner
status: draft
description: "Restore systems from known-good backups after an incident: choosing the restore point, scanning backups for attacker artefacts, isolated restore and integrity checks."
sources: ["https://www.cisa.gov/stopransomware/ransomware-guide", "https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.nist.gov/publications/data-integrity-recovering-ransomware-and-other-destructive-events"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Restoring from known-good backups

**Goal:** bring data and systems back from a backup that predates the compromise or has
been proven free of attacker artefacts, without reintroducing the intruder.

## Pick the restore point
- Use the master timeline: earliest attacker activity (T0) on that system. A backup taken
  after T0 may contain backdoors, web shells, attacker accounts or scheduled tasks.
- For data: newer is better; for system state/binaries: before T0 or rebuild instead.
- Ransomware often deletes or encrypts backups; confirm the catalogue and repository are
  intact and the backup server itself was not compromised.

## Validate before restore
1. Mount backup in an **isolated** network (clean room) with no route to production.
2. Scan with current AV/YARA rules built from the incident IOCs; check for the incident's
   persistence (services, tasks, Run keys, web shells, new accounts).
3. Hash-compare critical binaries against vendor/gold images.
4. For databases: integrity checks (`DBCC CHECKDB`, `pg_amcheck`) and application-level
   reconciliation with the business.

## Restore
- Rebuild OS from gold image, restore data only where possible.
- Restore in dependency order: identity, DNS, core infrastructure, then line-of-business apps.
- Reset credentials embedded in restored configs.
- Bring online behind enhanced monitoring.

## Gotchas
- Immutable/air-gapped backups are only useful if restore was tested; restore speed (TB/hour)
  often dictates recovery time, not backup existence.
- Backup admin credentials in the compromised AD: the attacker had them.
- Restoring an encrypted VM snapshot taken mid-encryption.

## Verify
Business owner signs off functional checks; sweeps on restored systems are clean; data
reconciliation against transaction logs or external records completed.
