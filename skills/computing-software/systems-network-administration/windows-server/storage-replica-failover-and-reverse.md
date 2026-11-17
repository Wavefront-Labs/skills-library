---
id: computing-software.systems-network-administration.windows-server.storage-replica-failover-and-reverse
name: storage-replica-failover-and-reverse
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, storage-replica, set-srpartnership, sr-failover, reverse-replication, disaster-recovery, test-failover, remove-srpartnership]
level: advanced
status: docs-checked
description: "Fail over Storage Replica: planned reversal with Set-SRPartnership, unplanned failover after source loss, test failover with Mount-SRDestination, and failback."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-replica/storage-replica-frequently-asked-questions
  - https://learn.microsoft.com/en-us/powershell/module/storagereplica/set-srpartnership
  - https://learn.microsoft.com/en-us/powershell/module/storagereplica/mount-srdestination
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Storage Replica failover and reverse replication

## Planned switch (both servers up)
Stop the application on the source, then reverse:
```powershell
Set-SRPartnership -NewSourceComputerName SR-SRV02 -SourceRGName RG02 `
  -DestinationComputerName SR-SRV01 -DestinationRGName RG01
```
The new source volume mounts; the old source becomes the destination and dismounts.
Synchronous replication means no data loss at the file system level.

## Unplanned (source dead)
Run the same command on the surviving destination to promote it to the new source.
If the log wrapped during a long outage, resync replays from the bitmap instead of the log,
which is typically slower to get back into sync.

## Test failover without breaking replication (2019+)
```powershell
Mount-SRDestination -Name SR-SRV02 -ComputerName SR-SRV02 -TemporaryPath T:\
# test the data read-write on the snapshot
Dismount-SRDestination -Name SR-SRV02 -ComputerName SR-SRV02
```
Writes go to the temporary volume; replication to the real destination volume continues. Use test failover only short term.

## Remove replication
```powershell
Get-SRPartnership | Remove-SRPartnership
Get-SRGroup | Remove-SRGroup       # on each server
```
The destination volume is remounted read/write again.

## Gotchas
- Never write to the destination via other means; it is dismounted for a reason.
- Async mode: unplanned failover loses whatever had not yet replicated (see
  `NumOfBytesRemaining` and the AsyncRPO setting).
- DNS/clients: Storage Replica moves storage, not names. Update DNS, DFS-N targets or
  use a cluster for name failover.

## Verify
- [ ] After reversal `Get-SRPartnership` shows the new source and destination.
- [ ] Replication healthy in the new direction.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23) and the windows-powershell-docs StorageReplica cmdlet pages. Confirmed Set-SRPartnership -NewSourceComputerName reversal, promotion of the destination after a disaster, Mount-SRDestination/Dismount-SRDestination (Windows Server 2019 and later, -TemporaryPath, short-term use only), Remove-SRPartnership/Remove-SRGroup remounting the volume read/write, and the bitmap resync after a log wrap. Removed unconfirmed claims about warning output, a full checksum resync and IsPrimary.

Method: documentation only; no commands were run.
