---
id: computing-software.database-administration.database-backup-recovery.legal-hold-and-deletion-in-backups
name: legal-hold-and-deletion-in-backups
category: computing-software
field: database-administration
product: database-backup-recovery
tags: [database-administration, database-backup-recovery, legal-hold, gdpr-backups, right-to-erasure, retention, backup-strategy]
level: practitioner
status: draft
description: "Reconcile backup retention with deletion duties (GDPR erasure, retention limits) and legal holds: suppression lists, crypto-shredding, retention locks and documented procedures."
sources:
  - https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/
  - https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html
  - https://learn.microsoft.com/en-us/azure/storage/blobs/immutable-legal-hold-overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deletion obligations and legal hold in backups

Two opposing duties: **delete** personal data when required (GDPR Art. 17, retention limits in policy), and **preserve** data under legal hold (litigation, regulatory investigation) even if it would normally expire.

## Erasure requests and backups
Regulators (e.g. the UK ICO guidance) accept that data in backups may not be immediately erasable, provided you:
1. Put the backup data "beyond use": it is not restored for live processing except for DR.
2. Keep a **suppression list** of erased subject IDs; after any restore, re-apply erasures before the data is used.
3. Delete it when the backup expires under the normal retention schedule.
4. Tell the individual what happens to backup copies.

Implement:
```sql
CREATE TABLE erasure_log (subject_id uuid PRIMARY KEY, erased_at timestamptz NOT NULL, request_ref text);
```
Stored outside the backup scope (or replicated separately) so it survives restoring an older backup; the restore runbook includes "replay erasure_log".

## Crypto-shredding
Encrypt each subject's (or tenant's) sensitive fields with a per-subject key held in a key store; erase by destroying the key. Backups then contain unreadable ciphertext for that subject. Works well for multi-tenant offboarding.

## Retention limits
Backup retention is part of the data retention policy: e.g. 35 days of daily, 12 monthly, 7 yearly. Longer retention needs a lawful basis; minimise PII in long-term archives (anonymise or exclude tables).

## Legal hold
- Suspends deletion for specific data or backup sets until released.
- Object storage: S3 Object Lock legal hold (`put-object-legal-hold --legal-hold Status=ON`), Azure immutable storage legal hold tags, GCS bucket/object holds. Unlike retention mode, legal hold has no expiry until removed.
- Backup software: mark backup sets as held (pgBackRest: archive copies outside expiry; Commvault/Veeam/RMAN `KEEP FOREVER` / `KEEP UNTIL`).
- Record who placed the hold, scope, matter reference and release date; review regularly.

## Conflict resolution
Legal hold overrides erasure for the held data; document the exception and resume erasure when the hold lifts.

## Verify
Audit: sample erased subject IDs, restore last month's backup in a sandbox, run the suppression replay, and confirm no erased subject remains; list all active holds with owners.
