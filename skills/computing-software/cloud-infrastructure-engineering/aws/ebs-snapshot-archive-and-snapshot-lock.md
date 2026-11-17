---
id: computing-software.cloud-infrastructure-engineering.aws.ebs-snapshot-archive-and-snapshot-lock
name: ebs-snapshot-archive-and-snapshot-lock
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ebs, ebs-snapshots, snapshot-archive, snapshot-lock, compliance-mode, governance-mode, retention]
level: practitioner
status: docs-checked
description: "Cut long-term EBS snapshot cost with the archive tier (full snapshots, 90-day minimum, restore times) and make snapshots immutable with snapshot lock."
sources: ["https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-archive.html", "https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-archive-considerations.html", "https://docs.aws.amazon.com/ebs/latest/userguide/restore-archived-snapshot.html", "https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-archive-pricing.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-snapshot-lock.html", "https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-lock-concepts.html", "https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-lock-considerations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EBS snapshot archive and snapshot lock

## 1. Archive tier
For snapshots kept ≥ 90 days and rarely restored (monthly/annual compliance copies).
```bash
aws ec2 modify-snapshot-tier --snapshot-id snap-0abc --storage-tier archive
aws ec2 describe-snapshot-tier-status --filters Name=snapshot-id,Values=snap-0abc
# restore: temporary (N days) or permanent
aws ec2 restore-snapshot-tier --snapshot-id snap-0abc --temporary-restore-days 5
aws ec2 restore-snapshot-tier --snapshot-id snap-0abc --permanent-restore
```
- Archiving converts the snapshot into a **full** snapshot (all blocks, not incremental) —
  archiving daily incremental snapshots of one volume can cost more than keeping them in the
  standard tier. AWS recommends archiving monthly, quarterly or yearly snapshots.
- Minimum 90 days in archive (deleting or permanently restoring earlier bills the remaining days); restore takes up to
  **72 hours** depending on snapshot size; restores are billed per GB restored (see the pricing page).
- AWS Backup can archive its snapshots. You can archive only completed snapshots you own, and a snapshot
  associated with AMIs only if all of those AMIs are disabled. An archive or restore cannot be cancelled once started.

## 2. Snapshot lock
Immutability for snapshots (ransomware, regulatory retention):
```bash
aws ec2 lock-snapshot --snapshot-id snap-0abc --lock-mode governance --lock-duration 30
aws ec2 lock-snapshot --snapshot-id snap-0abc --lock-mode compliance --cool-off-period 24 --lock-duration 365
aws ec2 describe-locked-snapshots --snapshot-ids snap-0abc
```
- **Governance**: users with `ec2:UnlockSnapshot` can unlock/shorten.
- **Compliance**: after the optional **cool-off period** (up to 72 h, during which it can still be
  unlocked — your safety net for mistakes), nobody can unlock it, change the mode or shorten it; only extending the duration is possible. The only
  way to delete it before expiry is to close the AWS account (a closed account is suspended for 90 days,
  then AWS deletes its snapshots even if locked).
- You can lock archived snapshots and archive locked snapshots. You can lock snapshots associated with an AMI, and deregister an AMI whose snapshots are locked. AWS recommends not locking AWS Backup snapshots (use AWS Backup Vault Lock).

## Gotchas
- Compliance lock on the wrong snapshot or duration = paying for it until expiry — always use a cool-off period.
- Archived snapshots can't be used to create volumes or AMIs until restored.
- Archiving automatically disables fast snapshot restore and snapshot sharing; re-enable them manually after restoring.

## Verify
- [ ] `describe-snapshot-tier-status` shows `archival-complete` for archived snapshots; cost per GB drops in Cost Explorer.
- [ ] Deleting a compliance-locked snapshot fails after cool-off.
- [ ] A restore drill from archive completed within the documented RTO (≤ 72 h).

## Checked

Checked 2026-10-27 against the EBS User Guide pages Archive Amazon EBS snapshots (considerations and limitations, restore, pricing and billing, monitoring) and Amazon EBS snapshot lock (concepts, considerations, IAM), plus the botocore ec2 model.
Confirmed: modify-snapshot-tier --storage-tier archive; restore-snapshot-tier with --temporary-restore-days or --permanent-restore; archived snapshots are full snapshots; 90-day minimum archive period billed for remaining days; restore up to 72 hours; archived snapshots cannot create volumes or be shared or copied until restored; fast snapshot restore is disabled on archive; tiering status archival-complete; lock-snapshot parameters (lock mode compliance or governance, cool-off period 1-72 hours, lock duration 1-36500 days); governance versus compliance behaviour; compliance lock can only be removed early by closing the account; locked snapshots can be archived and vice versa; ec2:LockSnapshot, ec2:UnlockSnapshot and ec2:DescribeLockedSnapshots actions. Removed the unconfirmed Data Lifecycle Manager archive claim and the shared and copied claim.

Method: documentation only; no commands were run.
