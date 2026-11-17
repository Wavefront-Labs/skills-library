---
id: computing-software.systems-network-administration.windows-server.diagnose-storage-latency
name: diagnose-storage-latency
category: computing-software
field: systems-network-administration
product: windows-server
tags: [performance-monitoring, disk-latency, performance-counters, storage-spaces, resource-monitor]
level: practitioner
status: draft
description: "Diagnose slow storage on Windows Server: Avg Disk sec/Transfer thresholds, queue length, per-process I/O, Storport tracing and separating host from array issues."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server
  - https://learn.microsoft.com/en-us/windows-server/administration/performance-tuning
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing storage latency

## The counters that matter
`LogicalDisk(*)` / `PhysicalDisk(*)`:
- **Avg. Disk sec/Read** and **sec/Write**: latency. Rough guide for HDD-era apps: < 10 ms good, 10-20 ms tolerable,
  > 25 ms bad. SSD/NVMe should be well under 1-2 ms.
- **Disk Transfers/sec** (IOPS) and **Disk Bytes/sec** (throughput): tells you whether latency rises with load.
- **Current Disk Queue Length**: sustained high values with high latency = saturated path.
- **% Idle Time** is more meaningful than % Disk Time on modern storage.

```powershell
Get-Counter '\LogicalDisk(*)\Avg. Disk sec/Read','\LogicalDisk(*)\Avg. Disk sec/Write','\LogicalDisk(*)\Disk Transfers/sec' -SampleInterval 5 -MaxSamples 12
```

## Who is doing the I/O
Resource Monitor > Disk tab (per process and per file), or:
```powershell
Get-Counter '\Process(*)\IO Data Bytes/sec' | Select -Expand CounterSamples | Sort CookedValue -Desc | Select -First 10 InstanceName,CookedValue
```
Usual suspects: antivirus scans, backup, indexing, SQL checkpoints, log shipping.

## Host or array?
- Latency high at the LogicalDisk but the array reports low latency: problem in the host path (HBA queue depth, MPIO
  policy, driver/firmware, CPU starvation on the host).
- Both high: array/backend saturated.
- Storport/disk events in System log (129 resets, 153 retried I/O) point at the path.
- For deep dives: `wpr -start GeneralProfile -start DiskIO` then analyse Storage I/O graphs in WPA, or Storport ETW
  tracing for per-request latency at the miniport.

## Common fixes
Exclude database/VM folders from antivirus, align backup windows, MPIO Round Robin vs Failover Only per vendor,
update HBA firmware/drivers, move hot files to faster tiers, raise queue depth per vendor guidance.

## Verify
- [ ] Latency within target at peak load in a new counter capture.
