---
id: computing-software.systems-network-administration.virtualisation.hyper-v-replica-health-and-resync
name: hyper-v-replica-health-and-resync
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, hyper-v-replica, measure-vmreplication, replication-resync, replication-health, hrl, windows-server]
level: practitioner
status: docs-checked
description: "Monitor Hyper-V Replica health with Measure-VMReplication, interpret warning and critical states, and run resynchronisation after paused or broken replication."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/measure-vmreplication
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/resume-vmreplication
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-virtual-machines
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmreplication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V Replica health and resync

## Check health
```powershell
Get-VMReplication | Format-Table Name, State, Health, Mode, FrequencySec, PrimaryServer, ReplicaServer
Measure-VMReplication -VMName app01 | Format-List *
```
`Measure-VMReplication` reports the replication state and health; `Get-VMReplication` lists State, Health, Mode and FrequencySec.

## States
- **Normal**: replication cycles complete on schedule, backlog is minimal, no recent errors.
- **Warning**: replication works but lags or the backlog grows (often transient network or storage load); a placeholder VM waiting for an external-media import also shows Warning.
- **Critical**: replication stalls or fails and the RPO is at risk; check connectivity, storage capacity and performance, authentication, certificates and event logs, then resume or resynchronise.

## Change tracking
The primary records changes in `.hrl` files next to the VHDs and sends them each replication cycle. `Resume-VMReplication` resumes replication that is Paused, in Error, Suspended or needs resynchronisation.

## Resume and resync
```powershell
Resume-VMReplication -VMName app01                   # after a pause/network outage
Resume-VMReplication -VMName app01 -Resynchronize    # start resynchronisation
Resume-VMReplication -VMName app01 -Resynchronize -ResynchronizeStartTime (Get-Date '05:00').AddDays(1)   # schedule it, up to 7 days ahead
Set-VMReplication -VMName app01 -AutoResynchronizeEnabled $true -AutoResynchronizeIntervalStart 18:30 -AutoResynchronizeIntervalEnd 06:00
```
Resynchronisation needs significant storage, processor and network resources: schedule it off hours.

## Monitoring
Alert on any VM whose `Health` is not `Normal`, for example from a scheduled script over `Get-VMReplication`.

## Verify
After resync, `Get-VMReplication` shows State `Replicating` and Health `Normal`.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: Normal, Warning and Critical health meanings, .hrl change-tracking files, Resume-VMReplication states and -Resynchronize/-ResynchronizeStartTime (up to 7 days), the resource cost of resynchronisation, and the Set-VMReplication auto-resync parameters. Removed because no documentation page confirmed them: the 20% missed-cycle threshold, the half-VHD log-size rule, Reset-VMReplicationStatistics usage, and the named VMMS event-log channel.
Method: documentation only; no commands were run.
