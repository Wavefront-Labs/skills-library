---
id: computing-software.cloud-infrastructure-engineering.aws.ebs-volume-initialization-after-snapshot-restore
name: ebs-volume-initialization-after-snapshot-restore
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ebs, volume-initialization, fio-initialize, lazy-loading, provisioned-rate-initialization, fast-snapshot-restore]
level: advanced
status: docs-checked
description: "Avoid first-read latency on EBS volumes restored from snapshots: lazy loading explained, fio/dd initialization, provisioned initialization rate, and Fast Snapshot Restore."
sources: ["https://docs.aws.amazon.com/ebs/latest/userguide/initalize-volume.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-initialize-monitor.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-fast-snapshot-restore.html", "https://docs.aws.amazon.com/ebs/latest/userguide/volume-creation-credits.html", "https://docs.aws.amazon.com/ebs/latest/userguide/view-fsr-enabled-snapshots.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Initializing EBS volumes restored from snapshots

## 1. The problem
A volume created from a snapshot is usable immediately, but blocks are fetched from S3 on
first access (**lazy loading**). The first read of each block can be far slower than
normal, so a freshly restored database or a new instance from an AMI performs badly until
every block has been touched once. Brand-new empty volumes do not need initialization.

## 2. Options, fastest to cheapest
| Option | Effect | Cost |
|---|---|---|
| **Fast Snapshot Restore (FSR)** | volumes created from the snapshot in enabled AZs are fully initialized at creation | per snapshot per AZ per hour; credit bucket limits creations |
| **Provisioned rate for volume initialization** | specify a rate (100-300 MiB/s) at volume creation; EBS hydrates the snapshot data in a predictable time | per-GiB charge on the snapshot data size, billed when the volume becomes active |
| **Read every block yourself** (fio/dd) | after attach, read all blocks once | instance time only |
| Do nothing | lazy loading, slow first touches | none |

## 3. Reading every block (Linux)
```bash
lsblk                                   # find the device, e.g. /dev/nvme1n1
sudo fio --filename=/dev/nvme1n1 --rw=read --bs=1M --iodepth=32 --ioengine=libaio \
  --direct=1 --name=volume-initialize
# or, slower:
sudo dd if=/dev/nvme1n1 of=/dev/null bs=1M status=progress
```
AWS describes `fio` as considerably faster than `dd` because it reads multi-threaded; both only read the device. While Provisioned IOPS SSD volumes initialize, the I/O performance status check can show `warning`, which is expected. Throughput is bounded by the volume's
throughput (gp3 125 MiB/s default: raise throughput temporarily for faster init) and the
instance's EBS bandwidth. Windows: use `fio` for Windows or `dd` from a utility, reading
`\\.\PhysicalDriveN`.

## 4. Provisioned initialization rate
```bash
aws ec2 create-volume --snapshot-id snap-0abc --availability-zone eu-west-1a \
  --volume-type gp3 --volume-initialization-rate 300
aws ec2 describe-volume-status --volume-ids vol-0new \
  --query 'VolumeStatuses[].InitializationStatusDetails'   # InitializationType, Progress, EstimatedTimeToCompleteInSeconds
```
Completion time is the snapshot data size (not the volume size) divided by the rate, and nothing
runs on the instance. The rate can also be set in instance block device mappings and launch
templates. Limits: 5,000 MiB/s cumulative across concurrent creations per Region, and not on
Outposts, Local Zones or Wavelength Zones. If you also have FSR on the snapshot, the specified
rate is used instead of FSR. Information can take up to 5 minutes to update.

## 5. Fast Snapshot Restore
```bash
aws ec2 enable-fast-snapshot-restores --source-snapshot-ids snap-0abc \
  --availability-zones eu-west-1a eu-west-1b
aws ec2 describe-fast-snapshot-restores --filters Name=snapshot-id,Values=snap-0abc
```
States `enabling` to `optimizing` to `enabled` (optimizing takes 60 minutes per TiB and gives only
partial benefit). There is one credit bucket per snapshot per AZ and each initialized volume uses one
credit; the fill rate is MIN(10, 1024 / snapshot GiB) and the bucket size is MAX(1, MIN(10, 1024 / snapshot GiB)),
starting at zero. With no credit the volume is created without FSR. Limits: snapshots up to 16 TiB,
5 FSR snapshots per Region, full benefit up to 64,000 IOPS and 1,000 MiB/s, and no Outposts or
Local Zones. Best for golden AMI snapshots used by ASGs or DR
snapshots needing instant performance. Disable when not needed: it bills hourly.

## Gotchas
- Snapshots copied to another region or archived and restored also lazy-load.
- Database restores (self-managed on EC2) should initialize before cutting traffic over.
- RDS restores have their own lazy loading; RDS mitigations differ (warm the DB with reads).

## Verify
- [ ] fio run completes; subsequent read latency (`VolumeTotalReadTime / VolumeReadOps`) matches a normal volume.
- [ ] With provisioned rate, `describe-volume-status` shows initialization completed at the expected time.
- [ ] FSR enabled only on snapshots that need it; cost reviewed monthly.

## Checked

Checked 2026-10-27 against the Amazon EBS User Guide (Initialize volumes, Monitor volume initialization, Fast snapshot restore, Volume creation credits, FSR state pages) and the botocore EC2 model.
- `create-volume --volume-initialization-rate` (100 to 300 MiB/s), billing basis, the 5,000 MiB/s regional limit and the FSR interaction confirmed.
- The `dd` and `fio` commands match the documented ones; `describe-volume-status` returns progress in `InitializationStatusDetails`, not in `VolumeStatus.Details`, so the query was corrected.
- FSR states, 60 minutes per TiB optimizing, credit bucket formulas and the 5-snapshot and 16 TiB limits confirmed.
- Removed the "(2025)" launch date and the "safe on mounted filesystems" assertion, which no page states.

Method: documentation only; no commands were run.
