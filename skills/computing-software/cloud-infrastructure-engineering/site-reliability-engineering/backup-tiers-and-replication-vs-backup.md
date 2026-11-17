---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.backup-tiers-and-replication-vs-backup
name: backup-tiers-and-replication-vs-backup
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [backup-tiers, replication-vs-backup, data-integrity, 3-2-1-backup, snapshots, pitr]
level: practitioner
status: docs-checked
description: "Design tiered backups (snapshots, PITR, offsite immutable copies) and explain why replication and redundancy do not replace backups, with a per-tier failure coverage table."
sources: ["https://sre.google/sre-book/data-integrity/", "https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup tiers and replication vs backup

SRE Book "Data Integrity", second layer (backups and related recovery methods): a broad range of scenarios
at reasonable cost demands a tiered backup strategy. The first tier is many frequent, quickly restored
backups closest to the live datastores; later tiers hold fewer backups, kept longer, on different storage
and further away. And: replication and redundancy are not recoverability.

## Why replication is not backup
The book's answer to "we have replication, which is better than a backup" is that replication helps with
locality and site-specific disaster, but datastores that automatically sync replicas push a corrupt row or
errant delete to all copies, likely before you can isolate the problem. Non-serving exports (for example to
a native file) cover user and application errors but not losses at a lower layer, and copies on the same
filesystem share that exposure. Diversity is key: protecting against failure at layer X requires storing
data on diverse components at that layer.

## Tiers (the book's tiering, with this skill's own mapping)
| Tier | Book description | Typical mechanism |
|---|---|---|
| 1 | many frequent, quickly restored backups near the live data; retained hours to single-digit days; minutes to restore | local snapshots |
| 2 | fewer backups retained single-digit to low double-digit days on site-local distributed filesystems; hours to restore; catches bugs detected too late for tier 1 | full/incremental copies |
| 3+ | nearline storage such as tape libraries and offsite media; protect against site-level issues; taken less often, retained longer | offsite / offline copies |

The book notes Google drew its line between 30 and 90 days of backups for many services, depending on
tolerance for data loss and investment in early detection. Point-in-time recovery is valuable where a
strategy supports it; use it together with a tiered strategy if you can.

## Implementation notes
- Keep later-tier copies on different credentials and in a different place from production, so a bad script
  with production credentials cannot delete them (this skill's advice, not the book's).
- AWS Backup Vault Lock in compliance mode: once the grace time (cooling-off period) expires, the vault and
  lock cannot be changed or deleted by any user or by AWS while it holds recovery points. Governance mode can
  be removed by users with sufficient IAM permissions. Recovery points with retention "Always" are kept forever.
- Retention of the deepest tier should cover the time to detect slow corruption (see
  `data-integrity-failure-modes`).
- Restore speed decreases down the tiers; check each tier's restore time against its use cases.
- Media isolation protects against media flaws; moving data to and from tiers is expensive.

## Gotchas
- Snapshots stored in the same site as the data share its blast radius.
- Backup jobs fail silently; monitor last-success timestamp per tier.

## Verify
- [ ] Table of tiers per dataset with restore time measured per tier.
- [ ] Deletion attempt on the most protected tier with admin credentials fails.

## Checked
2026-11-01. Confirmed against the SRE Book "Data Integrity" chapter (replication versus backup, diversity,
tier descriptions, 30-90 day line, point-in-time recovery) and the AWS Backup Vault Lock page (compliance
versus governance mode, grace time, "Always" retention). Removed: the per-tier frequency and retention
figures, the 3-2-1 rule, the crash-consistent snapshot advice and the key-management claim, none of which a
fetched page states.
Method: documentation only; no commands were run.
