---
id: computing-software.systems-network-administration.windows-server.hyper-v-replica-initial-replication-media
name: hyper-v-replica-initial-replication-media
category: computing-software
field: systems-network-administration
product: windows-server
tags: [hyper-v-replica, initial-replication-external-media, enable-vmreplication, import-vminitialreplication, disaster-recovery]
level: practitioner
status: docs-checked
description: "Seed Hyper-V Replica over slow links with initial replication to external media or an existing restored VM, then import on the replica host."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-virtual-machines
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/start-vminitialreplication
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/import-vminitialreplication
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V Replica initial replication via external media

Sending a large VM over a slow WAN can take days. Seed it by disk instead.

## Option 1: export to external media
```powershell
Enable-VMReplication -VMName FS01 -ReplicaServerName HVDR01.corp.example.com -ReplicaServerPort 80 -AuthenticationType Kerberos
Start-VMInitialReplication -VMName FS01 -DestinationPath <external media path>
```
This creates a placeholder VM on the replica site (health Warning) and writes the replica contents to a subfolder for
the VM on the media. Eject the media safely and move it to the replica server, then on a replica host:
```powershell
Import-VMInitialReplication -VMName FS01 -Path <path to the VM subfolder on the media>
```
When the import finishes, the initial checkpoint is applied to the placeholder VM, health changes to Normal, and
replication continues at the configured frequency. Check with `Get-VMReplication -VMName FS01` (State Replicating).

## Option 2: use an existing VM on the replica server
Restore the VM on the replica server and use it as the basis; only changes are then replicated. Use
`Start-VMInitialReplication -VMName FS01 -UseBackup` after `Enable-VMReplication`, as described on the
`Start-VMInitialReplication` reference page.

## Option 3: schedule network initial replication
```powershell
Start-VMInitialReplication -VMName FS01 -InitialReplicationStartTime (Get-Date '22:00')
```
Starts the initial copy over the network at a set time; the documentation allows up to seven days ahead.

## Gotchas
- Encrypt the seed media in transit with your organisation's disk-encryption tool.
- The placeholder VM on the replica is not meant to be started.
- The media needs space for all the VM's virtual disks.

## Verify
- [ ] After import: `Get-VMReplication -VMName FS01` shows State Replicating, Health Normal.

## Checked

2026-10-26 against the Windows Server docs (replication-virtual-machines, external media section; repository last commit 2026-10-23) and the Hyper-V module reference for Start-VMInitialReplication and Import-VMInitialReplication (Windows Server 2025): -DestinationPath, -UseBackup, -InitialReplicationStartTime, Import-VMInitialReplication -Path, the Warning-to-Normal health transition and checkpoint application. The docs page itself spells the import command Import-VMInitialReplica in one example; the module reference documents Import-VMInitialReplication. Removed unconfirmed claims about log growth during transit, BitLocker To Go and the 2 TB over 100 Mbit example.

Method: documentation only; no commands were run.
