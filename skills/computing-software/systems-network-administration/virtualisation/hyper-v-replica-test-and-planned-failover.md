---
id: computing-software.systems-network-administration.virtualisation.hyper-v-replica-test-and-planned-failover
name: hyper-v-replica-test-and-planned-failover
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, hyper-v-replica, replica-test-failover, planned-failover, unplanned-failover, start-vmfailover, reverse-replication, windows-server]
level: advanced
status: docs-checked
description: "Run Hyper-V Replica test failovers, planned failovers with reverse replication, and unplanned failovers to a chosen recovery point, then complete and fail back cleanly."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/replication-failover
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/start-vmfailover
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmnetworkadapter
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmnetworkadapterfailoverconfiguration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V Replica test, planned and unplanned failover

## Test failover (no impact on replication)
On the replica host:
```powershell
Start-VMFailover -VMName app01 -AsTest          # creates 'app01 - Test', disconnected or on test network
Start-VM 'app01 - Test'                          # validate the app
Stop-VMFailover -VMName app01                    # deletes the test VM
```
Set the test network once with `Set-VMNetworkAdapter -VMName app01 -TestReplicaSwitchName 'Isolated'` (the switch parameter belongs to `Set-VMNetworkAdapter`, not `Set-VMNetworkAdapterFailoverConfiguration`). By default the latest recovery point is used.

## Planned failover (no data loss, both sites up)
```powershell
# primary
Stop-VM app01
Start-VMFailover -VMName app01 -Prepare          # sends last changes
# replica
Start-VMFailover -VMName app01
Set-VMReplication -VMName app01 -Reverse         # replicate back towards old primary
Start-VM app01
```

## Unplanned failover (primary lost)
```powershell
Get-VMSnapshot -VMName app01 -SnapshotType Replica          # pick a recovery point if needed
Start-VMFailover -VMName app01 [-VMRecoverySnapshot $point]
Start-VM app01
# check the app, then commit:
Complete-VMFailover -VMName app01
```
`Start-VMFailover` creates a checkpoint on the replica VM and does not start it; start it and test before completing. `Complete-VMFailover` removes the recovery points and merges the checkpoint, so you cannot revert to an earlier point afterwards (export first to keep extra points). Replication health then shows Warning. When the old site returns, reverse replication with `Set-VMReplication -VMName app01 -Reverse -ReplicaServerName <FQDN>`.

## Re-IP
Set the failover IP on the replica VM (supported Windows guests with current integration services and synthetic adapters):
```powershell
Set-VMNetworkAdapterFailoverConfiguration -VMName app01 -IPv4Address 10.20.5.10 -IPv4SubnetMask 255.255.255.0 -IPv4DefaultGateway 10.20.5.1 -IPv4PreferredDNSServer 10.20.0.10
```

## Verify
`Get-VMReplication -VMName app01 | FL VMName, ReplicationMode, ReplicationState` shows the expected mode and state after each step.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: the test, planned and unplanned failover command sequences (-AsTest, Stop-VMFailover, -Prepare, Set-VMReplication -Reverse, Complete-VMFailover), that Complete-VMFailover removes recovery points, and the parameter set of Set-VMNetworkAdapterFailoverConfiguration. Removed because no documentation page confirmed them: the quarterly-test advice.
Method: documentation only; no commands were run.
