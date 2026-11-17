---
id: computing-software.systems-network-administration.virtualisation.hyper-v-scalability-limits-and-sizing
name: hyper-v-scalability-limits-and-sizing
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, hyper-v-limits, scalability, capacity-planning, host-sizing, vm-maximums, windows-server]
level: practitioner
status: docs-checked
description: "Size Hyper-V hosts and VMs against the published maximums (vCPU, memory, disks, cluster nodes) and the practical limits that bite first: NUMA, reserve and failover headroom."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/maximum-scale-limits
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/dynamic-memory
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/configure-non-uniform-memory-access
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Hyper-V scalability limits and sizing

**Goal:** design hosts and VMs that stay well inside the supported maximums.

## Published maximums (Windows Server 2025 unless stated)
- VHDX virtual disk: 64 TB (VHD 2,040 GB). SCSI: 4 controllers, 64 devices each, 256 devices per VM. Gen 1 IDE: 4 devices, and the boot disk must be on IDE in Gen 1.
- Per VM: Windows Server 2025 allows 2,048 virtual processors (Gen 2, PowerShell only) and 240 TB memory; Gen 1 is 64 vCPU and 1 TB. Windows Server 2022 allows 1,024 vCPU and 240 TB (Gen 2). Windows Server 2019 and 2016 allow 240 vCPU and 12 TB (Gen 2). 50 checkpoints, 64 standard network adapters on Gen 2 (2019 and later; 8 on 2016), 4 virtual Fibre Channel adapters.
- Per host: 1,024 running VMs on all supported versions; logical processors 2,048 (2025), 1,024 (2022), 512 (2019 and 2016); memory 4 PB with 5-level paging or 256 TB with 4-level paging (2025 and 2022), 24 TB (2019 and 2016). Hyper-V imposes no virtual-to-logical processor ratio.
- Failover cluster: 64 nodes and 8,000 running VMs per cluster.
- The guest operating system may support less than Hyper-V's maximum; check the OS vendor's limits.

## Related planning facts
- Hyper-V automatically reserves memory for the management OS (and for failover cluster services on a clustered host); do not plan to use every byte of host RAM for VMs.
- Dynamic Memory can be adjusted on a running VM (increase maximum, decrease minimum).
- `Get-VMHostNumaNode` shows the host NUMA topology and `Get-VMHost | FL NumaSpanningEnabled` shows spanning.

## Quick inventory
```powershell
Get-VMHost | Select-Object LogicalProcessorCount, MemoryCapacity
Get-VMHostNumaNode
```

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: the VM, host and cluster maximums for Windows Server 2025, 2022, 2019 and 2016, the absence of a vCPU to logical-processor ratio, automatic management-OS memory reservation, Dynamic Memory runtime changes, and Get-VMHostNumaNode. Removed because no documentation page confirmed them: the 2 GB root reserve, the 4:1 ratio rule of thumb, the N+1 capacity formula, the performance counter name, and the Gen 1 to Gen 2 conversion remark.
Method: documentation only; no commands were run.
