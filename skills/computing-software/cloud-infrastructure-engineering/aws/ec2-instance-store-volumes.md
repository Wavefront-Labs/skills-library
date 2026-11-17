---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-instance-store-volumes
name: ec2-instance-store-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, nvme-instance-store, ephemeral-storage, instance-storage-raid, i4i, d3, data-loss-risk]
level: practitioner
status: docs-checked
description: "Use EC2 instance store NVMe disks safely: which types have them, formatting and RAID at boot, what survives reboot vs stop, and designs that tolerate losing the data."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-store-lifetime.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-store-volumes.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ssd-instance-store.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-instances-status-check_sched.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EC2 instance store volumes

## 1. What it is
Physically attached NVMe (or HDD on D-family) disks on the host. Very high IOPS and
throughput, low latency, included in the instance price. **Ephemeral**: data is lost when
the instance stops, hibernates, terminates, or the underlying disk/host fails.
| Event | Data |
|---|---|
| Reboot | kept |
| Stop / hibernate / terminate | **lost** |
| Host retirement, hardware failure | **lost** |
| Spot interruption (stop or terminate) | **lost** |
| Instance type change | does not persist |
Instance store is attached only at launch and cannot be moved between instances. Support depends on the type:
for example C8i, M8i and R8i have none, while C8id, M8id and R8id do. NVMe instance store volumes are encrypted
(XTS-AES-256, keys destroyed on stop or termination) and every volume of an NVMe-store type is attached
automatically at launch. Check a type:
```bash
aws ec2 describe-instance-types --instance-types i4i.2xlarge \
  --query 'InstanceTypes[].InstanceStorageInfo'
```

## 2. Preparing the disks at boot
SSD instance store volumes that support TRIM are fully trimmed before allocation and are not formatted when the
instance launches, so format and mount them yourself; skip the TRIM pass during formatting for faster access.
EBS volumes also appear as NVMe devices on Nitro-based instances, so identify the instance store disks
(for example with `lsblk -o NAME,SIZE,MODEL` or `nvme list`) rather than assuming device order. Run the
format-and-mount step from user data or a systemd unit on every boot (not just first boot), because stop/start
returns empty volumes.
- RAID 0 across devices for throughput; never RAID 1 for durability (all disks share fate
  with the host).
- On Linux, run `fstrim` periodically for TRIM-capable volumes, and leave about 10 percent of an SSD volume
  unpartitioned for over-provisioning to keep write performance up as the disk fills.
- Do not put instance store in fstab by device name; mount from the boot script. If you
  must, use `nofail` so a fresh empty disk does not block boot.

## 3. Good uses
- Caches (Redis replicas, CDN caches), buffers, scratch for ETL/Spark shuffle,
  temp tables, build workspaces.
- Replicated datastores that handle node loss: Cassandra, Kafka with replication factor 3,
  Elasticsearch/OpenSearch with replicas, distributed SQL (CockroachDB), ClickHouse with
  replication. Spread replicas across AZs; plan rebuild bandwidth.
- Swap on memory-hungry hosts where swap content is disposable.

## 4. Bad uses
- The only copy of anything. Databases on a single node.
- Anything you cannot rebuild from S3/EBS/replicas within your RTO.
- Workloads that stop/start nightly for cost savings (data gone each time).

## 5. Operations
- Monitor host health: scheduled events (`describe-instance-status` shows codes such as `instance-retirement`,
  `instance-stop`, `system-reboot`, `system-maintenance`). Instance retirement and instance stop events lose
  instance store data, so replace the node in your cluster before the date. AWS also sends AWS Health events
  you can route through EventBridge.
- Copy data you need to keep to persistent storage (EBS, S3 or EFS); do it at the application level.
- Spot with instance store: drain on interruption and let the cluster re-replicate.

## Gotchas
- Types with NVMe instance store attach every volume automatically; types with non-NVMe instance store (for
  example C1, C3, M1-M3, R3, D2, H1, I2, X1, X1e) need block device mappings at launch.
- Do not assume `/dev/nvme0n1` is the root volume or that instance store disks come first; identify disks by
  size and model with `lsblk`.

## Verify
- [ ] Boot script recreates and mounts the array on stop/start (test it once).
- [ ] Applications treat `/scratch` contents as disposable; recovery from node loss tested.
- [ ] Alarm or automation on scheduled retirement events for instance-store fleets.

## Checked

Date: 2026-10-27. Sources: EC2 User Guide pages "Data persistence for Amazon EC2 instance store volumes", "Instance store volume limits for EC2 instances", "SSD instance store volumes for EC2 instances" and "Scheduled events for Amazon EC2 instances".
Confirmed: reboot keeps data; stop, hibernate, terminate, instance type change, instance retirement, instance stop and failed disk do not; instance store attaches only at launch; NVMe volumes are encrypted and auto-attached; TRIM-capable volumes are unformatted and pre-trimmed; the 10 percent over-provisioning advice; scheduled event codes; describe-instance-types InstanceStorageInfo query.
Removed (not found in the pages): the named storage-optimized family list, the NVMe model string used in the boot script, the mkfs.xfs -K tip, the EMR remark, the "snapshots are impossible" statement and the two-minute Spot notice.

Method: documentation only; no commands were run.
