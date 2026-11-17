---
id: computing-software.systems-network-administration.virtualisation.hyper-v-quick-migration-vs-live-migration
name: hyper-v-quick-migration-vs-live-migration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v-quick-migration, quick-migration, live-migration, hyper-v, failover-cluster]
level: practitioner
status: docs-checked
description: "Use quick migration versus live migration for clustered Hyper-V VMs: how each works, downtime, drain behaviour by priority, and when quick migration is the fallback."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/move-clustervirtualmachinerole
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Quick migration vs live migration in clusters

**Goal:** move clustered VMs with the right method and know what downtime each causes.

## Methods (`Move-ClusterVirtualMachineRole -MigrationType`)
| Type | Meaning in Microsoft's reference |
|---|---|
| `Live` | Transparently migrates the VM without a dropped network connection or perceived downtime |
| `Quick` | Rapidly migrates a running VM with minimal downtime |
| `Shutdown` | Orderly guest shutdown, then migrates the VM |
| `ShutdownForce` | Shuts the guest down without waiting for slow processes, then migrates |
| `TurnOff` | Turns the VM off without shutting down the OS (like pulling power; data loss possible) |

```powershell
Move-ClusterVirtualMachineRole -Name app01 -Node hv02 -MigrationType Live
Move-ClusterVirtualMachineRole -Name app01 -Node hv02 -MigrationType Quick
Move-ClusterVirtualMachineRole -Name app01 -Node hv02 -MigrationType Shutdown
```
The reference describes the cmdlet as the live migration command; for a quick migration it says to use `Move-ClusterGroup` after setting the **OfflineAction** parameter of the VM resource to save state (value 1) with `Get-ClusterResource` and `Set-ClusterParameter`. The cmdlet cannot run remotely without CredSSP authentication on the server.

## Choosing
- Live migrate production VMs; use quick migration only where a short pause is acceptable.
- A quick migration saves and restores the VM's memory, so its pause grows with RAM size and storage speed (test it before relying on it).

## Verify
Cluster events (*Microsoft-Windows-FailoverClustering/Operational*) and the VM's network connectivity during the move show which method was used and how long the pause lasted.

## Checked

Checked 2026-10-26 against the Windows Server 2025 `Move-ClusterVirtualMachineRole` reference (accepted `-MigrationType` values TurnOff, Quick, Shutdown, ShutdownForce, Live, with their descriptions; the quick migration note and CredSSP remark). Removed as undocumented: downtime figures, node-drain behaviour with `MoveTypeThreshold` and VM priority values 3000/2000/1000, the list of reasons live migration falls back to quick, saved-state and processor-family remarks, and `.vmrs`/`.bin` sizing guidance.

Method: documentation only; no commands were run.
