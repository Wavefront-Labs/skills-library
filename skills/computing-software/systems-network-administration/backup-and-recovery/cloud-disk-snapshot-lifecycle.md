---
id: computing-software.systems-network-administration.backup-and-recovery.cloud-disk-snapshot-lifecycle
name: cloud-disk-snapshot-lifecycle
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [ebs-snapshots, data-lifecycle-manager, cloud-snapshots, aws, azure-disk-snapshots, snapshot-retention]
level: practitioner
status: docs-checked
description: "Manage cloud disk snapshots: EBS incremental snapshots, Data Lifecycle Manager policies, multi-volume consistency, archive tier, Recycle Bin, and Azure/GCP equivalents."
sources:
  - https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-lifecycle.html
  - https://docs.aws.amazon.com/ebs/latest/userguide/ebs-snapshots.html
  - https://learn.microsoft.com/en-us/azure/virtual-machines/disks-incremental-snapshots
  - https://cloud.google.com/compute/docs/disks/scheduled-snapshots
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud disk snapshot lifecycle

**Goal:** automatic, consistent, cost-controlled disk snapshots that expire on schedule and survive accidental deletion.

## EBS basics
- Snapshots are incremental: see the EBS snapshots page for how deleting one affects the others.
- Crash-consistent by default. Multi-volume consistency: `aws ec2 create-snapshots --instance-specification InstanceId=i-0abc,ExcludeBootVolume=false`.
- App-consistent: use Data Lifecycle Manager pre/post scripts (`Scripts` in the create rule) or your own quiesce steps.

## Data Lifecycle Manager
```sh
aws dlm create-lifecycle-policy --execution-role-arn arn:aws:iam::111122223333:role/AWSDataLifecycleManagerDefaultRole \
  --description "daily-14" --state ENABLED --policy-details file://policy.json
```
policy.json essentials, inside `PolicyDetails`: `PolicyType` (`EBS_SNAPSHOT_MANAGEMENT`), `ResourceTypes` (one of `VOLUME` or `INSTANCE`), `TargetTags`, and a `Schedules` list (up to 4). Each schedule has a `CreateRule` (`CronExpression`, or `Interval` with `IntervalUnit` set to `HOURS`), a `RetainRule` (`Count`, or `Interval` with `IntervalUnit` of DAYS, WEEKS, MONTHS or YEARS), and optionally `CrossRegionCopyRules` (`Encrypted` is required), `FastRestoreRule`, `ShareRules`, `DeprecateRule` and `ArchiveRule`.

## Protection and cost
- **Recycle Bin** retention rules keep deleted snapshots for a period you set, for recovery from accidental or malicious deletion.
- **Snapshot archive**: a cheaper tier for rarely needed copies; check the EBS pricing and archive pages for minimum storage period and restore time.
- Clean up orphan snapshots from deleted volumes/AMIs (a common cost leak); deregistering an AMI does not delete its snapshots.
- Encrypted snapshots: cross-account/cross-region copy needs KMS key grants.
- For centralised policies across accounts, AWS Backup plans are the broader option.

## Azure and GCP
- Azure managed disk incremental snapshots (`az snapshot create --incremental true`).
- GCP snapshot schedules (resource policies) attached to disks: `gcloud compute resource-policies create snapshot-schedule`.

## Checked
2026-11-01. Confirmed: `CreateLifecyclePolicy` request shape (PolicyDetails, Schedules, CreateRule HOURS-only interval, RetainRule units, CrossRegionCopyRules, FastRestoreRule, ShareRules, DeprecateRule, ArchiveRule) from the botocore dlm model; CLI flags via check_commands. Removed: price and percentage figures, retention minimums, VSS document name, AWS-side storage claim, example retention numbers.
Method: documentation only; no commands were run.

## Verify
Monthly: create a volume from the newest snapshot, attach to a test instance, mount and check data; DLM policy shows no errors in CloudWatch.
