---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.disaster-recovery-planning
name: disaster-recovery-planning
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, disaster-recovery, dr, dr-plan, business-continuity, bcp, rto, rpo, backup, restore-testing, immutable-backups, air-gapped-backup, aws-backup, vault-lock, azure-backup, azure-site-recovery, backup-and-dr, cross-account-backup, ransomware, point-in-time-recovery, pitr, dr-runbook, game-day, dr-drill, elastic-disaster-recovery, 3-2-1-backup]
level: advanced
status: draft
description: "Write and test a cloud DR plan: scenario list incl. ransomware and account compromise, RTO/RPO per tier, immutable cross-account backups, restore runbooks and scheduled DR drills."
sources: ["AWS whitepaper - Disaster Recovery of Workloads on AWS", "NIST SP 800-34 Rev.1 Contingency Planning Guide", "Azure Architecture Center - Backup and disaster recovery", "Google Cloud - Disaster recovery planning guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Disaster recovery planning — the plan is the restore you've rehearsed

**Goal:** for every critical workload, a written, rehearsed procedure that restores service
within its RTO and loses no more than its RPO — including when the disaster is a person
with your admin credentials, not a flooded region.

Distinct from HA: HA handles expected failures automatically (see
`computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-region-high-availability-design`);
DR handles the events HA cannot — corruption, deletion, compromise, region-wide or provider-wide loss.

## 1. List the scenarios
| Scenario | Does replication help? | What saves you |
|---|---|---|
| AZ loss | yes | multi-AZ |
| Region loss | yes | cross-region replica / standby |
| Bad migration / data corruption | **no — replicated instantly** | point-in-time recovery, versioned backups |
| Accidental deletion (human or IaC `destroy`) | no | deletion protection, backups, object versioning |
| Ransomware / account compromise | no — attacker deletes backups too | **immutable, cross-account** backups |
| Provider-wide or SaaS dependency outage | partly | exportable data, documented manual workaround |

Most DR budgets go to region loss; most real DR events are the corruption and deletion rows.

## 2. Set RTO and RPO per tier and check they're achievable
- RPO is bounded by backup/replication frequency: nightly snapshots = up to 24 h loss.
  Managed DB PITR (RDS, Azure SQL, Cloud SQL) typically gives ~5-minute RPO within the retention window.
- RTO includes detection + decision + restore + validation + DNS. Restoring a 5 TB database
  from snapshot can take hours (lazy-loading volumes are slow until warmed). **Measure it.**

## 3. Backups that survive the attacker
- **Separate account/subscription/project** for backups, with its own break-glass identity, not federated from the same IdP admin group.
- **Immutability:** AWS Backup Vault Lock (compliance mode), S3 Object Lock, Azure Backup
  immutable vaults + soft delete, GCP Backup and DR backup vault with enforced retention / bucket retention locks.
- 3-2-1 adapted: 3 copies, 2 storage types or services, 1 in a different account and region.
- Back up what IaC can't recreate: databases, object stores, secrets/KMS key material policy
  (deleting a KMS key makes every backup it encrypts unrecoverable — use scheduled deletion windows and alarms), DNS zones, IdP config.
- Infrastructure itself: the IaC repo and state backend are DR dependencies — mirror the repo, version and replicate state.

## 4. Runbooks
Per workload: trigger criteria, who declares DR (named role, not person), communication
template, ordered restore steps with commands, validation checks, and fail-back steps.
Keep a copy **outside** the environment it describes (if the wiki is in the dead region, the runbook is gone).

## 5. Drill
- Quarterly: restore a tier-0 database from backup into an isolated account; time it; validate checksums/row counts and app smoke tests.
- Yearly: full regional failover or tabletop for ransomware with legal/comms present.
- Record actual RTO/RPO achieved; if it misses target, the target or the design changes — not the report.

## Gotchas
- Backups never restored are hope, not backups; restore permissions and KMS grants are the usual failure.
- Snapshots in the same account as production share its blast radius.
- Retention shorter than detection time: corruption found after 14 days with 7-day PITR is unrecoverable.
- Cross-region copy of encrypted snapshots needs a key in the destination region.
- DR environments drift from prod unless built from the same IaC and tested.

## Verify
- [ ] Scenario table exists with a mitigation per row, including ransomware and accidental deletion.
- [ ] Tier-0/1 backups are immutable and in a separate account with separate credentials.
- [ ] Last restore drill date, measured RTO and RPO are recorded per tier-0 workload.
- [ ] Runbooks are stored outside the environment they recover.
- [ ] Retention exceeds the time it typically takes to detect corruption.

Uncertain: restore durations and PITR granularity vary by engine and size — measure rather than trust these ranges.
Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.cost-vs-resilience-tradeoffs, computing-software.cloud-infrastructure-engineering.site-reliability-engineering.incident-response-and-blameless-postmortems
