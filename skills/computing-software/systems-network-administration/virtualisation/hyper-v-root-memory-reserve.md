---
id: computing-software.systems-network-administration.virtualisation.hyper-v-root-memory-reserve
name: hyper-v-root-memory-reserve
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [root-reserve, memoryreserve, hyper-v-host, dynamic-memory, capacity-planning, hyper-v]
level: advanced
status: gated
description: "Size memory for the Hyper-V parent partition: automatic root reserve, MemoryReserve registry override, NUMA and S2D overheads, and diagnosing VMs that fail to start."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/non-uniform-memory-access
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/configure-non-uniform-memory-access
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/failover-cluster-manage-cluster-shared-volumes
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/manage-hyper-v-scheduler-types
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hyper-V root (parent partition) memory reserve

The host OS needs memory for itself, VM worker processes, the storage stack (CSV cache), drivers and agents. Hyper-V reserves
memory for the root automatically based on installed RAM; VMs cannot use it (gated: unconfirmed, source is paywalled or blocked).

## See what's available
```powershell
Get-VMHost | Select LogicalProcessorCount, MemoryCapacity
Get-VMHostNumaNode | Select NodeId, MemoryAvailable, MemoryTotal
Get-Counter '\Hyper-V Dynamic Memory Balancer(*)\Available Memory'
```
"Not enough memory in the system to start the virtual machine" with free RAM showing in Task Manager can be caused by memory reserved for the host and by NUMA placement (gated: unconfirmed, source is paywalled or blocked); the event ID was removed because it could not be confirmed.

## Override (only with reason)
The MemoryReserve registry value below is not documented in the Windows Server pages checked (gated: unconfirmed, source is paywalled or blocked). The reason is that no current Microsoft page that describes it was found. Registry DWORD in MB, on the host:
```powershell
New-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Virtualization" `
  -Name MemoryReserve -PropertyType DWord -Value 8192 -Force
# reboot required
```
Use to **increase** reserve on hosts running heavy host-side workloads (S2D, backup proxies,
monitoring agents) that page or crash under VM pressure; decreasing below the automatic
value invites host instability.

## Planning rules of thumb
- Plan VM memory below host RAM minus the host's own needs (root reserve, per-VM overhead and CSV block cache); the exact overhead is not confirmed (gated: unconfirmed, source is paywalled or blocked).
- The CSV block cache (`(Get-Cluster).BlockCacheSize`, MB per node, 1 GiB by default on Windows Server 2016 and later) is taken from host RAM; account for it per node.
- Keep NUMA in mind: by default Hyper-V tries to allocate a VM's memory from one NUMA node and may span nodes. With NUMA spanning disabled a VM cannot start if no single node has enough memory or logical cores (`Get-VMHost | Select NumaSpanningEnabled`, `Set-VMHost -NumaSpanningEnabled`).
- Clusters: leave enough to absorb a node failure (N+1); failover attempts fail with the
  same memory errors otherwise.

## Gotchas
- Dynamic Memory VMs with high startup memory need that amount free at boot even if their
  minimum is lower.
- Microsoft recommends not running application workloads in the root partition.

## Verify
Under full VM load the host shows no hard paging (`\Memory\Pages/sec` low), Hyper-V
Dynamic Memory Balancer available memory positive, and a failover test starts all VMs.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: NUMA spanning behaviour and the Get-VMHost NumaSpanningEnabled / Set-VMHost -NumaSpanningEnabled settings, Get-VMHostNumaNode, the CSV block cache default and unit, and the recommendation not to run application workloads in the root partition. Not confirmed, so gated: the automatic root reserve, the MemoryReserve registry value, the host memory event ID and overhead figures; no Microsoft documentation for them was found in the repositories checked.

Method: documentation only; no commands were run.
