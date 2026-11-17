---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.latency-numbers-and-resource-estimation
name: latency-numbers-and-resource-estimation
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [latency-numbers-cheat-sheet, resource-estimation, nalsd, back-of-the-envelope, system-design, performance]
level: advanced
status: docs-checked
description: "Estimate system resources with the classic latency numbers (memory, SSD, disk, datacenter RTT) and convert workloads into machine counts, NALSD style."
sources: ["https://sre.google/workbook/non-abstract-design/", "https://gist.github.com/jboner/2841832", "https://colin-scott.github.io/personal_website/research/interactive_latency.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Latency numbers and resource estimation

NALSD and capacity work rely on order-of-magnitude numbers. Precision is not the goal; being within a
a sensible factor and knowing which resource dominates is. The SRE Workbook (NALSD) says sound
reasoning and stated assumptions matter more than final values.

## Latency (the classic table, an old hardware generation)
From the widely copied "Latency Numbers Every Programmer Should Know" gist; treat as relative scale,
not current hardware.
| Operation | Time |
|---|---|
| L1 cache reference | 0.5 ns |
| Main memory reference | 100 ns |
| Compress 1K bytes | 3 us |
| Send 1K bytes over 1 Gbps network | 10 us |
| Read 1 MB sequentially from memory | 250 us |
| Round trip within same datacenter | 500 us |
| Read 1 MB sequentially from SSD | 1 ms |
| Disk seek | 10 ms |
| Read 1 MB sequentially from disk | 20 ms |

## Throughput per machine
The Workbook's NALSD example assumes a common 4 TB HDD sustains about 200 IOPS. Measure other
figures for your hardware or read the provider's published limits.

## Handy conversions
- 1 day ~ 86,400 s ~ 10^5 s; 1 month ~ 2.6 x 10^6 s; 1 year ~ 3.15 x 10^7 s.
- 1 M req/day ~ 12 req/s average.
- 1 Gbps ~ 125 MB/s ~ 10 TB/day.

## Estimation recipe
```
machines(resource) = demand(resource) / (per_machine_capacity(resource) * target_util)
machines = max over resources (CPU, RAM, disk capacity, disk IOPS, network)  -> then N+2, x regions
```
Example: when IOPS is the limit (as in the Workbook's query-log example with about 200 IOPS per HDD),
divide required IOPS by per-disk IOPS and target utilisation to see how many disks you need, then
compare with faster media.

## Gotchas
- Benchmarks you run beat any table; use tables only before you can measure.
- Cloud instance numbers vary by type; check the provider's published network and disk limits (burst vs baseline).

## Verify
- [ ] Every estimate names the dominating resource and per-machine capacity assumption.
- [ ] Assumptions replaced with measured numbers once a prototype exists.

## Checked
2026-11-01. Confirmed in the Latency Numbers gist (the nine table rows) and the SRE Workbook Non-Abstract Large System Design chapter (assumptions over exact values, 200 IOPS per HDD example, IOPS as limiting factor). The conversions are arithmetic. Removed: modern-hardware ranges, NVMe, NIC and HTTP throughput figures, intercontinental round trips, tail-latency fan-out claim, the spindle count.
Method: documentation only; no commands were run.
