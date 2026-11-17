---
id: computing-software.systems-network-administration.windows-server.storage-replica-server-to-server
name: storage-replica-server-to-server
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-replica, new-srpartnership, test-srtopology, server-to-server, disaster-recovery, block-replication]
level: advanced
status: docs-checked
description: "Set up server-to-server Storage Replica: prerequisites, Test-SRTopology report, data and log volumes, New-SRPartnership, and initial sync monitoring."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-replica/server-to-server-storage-replication
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-replica/storage-replica-frequently-asked-questions
  - https://learn.microsoft.com/en-us/powershell/module/storagereplica/new-srpartnership
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage Replica: server to server

Block-level, volume replication between two servers (Datacenter; Standard edition on Windows Server 2019 or later replicates a single volume up to 2 TB).

## Prerequisites
- Both servers domain joined, Windows Server Datacenter (or Standard 2019+ within its limit).
- Each server: a data volume and a log volume, same drive letters and sizes on both
  sides, GPT, not the system volume. Log on SSD/NVMe.
- Feature: install the File Server role and the Storage Replica feature, then restart (`Install-WindowsFeature Storage-Replica -IncludeManagementTools -Restart`).
- Network: ICMP, SMB 445 (5445 for SMB Direct) and WS-Man 5985 between servers, average 5 ms RTT or less for synchronous.

## Test first
```powershell
Test-SRTopology -SourceComputerName SR-SRV01 -SourceVolumeName F: -SourceLogVolumeName G: `
  -DestinationComputerName SR-SRV02 -DestinationVolumeName F: -DestinationLogVolumeName G: `
  -DurationInMinutes 30 -ResultPath '<vol>:\Temp'
```
Run during representative load; the HTML report checks the requirements and shows measured round-trip latency and write I/O.

## Create the partnership
```powershell
New-SRPartnership -SourceComputerName SR-SRV01 -SourceRGName RG01 -SourceVolumeName F: -SourceLogVolumeName G: `
  -DestinationComputerName SR-SRV02 -DestinationRGName RG02 -DestinationVolumeName F: -DestinationLogVolumeName G: `
  -LogSizeInBytes 32GB -ReplicationMode Synchronous   # log defaults to 8 GB if omitted
```
- Destination volume is dismounted and inaccessible while it is a destination.
- Seeded initial sync: copy data to the destination first (restore from backup) and add
  `-Seeded` to cut initial transfer.

## Monitor
```powershell
(Get-SRGroup).Replicas | Select DataVolume,ReplicationStatus,NumOfBytesRemaining
Get-WinEvent -ProviderName Microsoft-Windows-StorageReplica -MaxEvents 20 | fl
```
Admin-channel events: 1237 reports progress (bytes copied and remaining), 1215 reports block copy completed. Performance counters
under `Storage Replica Statistics`.

## Verify
- [ ] ReplicationStatus ContinuouslyReplicating on the destination.
- [ ] `Get-SRPartnership` shows the pair.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23) and the windows-powershell-docs StorageReplica cmdlet pages. Confirmed Standard edition limits, ports 445/5445/5985, 5 ms synchronous latency guidance, 8 GB default log with 10 GB minimum volume, -Seeded, Test-SRTopology report, and that events 1237 (progress) and 1215 (block copy completed) are the documented progress events. Removed the unconfirmed claim that event 5015 means bytes remaining.

Method: documentation only; no commands were run.
