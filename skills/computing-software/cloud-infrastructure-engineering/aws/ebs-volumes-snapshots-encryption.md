---
id: computing-software.cloud-infrastructure-engineering.aws.ebs-volumes-snapshots-encryption
name: ebs-volumes-snapshots-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ebs, gp3, gp2, io2, io2-block-express, st1, sc1, ebs-snapshot, ebs-snapshots, snapshot-lifecycle, data-lifecycle-manager, dlm, fast-snapshot-restore, ebs-encryption, encryption-by-default, kms, multi-attach, elastic-volumes, volume-resize, iops, throughput, ebs-optimized, nvme, xfs, growpart, instance-store]
level: practitioner
status: docs-checked
description: "Choose and tune EBS volumes (gp3 vs io2, IOPS/throughput, instance limits), resize online, run snapshots with Data Lifecycle Manager, and enforce KMS encryption by default."
sources: ["https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-snapshots.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-encryption.html", "https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-lifecycle.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-modify-volume.html", "https://docs.aws.amazon.com/ebs/latest/userguide/general-purpose.html", "https://docs.aws.amazon.com/ebs/latest/userguide/provisioned-iops.html", "https://docs.aws.amazon.com/ebs/latest/userguide/hdd-vols.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-fast-snapshot-restore.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# EBS volumes, snapshots and encryption

**Goal:** every volume is the cheapest type that meets its IOPS/throughput need, the
instance can actually deliver that performance, data is encrypted with a key you
control, and snapshots exist on a schedule with a tested restore.

## 1. Volume types (current generation)
| Type | Baseline | Max | Size | Use |
|---|---|---|---|---|
| **gp3** | 3,000 IOPS, 125 MiB/s included | 80,000 IOPS, 2,000 MiB/s (provision independently of size; 16,000 / 1,000 on Outposts) | 1 GiB-64 TiB | Default for everything |
| gp2 | 3 IOPS/GiB (min 100), volumes under 1 TiB burst to 3,000 | 16,000 IOPS at 5,334 GiB+; 250 MiB/s | 1 GiB-16 TiB | Legacy; migrate to gp3 |
| **io2 Block Express** | provisioned | 256,000 IOPS (on Nitro instances), 4,000 MiB/s, 1,000 IOPS/GiB | 4 GiB-64 TiB | Databases needing > 16k IOPS or 99.999% durability, Multi-Attach |
| st1 | 40 MiB/s per TiB baseline, burst 250 MiB/s per TiB | 500 MiB/s | 125 GiB-16 TiB | Sequential big data, logs |
| sc1 | 12 MiB/s per TiB baseline, burst 80 MiB/s per TiB | 250 MiB/s | 125 GiB-16 TiB | Cold, rarely read |
- gp3 IOPS : size ratio max 500 IOPS/GiB and throughput ≤ 0.25 MiB/s per provisioned IOPS
  (so 2,000 MiB/s needs ≥ 8,000 IOPS and a volume of 16 GiB or more).
- I/O size matters: the EBS volume-types page gives the I/O size at which each type reaches its maximum IOPS.
- Queue depth matters: a single-threaded `dd` will never show a volume's maximum IOPS; test with `fio` and a deep queue.

## 2. The instance is the other half of the limit
Each instance type has an EBS bandwidth/IOPS ceiling (some sizes only burst to it).
A fast volume on a small instance tops out at the instance's figure. Check
`aws ec2 describe-instance-types --instance-types m6i.large --query 'InstanceTypes[].EbsInfo'`.
io2 Block Express volumes reach their full IOPS only on Nitro-based instances; other instance
types reach up to 32,000 IOPS. Instance store is faster scratch space but its data is lost
when the instance stops.

## 3. Create, attach, grow online
```bash
aws ec2 create-volume --availability-zone eu-west-1a --volume-type gp3 --size 500 --iops 6000 --throughput 500 \
  --encrypted --kms-key-id alias/ebs-prod --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=db-data}]'
aws ec2 attach-volume --volume-id vol-0abc --instance-id i-0abc --device /dev/sdf
# on the instance
sudo mkfs.xfs /dev/nvme1n1 && sudo mount -o noatime /dev/nvme1n1 /data
# grow later (Elastic Volumes: size, type, IOPS, throughput — no detach)
aws ec2 modify-volume --volume-id vol-0abc --size 1000 --volume-type gp3 --iops 10000
aws ec2 describe-volumes-modifications --volume-ids vol-0abc   # wait for optimizing/completed
sudo growpart /dev/nvme0n1 1 && sudo xfs_growfs /   # root: partition first; data volume: just xfs_growfs /data (resize2fs for ext4)
```
- Volumes can only grow, never shrink (shrink = new volume + copy).
- Up to four modifications per volume in a rolling 24-hour period, and each must reach `completed`
  before the next; the volume is usable during `optimizing`
  but performance is a blend until `completed` (a 1 TiB volume can take up to six hours).
- Volumes are AZ-bound; moving AZ = snapshot → create in the target AZ (snapshot data is
  replicated across all AZs in the Region).
- Set `DeleteOnTermination` explicitly in launch templates to avoid orphaned volumes.
- **Multi-Attach** (io1/io2 only, enabled at creation or on an unattached volume, instances
  in the volume's AZ) needs a cluster-aware filesystem or application-level coordination;
  XFS/ext4 on two writers = corruption.

## 4. Encryption
```bash
aws ec2 enable-ebs-encryption-by-default --region eu-west-1
aws ec2 modify-ebs-default-kms-key-id --kms-key-id alias/ebs-prod
```
With encryption by default on, volumes and snapshot copies created from unencrypted
snapshots are always encrypted. Encrypting an existing volume: snapshot →
`copy-snapshot --encrypted --kms-key-id` → create volume → swap. When sharing encrypted
snapshots across accounts, plan the KMS key policy for the other account up front.

## 5. Snapshots
Incremental (only blocks changed since the previous snapshot are saved):
```bash
aws ec2 create-snapshot --volume-id vol-0abc --description "pre-upgrade" --tag-specifications 'ResourceType=snapshot,Tags=[{Key=app,Value=db}]'
aws ec2 create-snapshots --instance-specification InstanceId=i-0abc,ExcludeBootVolume=false   # snapshots all volumes of the instance
```
- Application consistency: quiesce the application and filesystem (`fsfreeze`, or the
  database's own flush/lock) before the snapshot call and release afterwards.
- A volume restored from a snapshot has first-access latency per block. Pre-warm by reading
  the whole device, or use **Fast Snapshot Restore**: volumes are fully initialised at
  creation and deliver all provisioned performance at once. It is enabled per snapshot per
  AZ, billed per minute enabled with a one-hour minimum, and unsupported on Outposts, Local
  Zones and Wavelength Zones. Volumes above 64,000 IOPS or 1,000 MiB/s should still be initialized.
- **Data Lifecycle Manager** policies enforce a regular snapshot schedule without a cron box:
  `aws dlm create-lifecycle-policy --execution-role-arn <ROLE_ARN> --policy-details file://dlm.json`.
  Use **AWS Backup** instead when you need one plan across EBS/RDS/EFS.
- Deleting a snapshot only removes data referenced by no other snapshot, so it may not reduce
  storage cost. The snapshot **Archive** tier has a 90-day minimum archive period and a
  restore can take up to 72 hours, depending on snapshot size.

## Gotchas
- gp2 burst credits exhausted on small volumes (a 100 GiB volume has a 300 IOPS baseline) is the
  classic "disk suddenly slow after an hour" — switch to gp3.
- A volume attached before November 3, 2016 23:40 UTC needs Elastic Volumes support initialized before it can be modified.
- Deleting a volume with no snapshot is unrecoverable; set `DeleteOnTermination` to false on data volumes.

## Verify
- [ ] `fio --rw=randread --bs=16k --iodepth=64 --numjobs=4 --direct=1 --runtime=60` hits ≥ 90% of provisioned IOPS on the attached instance.
- [ ] `get-ebs-encryption-by-default` returns true in every used region; `describe-volumes --filters Name=encrypted,Values=false` is empty.
- [ ] DLM/Backup policy produced a snapshot in the last 24 h; a restore to a new instance mounts and passes the app's integrity check.
- [ ] No volumes in `available` state (unattached, billed) older than 7 days.

## Checked
2026-10-31. Confirmed against the EBS User Guide pages for volume types, General Purpose SSD (gp3 3,000 IOPS / 125 MiB/s baseline, 80,000 IOPS, 2,000 MiB/s, 500 IOPS per GiB, 0.25 MiB/s per IOPS, Outposts limits; gp2 3 IOPS per GiB and 5,334 GiB for 16,000 IOPS), Provisioned IOPS (io2 Block Express 256,000 IOPS, 1,000:1, 4,000 MiB/s, 99.999% durability, Nitro requirement), HDD (st1 and sc1 baseline, burst and caps), modify volume (four modifications per rolling 24 hours, six hours for 1 TiB), snapshot archive (90 days, 72 hours), fast snapshot restore and encryption by default. Removed as unconfirmed: instance-store and device-name notes, the Multi-Attach instance count, the cross-account key action list and `aws/ebs` sharing claim, encryption performance claim, DLM default role and option list, Recycle Bin, the CloudWatch metric guidance and the st1 boot restriction. Prices were never kept.
Method: documentation only; no commands were run.
