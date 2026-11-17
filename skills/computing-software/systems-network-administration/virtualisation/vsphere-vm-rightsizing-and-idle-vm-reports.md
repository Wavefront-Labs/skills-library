---
id: computing-software.systems-network-administration.virtualisation.vsphere-vm-rightsizing-and-idle-vm-reports
name: vsphere-vm-rightsizing-and-idle-vm-reports
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [rightsizing, idle-vm, capacity-planning, powercli, vmware, vsphere]
level: practitioner
status: draft
description: "Find oversized and idle vSphere VMs from performance statistics with PowerCLI, pick safe thresholds, and resize without surprising application owners."
sources:
  - https://developer.broadcom.com/powercli/latest/vmware.vimautomation.core/commands/get-stat
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM right-sizing and idle VM reports

**Goal:** return wasted vCPU, RAM and storage, and stop paying for VMs nobody uses.

## Data you need
At least 30 days of statistics at a level that keeps daily rollups (Statistics level 1 keeps `cpu.usage.average`, `mem.usage.average`; level 2+ for `mem.active`). Batch and month-end peaks need a full month or more.

## PowerCLI report
```powershell
$start = (Get-Date).AddDays(-30)
Get-VM | Where PowerState -eq PoweredOn | ForEach-Object {
  $cpu = Get-Stat -Entity $_ -Stat cpu.usage.average -Start $start -IntervalMins 120 -ErrorAction SilentlyContinue | Measure-Object Value -Average -Maximum
  $mem = Get-Stat -Entity $_ -Stat mem.usage.average -Start $start -IntervalMins 120 -ErrorAction SilentlyContinue | Measure-Object Value -Average -Maximum
  $net = Get-Stat -Entity $_ -Stat net.usage.average -Start $start -IntervalMins 120 -ErrorAction SilentlyContinue | Measure-Object Value -Maximum
  [pscustomobject]@{VM=$_.Name; vCPU=$_.NumCpu; MemGB=$_.MemoryGB
    CpuAvg=[math]::Round($cpu.Average,1); CpuPeak=[math]::Round($cpu.Maximum,1)
    MemAvg=[math]::Round($mem.Average,1); NetPeakKBps=$net.Maximum }
} | Export-Csv rightsizing.csv -NoTypeInformation
```

## Thresholds (starting points)
- **Oversized CPU**: peak under 50% and average under 20% -> remove vCPUs (keep at least 2 for most server OSes).
- **Undersized CPU**: CPU ready over 5% per vCPU, or sustained peak over 85%.
- **Oversized memory**: guest-reported memory use well below allocation for the whole period; host `mem.active` underestimates real need, so confirm with in-guest metrics.
- **Idle**: CPU average under ~2%, network under ~1 KBps, and almost no disk I/O for 30 days.
- **Zombie**: powered off for 30+ days; check owner, then archive and delete.

## Acting safely
- Reducing vCPU or RAM needs a power cycle (hot-remove is not supported); schedule with owners.
- Licensing tied to cores (SQL, Oracle) often justifies resizing first.
- Fewer vCPUs often improves performance (less co-stop, fits a NUMA node).
- Record before/after and keep a rollback path.

## Verify
After changes, CPU ready and guest response times stay within limits for a full business cycle.
