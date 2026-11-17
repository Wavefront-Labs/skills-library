---
id: computing-software.systems-network-administration.virtualisation.hyper-v-vm-processor-and-numa-settings
name: hyper-v-vm-processor-and-numa-settings
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vm-processor-settings, vm-numa, hyper-v-vm, numa-spanning, core-scheduler, hyper-v]
level: advanced
status: docs-checked
description: "Tune Hyper-V VM processors: vCPU count, reserve, limit and relative weight, virtual NUMA topology per node, host NUMA spanning, and SMT exposure with the core scheduler."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmprocessor
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/about-hyper-v-scheduler-type-selection
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/manage-hyper-v-scheduler-types
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/non-uniform-memory-access
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/manage/configure-non-uniform-memory-access
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V VM processor and NUMA settings

## vCPU and resource control
```powershell
Set-VMProcessor -VMName sql01 -Count 16 -Reserve 25 -Maximum 100 -RelativeWeight 200
Get-VMProcessor -VMName sql01 | Format-List *
```
- **Reserve**: percentage of processor resources reserved for the VM (0 to 100).
- **Maximum**: the maximum percentage of resources available to the VM processor (0 to 100).
- **RelativeWeight**: priority for processor time relative to other VMs (1 to 10000).

## SMT and the core scheduler
The hypervisor uses the **core scheduler** by default beginning with Windows Server 2019; on Windows Server 2016 the default is the classic scheduler and the core scheduler is optional. The core scheduler schedules a VM's virtual processors on sibling SMT threads of a core, which isolates guests from each other. Expose SMT to the guest with `HwThreadCountPerCore`:
```powershell
Set-VMProcessor -VMName sql01 -HwThreadCountPerCore 0     # 0 = inherit the host's threads per core (not supported on Windows Server 2016)
```
New VMs on Windows Server 2019 (VM version 9.0) inherit the host's SMT setting; VMs created on Windows Server 2016 default to `HwThreadCountPerCore` 1. The scheduler is set with `bcdedit /set hypervisorschedulertype <type>` and takes effect after a reboot. To see which one is running, look in the system log for the most recent hypervisor launch event with ID 2.

## Virtual NUMA
By default a VM uses the topology of the physical host.
```powershell
Get-VMHostNumaNode
Get-VMProcessor -VMName sql01 | Select MaximumCountPerNumaNode, MaximumCountPerNumaSocket
Get-VMMemory   -VMName sql01 | Select MaximumAmountPerNumaNodeBytes
Set-VMProcessor -VMName sql01 -MaximumCountPerNumaNode 12      # shut the VM down first
```
In Hyper-V Manager (Processor > NUMA), **Use Hardware Topology** resets the values to the defaults; do this after moving a VM to hosts with different CPUs.

## NUMA spanning (host-wide)
```powershell
Get-VMHost | Format-List NumaSpanningEnabled
Set-VMHost -NumaSpanningEnabled $false      # shut down VMs first, then Restart-Service vmms (or reboot the host)
```
Without NUMA spanning a VM can only use as many logical cores as one NUMA node has (a 24-core VM will not start on a 16-core node). Starting with Windows Server 2025 and Windows 11 24H2, a VM with more virtual cores than a node has physical cores must be run with NUMA spanning configured on both host and VM; benchmark your workload to decide. The setting only applies to hosts with multiple NUMA nodes.

## Gotchas
- You cannot use virtual NUMA and Dynamic Memory together: a VM with Dynamic Memory effectively has one virtual NUMA node and no NUMA topology. Use static memory for NUMA-aware workloads.
- `Set-VMProcessor -CompatibilityForMigrationEnabled $true` limits the virtual processor's features so the VM can migrate between hosts with different processors.

## Verify
`Get-VMProcessor` and `Get-VMMemory` show the intended values, the guest reports the expected NUMA nodes and SMT threads, and the VM starts on every host it must run on.

## Checked

Checked 2026-10-26 against the Windows Server 2025 `Set-VMProcessor` reference and MicrosoftDocs/windowsserverdocs (hypervisor scheduler type selection, manage scheduler types, NUMA in Hyper-V, configure NUMA; latest commit 2026-10-23). Confirmed: Reserve and Maximum range 0-100, RelativeWeight 1-10000, `HwThreadCountPerCore` 0 behaviour and the Windows Server 2016 limitation, core scheduler default from Windows Server 2019, scheduler type via `bcdedit /set hypervisorschedulertype`, hypervisor event ID 2, default host topology, NUMA spanning commands and vmms restart, Windows Server 2025 spanning change, Dynamic Memory and vNUMA exclusion. Removed as undocumented: the default weight of 100, the admission-control claim for Reserve, the `bcdedit /enum` check, `coreinfo` and performance-counter checks, and the claim that "2" is valid on version 8.0+ configurations.

Method: documentation only; no commands were run.
