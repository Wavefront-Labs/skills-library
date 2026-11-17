---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.iops-sizing
name: iops-sizing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, storage-selection, iops-sizing, throughput, gp3, disk-performance]
level: practitioner
status: docs-checked
description: "Size IOPS and throughput for cloud block storage: measure workload IO, match volume types, check VM-level limits and bursting, and read per-volume limits from the vendor tables."
sources: ["https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html", "https://learn.microsoft.com/azure/virtual-machines/disks-types", "https://docs.cloud.google.com/compute/docs/disks/performance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IOPS and throughput sizing

## Steps
1. **Measure** the workload: peak and high-percentile read and write IOPS, throughput, IO size and queue
   depth, plus latency. Throughput is roughly IOPS multiplied by IO size.
2. **Choose a volume type** from the vendor's current limits table; limits change and depend on IO size.
   - AWS EBS: the page lists maximum IOPS and throughput per volume type. At the time checked: gp3 up to
     80,000 IOPS and 2,000 MiB/s, gp2 up to 16,000 IOPS and 250 MiB/s, io2 Block Express up to 256,000 IOPS
     and 4,000 MiB/s, io1 up to 64,000 IOPS and 1,000 MiB/s. io2 Block Express targets consistent
     sub-millisecond latency (average under 500 microseconds for 16 KiB I/O) and sustained IOPS. On
     Outposts the gp3 limits are lower (16,000 IOPS, 1,000 MiB/s).
   - Azure: Ultra Disk IOPS and throughput can be adjusted at runtime without detaching; a resize can take
     up to an hour to take effect, with at most four performance resizes in 24 hours. Premium SSD and
     Standard SSD offer disk bursting for unpredictable I/O patterns and spiky traffic.
   - Google Cloud: Persistent Disk limits depend on the machine type and vCPU count; to reach a target you
     must size both the disk and a VM that can deliver it. Hyperdisk performance has its own pages.
3. **Check the VM limit**: maximum performance varies by machine series and type, so a fast volume on a
   small machine can be capped by the machine.
4. **Avoid depending on bursting for sustained load.** Bursting covers spikes; size baseline performance for
   steady demand (see each vendor's bursting description).
5. **Validate** with a benchmark that uses the workload's IO size and queue depth.

## Gotchas
- Latency matters as much as IOPS for databases; check average and tail latency.
- Table limits assume particular IO sizes; compare like with like.

## Verify
- [ ] Benchmark results meet the measured peak with headroom.
- [ ] Cloud monitoring shows no throttling at peak.

## Checked
2026-11-01. Confirmed against the EBS volume types page (maximum IOPS and throughput rows, io2 Block Express
latency), the Azure managed disk types page (Ultra Disk runtime resize, bursting) and the Compute Engine disk
performance page (machine type and vCPU dependence). Removed: the old gp3 16,000 IOPS ceiling and its
3,000 IOPS / 125 MiB/s baseline (the page's table gives 80,000 IOPS and the baseline row was not readable),
Azure and Google per-type scaling claims, the striping advice, the snapshot lazy-load gotcha and tool
commands (`iostat`, PerfMon, `fio`).
Method: documentation only; no commands were run.
