---
id: computing-software.it-support-helpdesk.desktop-support.backup-types-and-rotation-schemes
name: backup-types-and-rotation-schemes
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, backup, data-recovery, backup-rotation, 3-2-1-rule, gfs, full-incremental-differential, synthetic-full, immutable-backup, restore-testing, rpo-rto, comptia-a-plus]
level: practitioner
status: draft
description: "Choose and check backup schemes: full, incremental, differential and synthetic, 3-2-1-1-0, GFS rotation, RPO/RTO, immutability and restore testing."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://www.cisa.gov/stopransomware/ransomware-guide"
  - "https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# backup-types-and-rotation-schemes

Goal: understand what the organisation's backups actually protect, and
prove a restore works before anyone needs it.

## Types
| Type | Backs up | Restore needs | Archive bit |
|---|---|---|---|
| **Full** | everything | that one set | cleared |
| **Incremental** | changes since last backup of any type | last full + every incremental since | cleared |
| **Differential** | changes since last full | last full + latest differential | not cleared |
| **Synthetic full** | built on the backup server from full + incrementals | one set | n/a |
Incrementals: smallest/fastest backups, slowest restores. Differentials grow
daily until the next full. Modern tools use changed-block tracking and
forever-incremental + synthetic fulls.

## Rules
- **3-2-1**: 3 copies, 2 different media/storage types, 1 off-site. Modern
  **3-2-1-1-0**: +1 offline/immutable copy, 0 errors on restore tests.
- **Immutable / air-gapped** copies are the ransomware control — attackers
  delete reachable backups first (CISA guide).
- **RPO** (how much data loss is acceptable → backup frequency) and **RTO**
  (how long to restore → method and media) are set by the business, per
  system.

## Rotation: grandfather-father-son (GFS)
Daily (son) kept ~1–2 weeks, weekly (father) kept ~1–2 months, monthly
(grandfather) kept a year or more; yearly for compliance retention. Tape or
cloud tiers; label and track media, store off-site copies.

## Endpoint context
- User files on endpoints: OneDrive Known Folder Move is the "backup" in
  most managed estates — but sync is not backup (deletions/ransomware
  propagate), so M365 retention/backup matters.
- Servers/NAS: image + file-level backups; databases with application-aware
  backups.

## Restore testing (the part people skip)
- Schedule test restores (monthly file restore, quarterly full system/VM
  restore to an isolated network) and record time taken vs RTO.
- Verify backup job reports daily — "success with warnings" often means
  files were skipped (open files, path too long).
- Check that encryption keys/passwords for backups are stored somewhere
  that survives the disaster.

## Verify
For a sample system you can state: last successful backup time, retention,
off-site/immutable copy location, and the result + duration of the last
test restore.
