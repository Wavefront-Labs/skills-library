---
id: computing-software.cloud-infrastructure-engineering.aws.ebs-gp2-to-gp3-migration-and-hdd-volume-selection
name: ebs-gp2-to-gp3-migration-and-hdd-volume-selection
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ebs, gp2-to-gp3, st1, sc1, elastic-volumes, cost-optimization, volume-types]
level: practitioner
status: docs-checked
description: "Migrate gp2 volumes to gp3 online with matched IOPS/throughput, find candidates fleet-wide, and pick st1 or sc1 HDD volumes for throughput-heavy or cold data."
sources: ["https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html", "https://docs.aws.amazon.com/ebs/latest/userguide/general-purpose.html", "https://docs.aws.amazon.com/ebs/latest/userguide/hdd-vols.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-modify-volume.html", "https://docs.aws.amazon.com/ebs/latest/userguide/monitoring-volume-modifications.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gp2 to gp3, and when to use st1/sc1

## 1. Why gp3
- The EBS User Guide lists gp3 at a 20 percent lower price per GiB than gp2.
- gp2 performance is tied to size: 3 IOPS/GB (min 100, max 16,000), burst to 3,000 for
  volumes under 1 TiB via credits; throughput up to 250 MiB/s.
- gp3 decouples: baseline **3,000 IOPS and 125 MiB/s** at any size (1 GiB to 64 TiB), and you can
  provision up to 80,000 IOPS (500 IOPS per GiB, so 160 GiB or larger for the maximum) and up to
  2,000 MiB/s (0.25 MiB/s per provisioned IOPS, so 8,000 IOPS or more for the maximum), paying
  only for extra. On Outposts the limits are 16 TiB, 16,000 IOPS and 1,000 MiB/s.

## 2. Match performance before converting
| gp2 size | gp2 baseline IOPS | gp3 setting |
|---|---|---|
| < 1,000 GiB | 100-2,999 (burst 3,000) | default 3,000 IOPS; gp2 delivers up to 250 MiB/s from 170 GiB upward, so provision `--throughput 250` if the workload uses it |
| 1,000-5,333 GiB | 3,000-16,000 | IOPS = 3 x size; throughput 250 MiB/s |
| >= 5,334 GiB | 16,000 | 16,000 IOPS, 250 MiB/s |
Check actual usage first (CloudWatch `VolumeReadOps`+`VolumeWriteOps` / period,
`VolumeReadBytes`+`VolumeWriteBytes`) and provision for the observed peak, not the gp2
theoretical number; extra IOPS above 3,000 cost money.

## 3. Convert online (Elastic Volumes)
```bash
aws ec2 modify-volume --volume-id vol-0abc --volume-type gp3
aws ec2 describe-volumes-modifications --volume-ids vol-0abc \
  --query 'VolumesModifications[].{state:ModificationState,progress:Progress}'
```
No downtime, no detach. If you omit `--iops` and `--throughput`, EBS provisions the higher of the
source gp2 volume's equivalent performance and the gp3 baseline (for example a 500 GiB gp2 volume
with 250 MiB/s becomes 3,000 IOPS and 250 MiB/s). Add `--iops` or `--throughput` only to override.
State goes `modifying` to `optimizing` (performance is between source and target) to `completed`;
the volume can be modified again once it is `completed`. A fully used 1 TiB volume can take about 6
hours, sometimes longer, and a request cannot be cancelled once submitted.

## 4. Fleet-wide
```bash
aws ec2 describe-volumes --filters Name=volume-type,Values=gp2 \
  --query 'Volumes[].{id:VolumeId,size:Size,attached:Attachments[0].InstanceId}' --output table
```
Loop over regions/accounts with a script or SSM Automation. Update launch templates, AMI block device
mappings, CloudFormation/Terraform defaults (`VolumeType: gp3`) and EBS CSI StorageClasses
(`type: gp3`) so new volumes are gp3.

## 5. st1 and sc1 (HDD)
| | st1 (throughput optimized) | sc1 (cold) |
|---|---|---|
| Size | 125 GiB - 16 TiB | 125 GiB - 16 TiB |
| Throughput | baseline 40 MiB/s per TiB, burst 250 MiB/s per TiB, max 500 MiB/s | baseline 12 MiB/s per TiB, burst 80 MiB/s per TiB, max 250 MiB/s |
| Use | big sequential reads/writes: log processing, Kafka, data warehouses on EC2 | infrequently accessed sequential data, lowest cost block storage |
| Not for | boot volumes, random small IO | same |
Both measure IO in 1 MiB units; small random IO performs terribly. Consider S3 for cold
data unless an application needs a block device.

## Gotchas
- A root volume cannot be modified to st1 or sc1, and a Multi-Attach volume can only switch between io1 and io2. Volume size can only increase.
- gp3 throughput above 125 MiB/s needs IOPS ratio: max 0.25 MiB/s per provisioned IOPS.
- Instance EBS bandwidth caps can bottleneck before the volume does.

## Verify
- [ ] `describe-volumes --filters Name=volume-type,Values=gp2` returns nothing in each region (or documented exceptions).
- [ ] Post-change latency/IOPS metrics equal or better than before at peak.
- [ ] IaC and StorageClass defaults specify gp3.

## Checked

Checked 2026-10-27 against the Amazon EBS User Guide (volume types, General Purpose SSD, HDD volumes, Modify a volume, Monitor modifications) and the botocore EC2 model.
- gp3 limits (3,000 IOPS and 125 MiB/s baseline, 80,000 IOPS, 2,000 MiB/s, 500 IOPS per GiB, 0.25 MiB/s per IOPS, 1 GiB to 64 TiB, Outposts limits) corrected from the stale 16,000 IOPS and 1,000 MiB/s.
- gp2 baseline (3 IOPS per GiB, 100 to 16,000, burst to 3,000 under 1 TiB), 128 to 250 MiB/s throughput, st1 (40 and 250 MiB/s per TiB, 500 max) and sc1 (12 and 80 MiB/s per TiB, 250 max), 125 GiB to 16 TiB, no boot volumes: confirmed.
- `modify-volume` options and the modification states confirmed; the 6-hour re-modify wait could not be confirmed and was replaced by the documented rule (wait for `completed`).
- The 20 percent gp3 price statement is quoted from the General Purpose SSD page; no other price or saving figure is kept. Removed the unconfirmed Compute Optimizer and account-default remarks.

Method: documentation only; no commands were run.
