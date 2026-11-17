---
id: computing-software.systems-network-administration.virtualisation.hyper-v-checkpoint-policy-for-dcs-and-databases
name: hyper-v-checkpoint-policy-for-dcs-and-databases
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, checkpoint-policy, automatic-checkpoints, domain-controller, vm-generation-id, usn-rollback, sql-server, windows-server]
level: practitioner
status: docs-checked
description: "Set Hyper-V checkpoint policy: disable checkpoints and automatic checkpoints on domain controllers, databases and clustered or replicated workloads, and enforce it fleet-wide."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/virtualized-domain-controller-architecture
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/virtualized-domain-controllers-hyper-v
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/checkpoints
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Checkpoint policy for DCs and databases

**Goal:** prevent checkpoint reverts that corrupt directory replication or transactional data, and stop forgotten checkpoints filling storage.

## Who should not be checkpointed
- **Domain controllers.** Microsoft's virtualized DC guidance says not to take or use snapshots of virtual DCs and to use a supported backup instead: a system-state backup restored with a backup application, with Windows Server Backup in the guest recommended. On a hypervisor that exposes VM-Generation ID (Windows Server 2012 or later DC), a snapshot restore makes the DC invalidate its local RID pool and set a new invocation ID, which guards against USN rollback, but it is a safeguard, not a backup method.
- **Systems that replicate data between nodes** (the checkpoints page names Active Directory) can suffer data consistency problems from standard checkpoints; treat databases with replication or log-shipping partners the same way unless the vendor documents otherwise.

## Enforce
```powershell
Set-VM -Name dc01, dc02 -CheckpointType Disabled
Get-VM | Set-VM -AutomaticCheckpointsEnabled $false
Get-VM | Select-Object Name, CheckpointType, AutomaticCheckpointsEnabled
```
`-CheckpointType` accepts Disabled, Standard, Production and ProductionOnly. Production checkpoints use VSS (or file-system freeze on Linux) and take no memory snapshot.

## Find forgotten checkpoints
```powershell
Get-VM | Get-VMSnapshot | Where-Object CreationTime -lt (Get-Date).AddDays(-3) |
  Select-Object VMName, Name, CreationTime
```
Run on a schedule and alert. Pick the age threshold (3 days here) as a local policy.

## Allowed use
Short-lived production checkpoints before a change on stateless or single-instance servers, deleted within the change window.

## Verify
Fleet report shows `CheckpointType = Disabled` on every DC and database VM, and the stale-checkpoint report is empty.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: VM-Generation ID safeguards (RID pool invalidated, new invocation ID after a snapshot restore) in the virtual DC architecture page; the guidance not to take or use snapshots of virtual DCs and to back them up with system-state backups in the virtualized DC page; checkpoints page warning that standard checkpoints can cause consistency problems for systems that replicate between nodes; Set-VM accepts -CheckpointType Disabled/Standard/Production/ProductionOnly and -AutomaticCheckpointsEnabled. Removed as unconfirmed: guest cluster node and Exchange DAG guidance, the client-Hyper-V automatic checkpoint default and the 72 hour threshold (now a local choice).

Method: documentation only; no commands were run.
