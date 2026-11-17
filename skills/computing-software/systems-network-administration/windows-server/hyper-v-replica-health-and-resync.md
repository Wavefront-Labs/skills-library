---
id: computing-software.systems-network-administration.windows-server.hyper-v-replica-health-and-resync
name: hyper-v-replica-health-and-resync
category: computing-software
field: systems-network-administration
product: windows-server
tags: [hyper-v-replica, measure-vmreplication, resynchronization, replication-health, disaster-recovery]
level: practitioner
status: docs-checked
description: "Monitor Hyper-V Replica health with Measure-VMReplication, interpret Warning and Critical states, and run or schedule resynchronization safely."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-virtual-machines
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/measure-vmreplication
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/resume-vmreplication
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmreplicationserver
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hyper-V Replica health and resynchronization

## Health
```powershell
Get-VMReplication -VMName APP01
Measure-VMReplication -VMName APP01
Measure-VMReplication -ReplicationHealth Warning      # filter: Normal, Warning, Critical, NotApplicable
```
- `LReplTime` is the last successful replication; `PReplSize(M)` and `AvgReplSize(M)` show replication size and
  `AvgLatency` the average latency. Compare `LReplTime` with the configured frequency (30 s, 5 min or 15 min).
- Normal: cycles complete on schedule and backlog is minimal.
- Warning: replication works but lags or backlog grows, often transient network or storage load. A placeholder VM
  waiting for an external-media import also shows Warning.
- Critical: replication stalls or fails and the RPO is at risk. Check connectivity, storage capacity and performance,
  authentication and certificates, and event logs.
- The monitoring interval (how often statistics are computed) is set on the replica server with
  `Set-VMReplicationServer -MonitoringInterval 12:00:00 -MonitoringStartTime 17:00:00`. Valid values are 1, 2, 3, 4, 6,
  8, 12 and 24 hours, or 2 to 7 days.

## Resume and resync
```powershell
Resume-VMReplication -VMName APP01                    # Paused, Error, Resynchronization Required or Suspended
Resume-VMReplication -VMName APP01 -Resynchronize     # for Resynchronization Required
Resume-VMReplication -VMName APP01 -Resynchronize -ResynchronizeStartTime '05:00'   # schedule it
Set-VMReplication -VMName APP01 -AutoResynchronizeEnabled $true -AutoResynchronizeIntervalStart 18:30 -AutoResynchronizeIntervalEnd 06:00
```
Resynchronization affects the host and its other VMs, so schedule it off-peak.

## Reset statistics after fixing
```powershell
Reset-VMReplicationStatistics -VMName APP01
```

## Alerting
Feed `Measure-VMReplication` output into monitoring and alert when Health is not Normal or `LReplTime` is older than
your RPO.

## Verify
- [ ] All VMs Health Normal; LReplTime within frequency.

## Checked

2026-10-26 against the Windows Server docs (replication-virtual-machines, monitoring section; repository last commit 2026-10-23) and the Hyper-V module reference (Windows Server 2025): health state meanings, Measure-VMReplication output columns and -ReplicationHealth values, Resume-VMReplication states, -Resynchronize and -ResynchronizeStartTime, the auto-resynchronize parameters, MonitoringInterval valid values, Reset-VMReplicationStatistics. Removed unconfirmed claims about the 20% missed-cycle rule, the 50% log threshold, event IDs 32022 and 32315, and a `3x frequency` alert rule.

Method: documentation only; no commands were run.
