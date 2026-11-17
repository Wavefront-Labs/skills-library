---
id: computing-software.cloud-infrastructure-engineering.aws.ebs-volume-status-checks-and-queue-length
name: ebs-volume-status-checks-and-queue-length
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ebs, volume-status-checks, volumequeuelength, ebs-monitoring, cloudwatch]
level: advanced
status: docs-checked
description: "Monitor EBS health and performance: volume status checks and auto-enable IO, VolumeQueueLength and latency maths, throughput and burst balance metrics."
sources: ["https://docs.aws.amazon.com/ebs/latest/userguide/monitoring-volume-checks.html", "https://docs.aws.amazon.com/ebs/latest/userguide/using_cloudwatch_ebs.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-io-characteristics.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-cloud-watch-events.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Volume status checks and VolumeQueueLength

## 1. Status checks
```bash
aws ec2 describe-volume-status --volume-ids vol-0abc \
  --query 'VolumeStatuses[].{status:VolumeStatus.Status,details:VolumeStatus.Details,events:Events}'
```
| Status | Meaning |
|---|---|
| `ok` | fine |
| `warning` | I/O performance degraded or severely degraded (io1, io2 and gp3 only) |
| `impaired` | I/O disabled after possible data inconsistency, or performance stalled |
| `insufficient-data` | checks may still be in progress |
Checks run about every 5 minutes (the I/O performance check every minute, collected by CloudWatch every
5 minutes). After a possible inconsistency EBS disables I/O to protect data; run `fsck` or `chkdsk`, then
`aws ec2 enable-volume-io --volume-id vol-0abc`. For volumes where availability beats caution:
`aws ec2 modify-volume-attribute --volume-id vol-0abc --auto-enable-io`. The I/O performance check does not apply to gp2, st1, sc1 or standard volumes.

## 2. Performance metrics (`AWS/EBS`)
- `VolumeReadOps`, `VolumeWriteOps`, `VolumeReadBytes`, `VolumeWriteBytes` (sum per period).
- Average latency per op = `VolumeTotalReadTime / VolumeReadOps` (metric math).
- `VolumeQueueLength`: outstanding I/Os. By Little's law, queue length = IOPS × latency. A long queue
  with high latency and IOPS at the provisioned limit means the volume is the bottleneck; a short queue
  with low IOPS means the application is not issuing enough parallel I/O.
- `VolumeThroughputPercentage`, `VolumeConsumedReadWriteOps` (Provisioned IOPS SSD volumes only).
- `BurstBalance` (gp2, st1, sc1 only): the percentage of I/O or throughput credits left; near zero means you fell to baseline, so consider gp3.
- `VolumeIdleTime`, and `VolumeStalledIOCheck` (Nitro instances) for impaired detection.
- Instance side: `EBSIOBalance%` and `EBSByteBalance%` (basic monitoring only, and only for some `*.4xlarge` instance sizes) show the burst bucket of burstable EBS bandwidth.

## 3. Alarms
`VolumeQueueLength` high plus latency high for 10 minutes; `BurstBalance < 20`; status check not ok via
EventBridge `EBS Volume Notification` events.

## Verify
- [ ] Dashboard per critical volume with IOPS vs provisioned, latency, queue length and burst balance.

## Checked

Checked 2026-10-27 against the Amazon EBS User Guide (Volume status checks, Amazon CloudWatch metrics for EBS, EBS events) and the botocore EC2 model.
- Status values, which volume types get the I/O performance check, auto-enable I/O, `enable-volume-io` and the `fsck` or `chkdsk` advice confirmed on the status checks page.
- Metric names, their volume-type restrictions (`BurstBalance`, `VolumeThroughputPercentage`, `VolumeConsumedReadWriteOps`), `VolumeStalledIOCheck` and the instance burst metrics (limited to some `*.4xlarge` sizes) confirmed on the CloudWatch metrics page; the average latency formula matches the documented metric math.
- The `EBS Volume Notification` detail type confirmed on the EBS events page. The `ModifyVolumeAttribute` `AutoEnableIO` member and `EnableVolumeIO` confirmed in the service model.

Method: documentation only; no commands were run.
