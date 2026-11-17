---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.data-integrity-failure-modes
name: data-integrity-failure-modes
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [data-integrity-failure-modes, data-loss-scenarios, data-integrity, risk-assessment, backup-strategy]
level: advanced
status: docs-checked
description: "Enumerate data-loss scenarios with the SRE Book's 24 combinations (root cause x scope x rate) and check each has a defence: soft delete, backups, replication or validation."
sources: ["https://sre.google/sre-book/data-integrity/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The 24 combinations of data-loss failure modes

SRE Book "Data Integrity": data loss can be classified along three axes, giving **24 distinct types of
failure** from combinations of:
- **Root cause** (6): user action, operator error, application bug, infrastructure defect, faulty hardware,
  site disaster.
- **Scope** (2): wide (many entities) vs narrow/directed (specific users or records).
- **Rate** (2): big bang (sudden) vs slow and steady (creeping over weeks).

6 x 2 x 2 = 24. Each needs a defence; no single mechanism covers all.

## Matrix (fill per dataset)
| Root cause | Scope | Rate | Example | Primary defence | Detection |
|---|---|---|---|---|---|
| User action | narrow | big bang | user deletes their folder | soft delete / trash | user notices |
| Operator error | wide | big bang | `DROP TABLE` in prod | backups + PITR, guarded admin tools | alerts on row count drop |
| Application bug | wide | slow | bug corrupts a fraction of writes for weeks | long-retention backups + out-of-band validation | validation pipeline |
| Application bug | narrow | big bang | migration breaks one tenant | per-tenant restore | probes / tenant reports |
| Infrastructure defect | wide | big bang | storage system bug | replication to different system, backups | integrity checks |
| Faulty hardware | narrow | slow | silent disk bit rot | checksums, scrubbing, replication | scrubbing errors |
| Site disaster | wide | big bang | region loss | cross-region replicas + offsite backups | obvious |

## Key insight from the book
**Low-grade corruption or deletion from software bugs** is the hardest case: the book's study of 19 Google
data recovery efforts found data deletion or loss of referential integrity from software bugs the most common
user-visible loss, and the most challenging variants were discovered weeks to months after the bug shipped.
Replication copies the damage, so defences are backups that reach back far enough and early detection with
out-of-band validation (see `out-of-band-data-validation`).

## Using it
1. For each critical dataset, fill the matrix (24 rows or a condensed version).
2. Mark rows with no defence or no detection: these are your risks.
3. Prioritise by likelihood x impact; add mechanisms (see `soft-and-lazy-deletion-implementation`,
   `backup-tiers-and-replication-vs-backup`).

## Gotchas
- Replication is not a backup: datastores that sync replicas push a corrupt row or errant delete to all copies.
- Restoring a whole dataset to fix narrow damage is slow and loses good writes; build per-entity restore.

## Verify
- [ ] Matrix completed for top datasets with an owner per gap.
- [ ] Retention of backups exceeds the expected detection time for slow corruption.

## Checked
2026-11-01. Confirmed against the SRE Book "Data Integrity" chapter: 24 failure types from root cause (user action,
operator error, application bugs, infrastructure defects, faulty hardware, site catastrophes), scope (wide or
narrow) and rate (big bang or creeping); the 19-recovery study; replication versus backup. Removed: the
"30 days" trash figure and the "0.1%" example, and the claim that recent backups are always corrupt too.
The matrix rows are illustrative examples, not book content.
Method: documentation only; no commands were run.
