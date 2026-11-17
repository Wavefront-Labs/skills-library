---
id: computing-software.systems-network-administration.virtualisation.vsphere-performance-charts-and-statistics-levels
name: vsphere-performance-charts-and-statistics-levels
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsphere-monitoring, performance-charts, statistics-level, rollup, cpu-ready, get-stat, realtime-stats, vmware, vcenter, vsphere]
level: practitioner
status: docs-checked
description: "Use vCenter performance charts: real-time vs historical intervals, statistics levels 1-4 and their database cost, key counters per resource, and pulling stats with Get-Stat."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-configuration/configuring-vcenter-server-using-the-vsphere-client/configuring-vcenter-server-in-the-vsphere-client/configuring-statistics-settings-in-the-vsphere-client/configure-statistics-intervals-for-vcenter-server-in-the-vsphere-client.html
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-monitoring-and-performance/monitoring-inventory-objects/data-counters.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# vCenter performance charts and statistics levels

**Goal:** get the right counters at the right resolution to prove or rule out a resource
bottleneck, without bloating the vCenter database.

## Intervals
| Interval | Sample period | Kept | Source |
|---|---|---|---|
| Real-time | seconds | short | ESXi host |
| Past day | 5 min | 1 day | vCenter |
| Past week | 30 min | 1 week | vCenter |
| Past month | 2 h | 1 month | vCenter |
| Past year | 1 day | 1 year | vCenter |
Short spikes vanish in rollups: a 30-second CPU ready storm is visible only in real-time
(or esxtop). Investigate live problems live.

## Statistics levels
Level 1 (the default for all intervals) covers basic CPU, memory, disk, network and system
metrics. Level 2 adds more counters, level 3 adds device metrics, and level 4 uses all
counters including minimum and maximum rollup values. Using levels 3 or 4 beyond the
default can make the vpxd process sustain memory growth; raise **temporarily** for the
day interval when troubleshooting, then lower.

## Counters that matter
| Resource | Counter | Warning sign |
|---|---|---|
| CPU | Ready (ms, summation) | sustained ready time (convert ms to % per vCPU) |
| CPU | Co-stop | sustained co-stop (too many vCPUs) |
| Memory | Balloon, Swapped/Swap in rate, Compressed | any sustained non-zero |
| Disk | Device/kernel/guest latency (read/write) | sustained device or kernel latency |
| Network | Dropped packets RX/TX | non-zero sustained |
Convert ready ms to %: ready_ms / (interval_s × 1000) × 100, per vCPU.

## Programmatic access
Pull counters with PowerCLI `Get-Stat` (verify current cmdlet parameters against the
PowerCLI documentation) or with the govc metric and object.collect commands from the
govc usage reference.

## Verify
For an incident, record the counter, interval and object used to reach the conclusion;
statistics levels are back to their normal values afterwards.

## Checked
2026-10-31: Collection intervals and retention (5 min kept 1 day, 30 min kept 1 week, 2 h kept 1 month, 1 day kept 1 year), level 1 as default for all intervals, level 2/3/4 counter coverage, level 4 including min/max rollups, and the vpxd memory-growth warning confirmed on the Configure Statistics Collection Intervals and Data Collection Levels pages. Removed unconfirmed figures: real-time 20 s sample/1 hour retention, warning thresholds (1000 ms, 5%, 3%, 20 ms, 2 ms) and Get-Stat parameter specifics.
Method: documentation only; no commands were run.
