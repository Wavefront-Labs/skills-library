---
id: computing-software.cloud-infrastructure-engineering.aws.ebs-recycle-bin-retention-rules
name: ebs-recycle-bin-retention-rules
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ebs, recycle-bin, retention-rule, ebs-snapshots, ami, accidental-deletion, ransomware-protection]
level: practitioner
status: docs-checked
description: "Protect EBS snapshots and AMIs from accidental or malicious deletion with Recycle Bin retention rules: tag- and region-level rules, rule lock, recovery, IAM and cost."
sources: ["https://docs.aws.amazon.com/ebs/latest/userguide/recycle-bin.html", "https://docs.aws.amazon.com/ebs/latest/userguide/recycle-bin-concepts.html", "https://docs.aws.amazon.com/ebs/latest/userguide/recycle-bin-create-rule.html", "https://docs.aws.amazon.com/ebs/latest/userguide/recycle-bin-lock.html", "https://docs.aws.amazon.com/ebs/latest/userguide/recycle-bin-perms.html", "https://docs.aws.amazon.com/ebs/latest/userguide/recycle-bin-factors.html", "https://docs.aws.amazon.com/ebs/latest/userguide/recycle-bin-working-with-snaps.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EBS Recycle Bin retention rules

Deleted snapshots/AMIs matching a retention rule go to the Recycle Bin instead of being
destroyed, and can be recovered until the retention period ends.

## 1. Rules
```bash
# region-level: all snapshots in the region, 14 days
aws rbin create-rule --resource-type EBS_SNAPSHOT --retention-period RetentionPeriodValue=14,RetentionPeriodUnit=DAYS \
  --description "all snapshots 14d"
# tag-level: only snapshots tagged backup=prod, 30 days
aws rbin create-rule --resource-type EBS_SNAPSHOT --retention-period RetentionPeriodValue=30,RetentionPeriodUnit=DAYS \
  --resource-tags ResourceTagKey=backup,ResourceTagValue=prod
# AMIs
aws rbin create-rule --resource-type EC2_IMAGE --retention-period RetentionPeriodValue=7,RetentionPeriodUnit=DAYS
```
- Retention is 1-365 days for snapshots and AMIs (EBS volumes, resource type `EBS_VOLUME`, are limited to 1-7 days). If several rules match, the longest retention wins.
- Region-level rules can **exclude** resources with tags (`--exclude-resource-tags`) — e.g.
  exclude `temp=true` CI snapshots to avoid paying for them.

## 2. Lock the rule (ransomware resilience)
```bash
aws rbin lock-rule --identifier <RULE_ID> --lock-configuration 'UnlockDelay={UnlockDelayValue=7,UnlockDelayUnit=DAYS}'
```
A locked rule can't be deleted or modified; unlocking starts a delay (7–30 days) before changes
are possible — an attacker with admin rights can't silently disable it.

Only Region-level rules without exclusion tags can be locked (tag-level rules cannot), and the unlock delay cannot be changed after locking.

## 3. Recover
```bash
aws ec2 list-snapshots-in-recycle-bin --query 'Snapshots[].[SnapshotId,RecycleBinEnterTime,RecycleBinExitTime]'
aws ec2 restore-snapshot-from-recycle-bin --snapshot-id snap-0abc
aws ec2 list-images-in-recycle-bin
aws ec2 restore-image-from-recycle-bin --image-id ami-0abc
```
Restore an AMI's snapshots too if they were deleted (they're separate resources).

## 4. IAM
`rbin:*` actions for rule management; `ec2:ListSnapshotsInRecycleBin`,
`ec2:RestoreSnapshotFromRecycleBin` for recovery. Restrict rule management to a security
role; deny `rbin:DeleteRule`/`UnlockRule` via SCP for everyone else.

## Gotchas
- Snapshots in the Recycle Bin are billed at normal snapshot rates — exclude high-churn snapshots.
- AWS Backup-managed snapshots: deleted by Backup lifecycle also go to the bin if matched — size accordingly.
- Rules are per Region.
- If you have rules for both AMIs and their snapshots, make the snapshot retention the same or longer, otherwise the AMI becomes unrecoverable.
- Resources deleted by AWS Backup or Data Lifecycle Manager are retained too; tag them and use exclusion tags to keep them out.

## Verify
- [ ] Delete a test snapshot tagged per rule → it appears in `list-snapshots-in-recycle-bin`; restore works.
- [ ] Rule shows `LockState: locked`.
- [ ] Monthly snapshot cost reviewed after enabling region-level rules.

## Checked

Checked 2026-10-27 against the EBS User Guide pages on Recycle Bin (overview, concepts, create rule, lock rule, permissions, considerations, snapshots) and the botocore rbin model.
Confirmed: retention 1-365 days for snapshots and AMIs, 1-7 days for volumes; tag-level versus Region-level rules and exclusion tags; longest retention wins when several rules match; lock only for Region-level rules without exclusion tags, unlock delay 7-30 days fixed at lock time; rbin and ec2 IAM actions (rbin:CreateRule, LockRule, UnlockRule, DeleteRule; ec2:ListSnapshotsInRecycleBin, ec2:RestoreSnapshotFromRecycleBin); create-rule and list-snapshots-in-recycle-bin command forms; snapshots in the bin are billed at regular snapshot rates and there is no extra charge for Recycle Bin itself; rules function only in the Region where created; AWS Backup and Data Lifecycle Manager deletions are retained.

Method: documentation only; no commands were run.
