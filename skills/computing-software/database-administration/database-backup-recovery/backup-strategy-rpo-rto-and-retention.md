---
id: computing-software.database-administration.database-backup-recovery.backup-strategy-rpo-rto-and-retention
name: backup-strategy-rpo-rto-and-retention
category: computing-software
field: database-administration
product: database-backup-recovery
tags: [database-administration, backup-strategy, rpo, rto, retention-policy, 3-2-1-rule, full-incremental-differential, cost-of-downtime, grandfather-father-son, immutable-backup, ransomware]
level: advanced
status: draft
description: "Derive backup frequency, retention tiers, and storage topology from actual RPO/RTO requirements instead of a generic nightly-full default."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backup strategy: start from RPO/RTO, not from "nightly full backup"

**Goal:** stop defaulting to "full backup every night, keep 30 days" and instead
derive frequency, type, and retention from what the business actually needs to
survive, because the default is almost always wrong in one direction or the other.

## 1. RPO and RTO are two different numbers with different levers
- **RPO (Recovery Point Objective)**: how much data loss is acceptable, measured
  in time. An RPO of 5 minutes means backups/log shipping must capture state at
  least every 5 minutes (continuous WAL/binlog/transaction-log archiving, not
  just the full backup cadence).
- **RTO (Recovery Time Objective)**: how long recovery is allowed to take. A
  500GB database with a logical dump/restore (mysqldump, pg_dump) might take 6
  hours to restore — if RTO is 30 minutes, the backup *type* itself is wrong
  (needs physical/snapshot-based restore, or a warm standby), regardless of how
  often backups run.
Get both numbers from whoever owns the business risk, in writing, before
designing anything — "as fast as possible" and "no data loss ever" are not RPO/RTO,
they're the absence of a decision, and they get "decided" during the actual
incident instead, under worse conditions.

## 2. Backup type follows from RPO, frequency follows from change volume
- **Full**: complete copy. Simplest restore (one step) but most storage/time to
  create.
- **Incremental**: only changes since the last backup (of any type). Fast to
  create, but restore requires replaying the full chain in order — a single
  corrupted link breaks every backup after it.
- **Differential**: changes since the last *full* (not the last backup).
  Restore needs only the full plus the one differential — simpler recovery chain
  than incremental, at the cost of each differential growing until the next full.
A near-zero RPO on a write-heavy system needs continuous log shipping (WAL/binlog/
redo) between full/incremental backups, not just more frequent fulls.

## 3. Retention: grandfather-father-son (GFS) or equivalent tiering
Keep daily backups for a short window (e.g. 7–14 days), weekly for a medium window
(4–8 weeks), monthly for a long window (12+ months) — gives cheap protection
against both "noticed yesterday" and "noticed three months later" without storing
every daily backup forever. Decide retention against two separate drivers that
often conflict: operational recovery needs (usually short) and compliance/legal
retention requirements (often long, sometimes requiring *immutability*, not just
retention).

## 4. The 3-2-1 rule, and why ransomware broke the simple version
3 copies, 2 different media/storage types, 1 offsite. Modern threat model adds a
4th consideration: at least one copy must be **immutable or air-gapped** —
ransomware and compromised-credential attacks increasingly target backup systems
directly (deleting or encrypting backups before/along with production data).
Object-storage immutability (WORM/retention-lock features) or offline/air-gapped
media defeats an attacker who has admin access to the backup console itself — a
backup an attacker with your credentials can delete is not a real backup for that
threat model.

## 5. Cost of downtime justifies the spend, in both directions
Calculate expected cost of an outage (revenue/hour, SLA penalties, reputational)
against the cost of tighter RPO/RTO (more infrastructure, standby replicas,
tooling). This cuts both ways: a low-value internal reporting database doesn't
need synchronous multi-region replication, and an unjustified 2am full-backup
window that saturates shared storage I/O for a system nobody will restore from
within a year is waste, not safety.

## Verify
- [ ] RPO and RTO are written down, numeric, and signed off by a business owner — not inferred from infrastructure defaults.
- [ ] Backup type/frequency was chosen to meet the RPO, and restore procedure was timed against the RTO.
- [ ] Retention tiers (GFS or equivalent) match actual operational and compliance needs separately.
- [ ] At least one backup copy is immutable or air-gapped against an attacker with production/backup-console credentials.
- [ ] The spend on backup infrastructure was sized against the real cost of the downtime it prevents.
