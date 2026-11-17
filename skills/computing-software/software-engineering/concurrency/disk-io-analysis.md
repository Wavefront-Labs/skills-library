---
id: computing-software.software-engineering.concurrency.disk-io-analysis
name: disk-io-analysis
category: computing-software
field: software-engineering
product: concurrency
tags: [performance, disk-io, iostat, biolatency, storage-performance, linux]
level: advanced
status: draft
description: "Analyse disk I/O performance with iostat, pidstat, iotop, biolatency and biosnoop: saturation, latency histograms, per-process attribution and cloud volume limits."
sources: ["https://man7.org/linux/man-pages/man1/iostat.1.html", "https://github.com/iovisor/bcc/blob/master/tools/biolatency_example.txt", "https://www.brendangregg.com/USEmethod/use-linux.html", "https://docs.aws.amazon.com/ebs/latest/userguide/ebs-io-characteristics.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Disk I/O analysis (iostat / biolatency)

## iostat first
```
iostat -xz 1
Device  r/s   w/s   rkB/s  wkB/s  r_await w_await aqu-sz  %util
nvme0n1 850  1200  34000  96000   0.4     6.8     9.1    98.0
```
- `r_await`/`w_await`: average ms per I/O **including queue time**. Compare to device expectations
  (NVMe < 1 ms, SSD network volumes 1-3 ms, HDD 5-15 ms).
- `aqu-sz` (avgqu-sz): average queue depth: saturation indicator.
- `%util`: busy time. Near 100% is saturation for HDDs; for SSD/NVMe (parallel devices) it can show
  100% with headroom left. Use latency and queue depth instead.
- r/s, w/s, rkB/s give IOPS and throughput; divide to get average I/O size.

## Who is doing it
```
pidstat -d 1                  # per-process kB read/written
iotop -oPa                    # accumulated I/O by process
sudo biotop                   # BCC: top processes by block I/O
```

## Latency distributions (averages hide outliers)
```
sudo biolatency -D 10 1       # histogram per disk
sudo biosnoop                 # each I/O: process, sector, size, latency
sudo ext4slower 10            # file system ops slower than 10 ms (xfsslower, btrfsslower...)
```
Bimodal histograms = cache hits vs device; long tails = queueing, GC in SSD firmware, throttling.

## Common findings
- **Cloud volume limits**: AWS EBS gp3 baseline 3000 IOPS/125 MB/s unless provisioned higher; burst
  credits on gp2/st1; instance-level EBS bandwidth caps. CloudWatch `VolumeQueueLength`,
  `VolumeThroughputPercentage`; Azure/GCP have similar disk throttling metrics.
- fsync-heavy workloads (databases, logs with `sync`) dominated by write latency: batch commits,
  group commit, faster log device.
- Swapping (`vmstat 1` `si`/`so` > 0) masquerading as disk load.
- Page cache misses after memory pressure: `cachestat` (BCC), `free -m` buff/cache.
- Small random I/O on HDD; read amplification from wrong block/readahead settings
  (`blockdev --getra`).
- Log files or temp files on the same volume as the database.

## Verify capacity
`fio --name=randread --rw=randread --bs=4k --iodepth=32 --direct=1 --size=4G --runtime=60` to
measure what the device can actually do, then compare with observed load.
