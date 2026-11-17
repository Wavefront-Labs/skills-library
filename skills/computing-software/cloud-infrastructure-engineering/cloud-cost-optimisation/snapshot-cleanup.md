---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.snapshot-cleanup
name: snapshot-cleanup
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, workload-optimisation, snapshot-cleanup, orphaned-snapshots, backup-retention, ebs-snapshots, data-lifecycle-manager]
level: practitioner
status: docs-checked
description: "Clean up snapshots and backups past their purpose: find orphaned and aged snapshots, enforce lifecycle policies, archive tiers, and avoid deleting what retention requires."
sources: ["https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-lifecycle.html", "https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-archive.html", "https://learn.microsoft.com/azure/virtual-machines/snapshot-copy-managed-disk", "https://cloud.google.com/compute/docs/disks/scheduled-snapshots", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-deleting-snapshot.html", "https://docs.aws.amazon.com/ebs/latest/userguide/recycle-bin.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot and backup cleanup

## Find waste
- Snapshots whose source volume no longer exists (orphaned).
- Snapshots older than policy (e.g. > 90 days) not tied to a retention requirement.
- AMIs deregistered but backing snapshots kept; AMIs no longer used by any launch template.
- Manual database snapshots kept forever; backup copies beyond policy.
Example (AWS CLI): list your snapshots with start time and volume ID, then compare against
`aws ec2 describe-volumes` to find orphans.

## Fix
1. **Classify** with owners: required for retention/legal hold? If unknown, tag and quarantine
   (notify, wait 30 days) before deletion.
2. **Automate lifecycle**: Amazon Data Lifecycle Manager (only manages snapshots and AMIs it
   created); GCP snapshot schedules with retention.
3. **Archive tier** for long-term required snapshots: EBS Snapshots Archive is aimed at snapshots
   kept 90 days or longer and rarely accessed; archiving converts the incremental snapshot to a
   full one.
4. **Deregister AMIs** then delete their snapshots (a root snapshot of a registered AMI can't be deleted).
5. Report snapshot spend per team monthly.

## Gotchas
- Incremental snapshots: deleting an old one may not save much (data referenced by later ones
  is kept and billed to them).
- Deleting snapshots under legal hold or needed for compliance - always check retention rules.
- Recycle Bin retention rules keep deleted snapshots and AMIs for the period set, and they are
  billed at the normal snapshot rate meanwhile.

## Verify
- [ ] No orphaned snapshots older than quarantine period; lifecycle policies on all volumes.

## Checked
2026-11-01. Confirmed in the EBS pages on Data Lifecycle Manager, Snapshots Archive (90 days or longer, converted to
full snapshot), deleting snapshots (referenced data kept, AMI deregistration first) and Recycle Bin (retention, normal
billing). Removed: AWS Backup, Azure Backup and backup-vault claims and the archive restore-delay claim (not stated in
the pages read).
Method: documentation only; no commands were run.
