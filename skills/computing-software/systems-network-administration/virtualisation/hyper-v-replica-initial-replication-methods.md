---
id: computing-software.systems-network-administration.virtualisation.hyper-v-replica-initial-replication-methods
name: hyper-v-replica-initial-replication-methods
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [initial-replication, replication-frequency, hyper-v-replica, enable-vmreplication, seeding, hyper-v]
level: practitioner
status: docs-checked
description: "Seed Hyper-V Replica efficiently: over the network on a schedule, via external media export/import, or from a restored backup, and choose replication frequency."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/start-vminitialreplication
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/import-vminitialreplication
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-virtual-machines
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmreplication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Initial replication methods

After `Enable-VMReplication`, the full VM must reach the replica once.

## 1. Over the network (default)
```powershell
Start-VMInitialReplication -VMName app01                                    # now
Start-VMInitialReplication -VMName app01 -InitialReplicationStartTime (Get-Date "2026-10-19 22:00")
```
Fine on LAN or for small VMs. For big VMs over WAN, schedule out of hours and keep compression enabled (`Set-VMReplication -CompressionEnabled $true`; compression is on by default).

## 2. External media (large VMs over slow links)
```powershell
Start-VMInitialReplication -VMName app01 -DestinationPath "<MEDIA_DIR>\IR"
```
Ship the disk; on the replica server:
```powershell
Import-VMInitialReplication -VMName app01 -Path "<MEDIA_DIR>\IR\app01_<guid>"
```
The replica VM exists as a placeholder with health Warning until the import completes; replication then continues at the configured frequency.

## 3. From an existing VM on the replica side (restored backup)
Restore the VM from backup at the DR site, mark it as the replica VM, then start initial replication from the primary using the restored copy:
```powershell
Set-VMReplication -VMName app01 -AsReplica                 # on replica server: the restored VM becomes the seed
Start-VMInitialReplication -VMName app01 -UseBackup        # on primary
```
`-UseBackup` on `Start-VMInitialReplication` must match the option used when replication was enabled.

## Replication frequency
`-ReplicationFrequencySec 30 | 300 | 900` (30 s, 5 min, 15 min). Choose by RPO, criticality and available bandwidth; the default in the documented PowerShell example is 5 minutes.

## Gotchas
- Exclude disks you do not need at the replica (for example page-file or temp disks) with `-ExcludedVhd` or `-ExcludedVhdPath` on `Enable-VMReplication`.
- A scheduled start can be at most seven days ahead (`-InitialReplicationStartTime`).

## Verify
`Get-VMReplication -VMName app01` shows State `Replicating` and Health `Normal`.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: Start-VMInitialReplication -InitialReplicationStartTime (up to seven days) and -DestinationPath, Import-VMInitialReplication -Path, placeholder VM with Warning health until import, -UseBackup and -AsReplica semantics, frequencies of 30 s, 5 min and 15 min, and -ExcludedVhd/-ExcludedVhdPath. Removed because no documentation page confirmed them: the claims about dynamic versus fixed disk copy size and HRL log growth during seeding.
Method: documentation only; no commands were run.
