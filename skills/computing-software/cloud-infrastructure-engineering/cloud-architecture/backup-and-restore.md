---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.backup-and-restore
name: backup-and-restore
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, disaster-recovery, backup-and-restore, backup-strategy, cross-region-backup, iac-rebuild, restore-automation, backup-policy, aws-backup, azure-backup, backup-and-dr-service]
level: practitioner
status: docs-checked
description: "Implement backup-and-restore DR: what to back up, frequency and retention per tier, cross-region and cross-account copies, IaC rebuild and automated restore."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html", "https://learn.microsoft.com/azure/backup/backup-overview", "https://cloud.google.com/backup-disaster-recovery/docs/concepts/backup-dr"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup and restore DR strategy

The lowest-footprint DR strategy: data is protected by backups (optionally copied to another region)
and infrastructure, configuration and code are redeployed at recovery time. AWS describes it as
suitable for data loss or corruption, a regional disaster (with cross-region copies) or lack of
redundancy in a single-AZ workload.

## Steps
1. **Inventory data and configuration** per workload: databases, object storage, file shares,
   block volumes, code and configuration, and machine images (AMIs).
2. **Policy per tier**: backup frequency determines the achievable recovery point and must meet
   the RPO; the backup must allow restore to the point in time it was taken. Use a central service:
   AWS Backup (centralised configure, schedule and monitor; copies across Regions and accounts;
   cross-account copies help against insider threats or account compromise); Azure Backup
   (vaults act as a security boundary; geo-redundant storage is the default and recommended
   replication, soft delete and immutable backup are available; Azure Site Recovery handles DR
   orchestration); Google Backup and DR (backup vaults give immutable, indelible backups, with
   cross-region and cross-project restore options).
3. **Infrastructure as code** for everything: AWS says to always deploy with IaC (for example
   CloudFormation or CDK), because without it restoring in the recovery Region is complex, which
   increases recovery time and may exceed the RTO. AMIs can be copied within or across Regions.
4. **Automate restore**: AWS Backup does not currently schedule or automatically restore, so use
   the SDK (for example SNS plus Lambda on backup completion) to restore to the DR Region. A
   periodic restore also guards against the restore control plane being unavailable in a disaster.
5. **S3 data**: cross-Region replication is near-zero RPO but does not protect against corruption
   or deletion as well as point-in-time backups; enable object versioning.
6. **Test restores**: AWS states a backup strategy must include testing backups. Measure the time of each step.

## Gotchas
- Backups exist but IaC hasn't been applied to a fresh region in years; expect drift and hardcoded region names.
- Continuous replication copies corruption too; keep point-in-time backups.

## Verify
- [ ] Full rebuild and restore in the recovery region completed in a drill; time recorded vs RTO.
- [ ] Backup copies exist in a separate account and region.

## Checked
2026-11-08. Confirmed: AWS Well-Architected DR whitepaper backup and restore section (IaC advice, AMIs, RPO and frequency, AWS Backup cross-Region and cross-account copy, no scheduled restore, SDK automation, S3 CRR and versioning, testing), AWS Backup overview (centralised management, cross-Region backup), Azure Backup overview (vault as security boundary, GRS default, soft delete, immutable backup, Site Recovery for DR), Google Backup and DR overview (immutable backup vaults, cross-region and cross-project restore). Removed: quarterly test cadence, minute-level PITR RPO, encryption key guidance, TB restore throughput, quota notes, "cheapest" claim.
Method: documentation only; no commands were run.
