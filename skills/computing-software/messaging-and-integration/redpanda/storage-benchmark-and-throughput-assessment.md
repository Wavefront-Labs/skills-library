---
id: computing-software.messaging-and-integration.redpanda.storage-benchmark-and-throughput-assessment
name: storage-benchmark-and-throughput-assessment
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [fio, storage, benchmark, rpk-topic-analyze, throughput, nvme, capacity]
level: practitioner
status: docs-checked
description: "Benchmark the Redpanda data disk with the documented fio sequential write job, and assess live throughput with rpk topic analyze."
sources:
  - https://docs.redpanda.com/streaming/current/deploy/redpanda/manual/sizing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Choose storage.** Locally attached NVMe SSD suits high throughput and low latency, but cloud local disks are ephemeral and wiped on instance restart. SSD-backed network storage persists but has slightly higher tail latency. The page cites AWS io2 (up to 64,000 IOPS, 1,000 MB/sec), gp3 as the cheaper option, and equivalents on GCP and Azure.

**Benchmark with fio** against the real block device (fio defaults to the local directory), replicating the sequential write pattern. Job from the page, run from the data directory:

```ini
[global]
name=fio-seq-write
filename=fio-seq-write
rw=write
bs=16K
direct=1
numjobs=4
group_reporting
time_based
runtime=300 # 5 minute runtime
[file1]
size=10G
ioengine=libaio
iodepth=16
```

Read IOPS, BW (bandwidth divided by block size gives IOPS), slat, clat and lat; watch clat percentiles from p90 up for predictable performance.

**Assess throughput**
```bash
rpk topic analyze --regex '*' --print-all --time-range -1m:end
```
`--regex '*'` analyzes all topics, `--print-all` prints every metric, `--time-range -1m:end` covers the last minute. The output has a SUMMARY (topics, partitions, total bytes/s, batch rate, average batch size), a per-topic table, and P25/P50/P75/P99 percentiles per partition. Consistent percentiles suggest balance; large variation suggests rebalancing. If one topic dominates throughput, it may need optimization.

Then compare against network, disk IOPS and CPU limits and scale up or out; uneven topics or partitions call for redistributing partitions or adjusting replication factors.

## Checked

2026-11-08. Read the whole Sizing Guidelines page. Confirmed: storage guidance (NVMe, ephemeral cloud disks, network-attached latency, io2 64,000 IOPS and 1,000 MB/sec, gp3), the fio job and its metric definitions, rpk topic analyze command and flags, output sections, percentile interpretation, capacity and bottleneck advice. Nothing removed.

Method: documentation only; no commands were run.
