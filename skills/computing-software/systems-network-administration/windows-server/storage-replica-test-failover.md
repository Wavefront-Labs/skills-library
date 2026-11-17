---
id: computing-software.systems-network-administration.windows-server.storage-replica-test-failover
name: storage-replica-test-failover
category: computing-software
field: systems-network-administration
product: windows-server
tags: [storage-replica, mount-srdestination, sr-failover, disaster-recovery, test-failover]
level: advanced
status: docs-checked
description: "Run Storage Replica test failovers with Mount-SRDestination: snapshot the destination to a temp volume, test apps, then dismount without breaking replication."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-replica/storage-replica-frequently-asked-questions
  - https://learn.microsoft.com/en-us/powershell/module/storagereplica/mount-srdestination
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-replica/storage-replica-known-issues
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage Replica test failover

Since Server 2019, a replication destination can be mounted read-write as a **snapshot** without stopping
replication, so DR tests no longer need a real failover.

## Prerequisites
- An unused NTFS or ReFS volume on the destination server that is not being replicated, to hold the snapshot differences; size it for the writes you expect during the test.
- Destination partnership healthy (`Get-SRGroup` ReplicationStatus ContinuouslyReplicating).

## Mount
```powershell
Mount-SRDestination -Name DR01 -ComputerName DR01 -TemporaryPath T:\
```
The replicated volume becomes accessible read/write (you can also copy files off it or run an online backup). The temporary volume holds log data. Replication to the
real destination volume continues underneath.

## Test
Start the application on DR01 against D:, check data consistency, run app smoke tests. For clustered workloads use a
test network to avoid name or IP conflicts with production.

## Dismount
```powershell
Dismount-SRDestination -Name DR01 -ComputerName DR01
```
All test writes are discarded; the destination returns to its replicated state.

## Gotchas
- Use test failover only for short-term, temporary operations, not long-term.
- Do not point production clients at the test copy; its changes are discarded.
- Asynchronous replication: the snapshot is only as current as what has replicated; note the RPO you observed.
- If Mount-SRDestination fails with error 5823 (group or resource not in the correct state), see the Storage Replica known-issues page.

## Verify
- [ ] Test recorded with time-to-mount, app results, and dismount confirmed (`Get-SRGroup` shows ContinuouslyReplicating).

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23) and the windows-powershell-docs StorageReplica cmdlet pages. Confirmed Windows Server 2019 as the first release with this feature, the unused NTFS/ReFS non-replicating volume requirement, Mount-SRDestination -Name -ComputerName -TemporaryPath and Dismount-SRDestination, discarding changes on dismount, short-term-only guidance, and error 5823. Removed unconfirmed one-mount-at-a-time and out-of-space claims.

Method: documentation only; no commands were run.
