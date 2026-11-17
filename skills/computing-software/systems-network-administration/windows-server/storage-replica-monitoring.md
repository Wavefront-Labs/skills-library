---
id: computing-software.systems-network-administration.windows-server.storage-replica-monitoring
name: storage-replica-monitoring
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-replica, sr-monitoring, get-srgroup, performance-counters, replication-health]
level: advanced
status: docs-checked
description: "Monitor Storage Replica health: replication status and bytes remaining with Get-SRGroup, SR performance counters, event IDs and alerting on lag."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-replica/storage-replica-frequently-asked-questions
  - https://learn.microsoft.com/en-us/powershell/module/storagereplica/get-srgroup
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-replica/storage-replica-known-issues
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitor Storage Replica

## Status
```powershell
(Get-SRGroup).Replicas | Select DataVolume,ReplicationMode,ReplicationStatus,NumOfBytesRemaining,LastInSyncTime
Get-SRPartnership
```
`ReplicationStatus`: `ContinuouslyReplicating` is the healthy state and `InitialBlockCopy` is the initial sync; treat anything else as needing investigation.
`NumOfBytesRemaining` on the destination shows what is left to copy.
Watch initial sync drain:
```powershell
while ($true) { (Get-SRGroup -ComputerName SR-SRV02 -Name rg02).Replicas | ft DataVolume,NumOfBytesRemaining; Start-Sleep 30 }
```

## Performance counters
Object **Storage Replica Statistics**; the documented counter is **Total Bytes Received** on the destination, per replicated volume.
```powershell
Get-Counter -ComputerName SR-SRV02 -Counter '\Storage Replica Statistics(*)\Total Bytes Received'
```

## Events
Applications and Services Logs > Microsoft > Windows > StorageReplica > Admin (provider `Microsoft-Windows-StorageReplica`).
- 1237 on the destination shows bytes copied and remaining every 10 seconds during initial sync; 1215 is block copy completed.
- For asynchronous partnerships, 1239 means the AsyncRPO was exceeded and 1240 means it is back within; 1241 warnings repeating on the source are a known issue worth checking.
- Collect with WEF or Azure Monitor and alert on any Admin channel error or warning.

## Alerting
Scheduled script: alert if any replica is not continuously replicating for >10 min or async bytes remaining
exceeds what you can lose (RPO). The AsyncRPO value on the partnership drives events 1239/1240 and, on clusters, Health Service alerts.

## Verify
- [ ] Dashboard/alert fires when the replication network is unplugged in a test window and clears afterwards.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23) and the windows-powershell-docs StorageReplica cmdlet pages. Confirmed Get-SRGroup Replicas fields (ReplicationStatus, NumOfBytesRemaining, LastInSyncTime), ContinuouslyReplicating and InitialBlockCopy values, the Total Bytes Received counter, Admin channel events 1237/1215, and AsyncRPO events 1239/1240. Removed the unconfirmed status values, counter names, Operational channel claims and Failover Cluster Manager tab.

Method: documentation only; no commands were run.
