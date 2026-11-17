---
id: computing-software.messaging-and-integration.apache-kafka.kafka-disks-and-filesystem
name: kafka-disks-and-filesystem
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, xfs, ext4, noatime, log-dirs]
level: practitioner
status: docs-checked
description: "Choose data-disk layout and mount options: JBOD versus RAID, XFS versus EXT4, noatime and EXT4 tuning risks."
sources:
  - https://kafka.apache.org/42/operations/hardware-and-os/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: lay out disks and pick a filesystem for Kafka data.

Disks: use multiple drives, and do not share Kafka data drives with application logs or other OS filesystem activity, to protect latency. You can RAID them into one volume or mount each drive as its own directory. With several data directories, partitions are assigned round-robin and each partition lives entirely in one directory, so unbalanced partitions can unbalance disks. RAID balances at a lower level but usually costs write throughput and capacity, and RAID rebuilds are so I/O intensive they effectively disable the server, adding little availability beyond Kafka's own replication.

Filesystem: EXT4 and XFS are the common choices. In the docs' comparison XFS gave better Request Local Time (160ms versus 250ms+ for the best EXT4 setup) and less variability.

Mount option for all: `noatime`, because Kafka does not use access times.

XFS: defaults need little tuning. Optional: `largeio` (minimal effect) and `nobarrier` (only helps devices with battery-backed cache).

EXT4 options that raise performance but are unsafe in failures such as a power outage: `data=writeback`, disabling journaling, `commit=num_secs`, `nobh`, `delalloc`, and `fast_commit` (Linux 5.10+). Single-broker loss is recoverable from replicas, but multi-broker events can cause corruption that is hard to recover.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 hardware-and-os page; claims rewritten to match it. Removed the "bootstrapping consumers" atime detail and the data=ordered pairing as not confirmed. No hands-on run.
