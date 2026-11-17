---
id: computing-software.systems-network-administration.windows-server.storage-replica-log-sizing-and-modes
name: storage-replica-log-sizing-and-modes
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-replica, sr-log-volume, synchronous-replication, asynchronous-replication, rpo, set-srgroup, log-size]
level: advanced
status: docs-checked
description: "Size Storage Replica logs and choose synchronous vs asynchronous: latency limits, RPO, Test-SRTopology guidance, resizing logs and changing modes live."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-replica/storage-replica-frequently-asked-questions
  - https://learn.microsoft.com/en-us/powershell/module/storagereplica/set-srgroup
  - https://learn.microsoft.com/en-us/powershell/module/storagereplica/set-srpartnership
  - https://learn.microsoft.com/en-us/powershell/module/smbshare/set-smbbandwidthlimit
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage Replica log sizing and sync vs async

## Modes
| Mode | Write acknowledged when | RPO | Network |
|---|---|---|---|
| Synchronous | written to both source and destination logs | zero | average 5 ms RTT or less, enough bandwidth for the write workload |
| Asynchronous | written to source log | not guaranteed identical copies | no latency recommendation |
Synchronous adds the round trip to every write; a write-heavy SQL volume over a
10 ms link will crawl. Measure with `Test-SRTopology` first.

## Log size
- Default 8 GB, minimum 512 MB. The log must absorb writes during a link outage or
  slowdown; when it wraps a slower full resync is needed.
- Rule of thumb: sustained write throughput (`Avg Write Bytes/Sec` on the data disk) x seconds of outage you want to
  survive; e.g. 50 MB/s fills a 120 GB log in 40 minutes. `Test-SRTopology` also gives log sizing recommendations.
- A bigger log does not make replication faster; it only lets an outage last longer before resync falls back to the bitmap.
- Log volume: flash media (SSD), faster than the data volume, at least 10 GB, dedicated to the log.

## Change live
```powershell
Set-SRGroup -ComputerName SR-SRV01 -Name RG01 -LogSizeInBytes 64GB
Set-SRGroup -ComputerName SR-SRV02 -Name RG02 -LogSizeInBytes 64GB
Set-SRPartnership -SourceComputerName SR-SRV01 -SourceRGName RG01 `
  -DestinationComputerName SR-SRV02 -DestinationRGName RG02 -ReplicationMode Asynchronous
Set-SRPartnership -SourceComputerName SR-SRV01 -SourceRGName RG01 `
  -DestinationComputerName SR-SRV02 -DestinationRGName RG02 -AsyncRPO 60   # alert threshold in seconds, minimum 30
```
Set log size on both ends. AsyncRPO only changes monitoring (event 1239 when exceeded, 1240 when back within); it does not affect replication or I/O.

## Bandwidth control
```powershell
Set-SRNetworkConstraint -SourceComputerName SR-SRV01 -SourceRGName RG01 -SourceNWInterface 2 `
  -DestinationComputerName SR-SRV02 -DestinationRGName RG02 -DestinationNWInterface 3
Set-SmbBandwidthLimit -Category StorageReplication -BytesPerSecond 500MB   # needs FS-SMBBW feature
```

## Verify
- [ ] `Get-SRGroup | Select Name,LogSizeInBytes,ReplicationMode` and `Get-SRPartnership` show the new values.
- [ ] `Test-SRTopology` re-run after the change shows the measured latency within the 5 ms synchronous guidance.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23) and the windows-powershell-docs StorageReplica and SmbShare cmdlet pages. Confirmed the 8 GB default log, 512 MB minimum (Set-SRGroup -LogSizeInBytes), 10 GB log volume recommendation, 5 ms synchronous guidance, log-sizing formula, Set-SRPartnership -AsyncRPO (event 1239/1240, monitoring only), Set-SRNetworkConstraint and Set-SmbBandwidthLimit -Category StorageReplication (needs the FS-SMBBW feature). Fixed: AsyncRPO is a Set-SRPartnership parameter, not Set-SRGroup. Removed the unconfirmed Avg. Network Send Latency counter.

Method: documentation only; no commands were run.
