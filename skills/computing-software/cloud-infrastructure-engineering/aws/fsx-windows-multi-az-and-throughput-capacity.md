---
id: computing-software.cloud-infrastructure-engineering.aws.fsx-windows-multi-az-and-throughput-capacity
name: fsx-windows-multi-az-and-throughput-capacity
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, fsx, fsx-multi-az, throughput-capacity, fsx-windows, storage-scaling]
level: advanced
status: docs-checked
description: "Run FSx for Windows File Server in Multi-AZ, size and change throughput capacity and storage, and plan for the failover and downtime each change causes."
sources: ["https://docs.aws.amazon.com/fsx/latest/WindowsGuide/high-availability-multiAZ.html", "https://docs.aws.amazon.com/fsx/latest/WindowsGuide/managing-throughput-capacity.html", "https://docs.aws.amazon.com/fsx/latest/WindowsGuide/managing-storage-capacity.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FSx for Windows Multi-AZ and throughput capacity

## 1. Multi-AZ
```bash
aws fsx create-file-system --file-system-type WINDOWS --storage-type SSD --storage-capacity 1024 \
  --subnet-ids subnet-a subnet-b --security-group-ids sg-fsx \
  --windows-configuration 'DeploymentType=MULTI_AZ_1,PreferredSubnetId=subnet-a,ThroughputCapacity=128,
    ActiveDirectoryId=d-1234567890,AutomaticBackupRetentionDays=14'
```
- Active and standby file servers in two AZs with synchronous replication; failover typically completes in under 30 seconds and the
  standby takes over serving reads and writes; when the preferred subnet is healthy again, FSx fails back automatically.
- Single-AZ file systems usually see about 30 minutes of downtime during failure recovery and the planned maintenance window.

## 2. Throughput capacity
Throughput capacity sets network throughput, CPU/memory for caching, and the disk throughput ceiling.
```bash
aws fsx update-file-system --file-system-id fs-0abc --windows-configuration ThroughputCapacity=256
```
- Multi-AZ: change happens with a failover and failback (brief interruption each).
- Single-AZ: the file system is unavailable for a few minutes during the change.
- Throughput capacity can be increased or decreased at any time; during failover and failback I/O may pause and CloudWatch metrics may be briefly unavailable.
- Schedule in a maintenance window; watch `describe-file-systems --query 'FileSystems[].AdministrativeActions'`.

## 3. Storage and IOPS
- Storage can only increase, never decrease. FSx adds a larger set of disks and runs a background storage optimization;
  a further increase is blocked until 6 hours after the last request or until optimization finishes, whichever is longer.
  Throughput capacity must be at least 16 MBps to increase storage.
- SSD IOPS: Automatic mode keeps 3 IOPS per GiB (up to 400,000 per file system); User-provisioned mode takes 96-400,000.
  Both are set through the file system's disk IOPS configuration.

## 4. Metrics to size by
`AWS/FSx`: `DataReadBytes`/`DataWriteBytes`, `CPUUtilization`, `NetworkThroughputUtilization`,
`FileServerDiskThroughputUtilization` (limit set by throughput capacity). `DiskThroughputUtilization` is HDD only
(limit set by the storage volumes). Raise throughput capacity when these metrics sit near their provisioned limit.

## Verify
- [ ] A test failover (change throughput in staging) shows clients reconnecting; Multi-AZ failover typically completes in under 30 seconds.

## Checked

2026-10-28. Confirmed against the FSx for Windows User Guide pages high-availability-multiAZ, managing-throughput-capacity, managing-storage-capacity and monitoring-cloudwatch: Multi-AZ failover time and automatic failback, throughput change triggers failover/failback, Single-AZ downtime, storage increase-only and 6-hour/16 MBps rules, SSD IOPS modes and ranges, and metric names.
Removed: the claim that a Single-AZ system cannot be converted to Multi-AZ, the "hours of optimization / performance dips" wording, and the 80% sizing threshold (not stated in the docs).
Method: documentation only; no commands were run.
