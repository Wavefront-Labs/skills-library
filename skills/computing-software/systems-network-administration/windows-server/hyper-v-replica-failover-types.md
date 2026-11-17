---
id: computing-software.systems-network-administration.windows-server.hyper-v-replica-failover-types
name: hyper-v-replica-failover-types
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, hyper-v-replica, test-failover, planned-failover, unplanned-failover, start-vmfailover, reverse-replication, complete-vmfailover, hyper-v-replica-reverse]
level: practitioner
status: docs-checked
description: "Run Hyper-V Replica test, planned and unplanned failovers with PowerShell: commands, recovery point choice, reverse replication and failback."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-failover
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/start-vmfailover
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/complete-vmfailover
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hyper-V Replica failover: test, planned, unplanned

## Test failover (no impact on replication)
On the replica host:
```powershell
Start-VMFailover -VMName APP01 -AsTest          # creates 'APP01 - Test' from the latest recovery point
Start-VM -Name 'APP01 - Test'
# verify the app, then
Stop-VMFailover -VMName APP01                   # deletes the test VM and discards its data
```
The test VM is not connected to a network by default, and only one test failover can run per VM at a time. Attach it to
an isolated switch if the test needs networking.

## Planned failover (both sites up, no data loss)
```powershell
# on the primary
Stop-VM -Name APP01                              # the VM must be shut down
Start-VMFailover -VMName APP01 -Prepare          # replicates pending changes
# on the replica
Start-VMFailover -VMName APP01
Set-VMReplication -VMName APP01 -Reverse         # reverse replication, same settings as before
Start-VM -Name APP01
```

## Unplanned failover (primary lost)
```powershell
# replica host
Get-VMSnapshot -VMName APP01 -SnapshotType Replica    # list recovery points
Start-VMFailover -VMName APP01 -VMRecoverySnapshot (Get-VMSnapshot -VMName APP01 -SnapshotType Replica | Select-Object -Last 1)
Start-VM -Name APP01
Complete-VMFailover -VMName APP01                # commit the chosen point
```
- The latest recovery point is used by default; pipe `Get-VMSnapshot` into `Start-VMFailover` for an earlier one.
- Choose an application-consistent (VSS) point for databases; data loss depends on the point chosen.
- `Complete-VMFailover` commits the chosen point and removes all other recovery points; failover cannot be cancelled
  after that, so try other points before running it.
- Reverse replication back to the original primary with `Set-VMReplication -Reverse` once it returns, as the
  documentation describes after completing the failover.

## Network on the DR side
Attach the replica VM to a switch if needed. For Windows guests set failover TCP/IP per VM, run on the host with the
replica VM:
```powershell
Set-VMNetworkAdapterFailoverConfiguration -VMName APP01 -IPv4Address 10.50.0.20 -IPv4SubnetMask 255.255.255.0 `
  -IPv4DefaultGateway 10.50.0.1 -IPv4PreferredDNSServer 10.50.0.10
```
Update DNS records for the new address as part of the runbook.

## Verify
- [ ] Test failover performed regularly and recorded; RPO met (Measure-VMReplication LReplTime within frequency).

## Checked

2026-10-26 against the Windows Server docs (replication-failover; repository last commit 2026-10-23) and the Hyper-V module reference for Start-VMFailover and Complete-VMFailover (Windows Server 2025): command sequences for test, planned and unplanned failover, -Prepare, -VMRecoverySnapshot, -Reverse, test VM naming, no network by default, one test failover at a time, Complete-VMFailover removing other recovery points, Set-VMNetworkAdapterFailoverConfiguration IPv4 parameters. Removed the -TestReplicaSwitchName example (not in the failover docs) and the claims about Integration Services IP injection and DNS TTLs.

Method: documentation only; no commands were run.
