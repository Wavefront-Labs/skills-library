---
id: computing-software.systems-network-administration.virtualisation.hyper-v-hot-add-memory-and-network-adapters
name: hyper-v-hot-add-memory-and-network-adapters
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v-hot-add, hyper-v, runtime-memory-resize, hot-add]
level: practitioner
status: docs-checked
description: "Change running Hyper-V VMs without downtime: hot add or remove network adapters, runtime memory resize, SCSI disk hot add, and what still needs a shutdown."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/hyper-v-feature-compatibility-by-generation-and-guest
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/dynamic-memory
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmmemory
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/nested-virtualization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hot add memory and network adapters

**Goal:** know what can change on a running VM without an outage.

## What the documentation supports
| Change | Requirements |
|---|---|
| Hot add or removal of memory | Generation 1 and 2; Windows Server 2016 or Windows 10 guests |
| Hot add or removal of a virtual network adapter | Generation 2; any supported guest |
| Dynamic Memory while running | Increase the maximum memory, decrease the minimum memory |

Nested Hyper-V guests are different: memory cannot be adjusted while Hyper-V runs inside the VM.

## Commands
```powershell
Add-VMNetworkAdapter -VMName app01 -SwitchName vSwitch -Name 'Backup'
Remove-VMNetworkAdapter -VMName app01 -Name 'Backup'
Set-VMMemory -VMName app01 -StartupBytes 16GB          # static memory VM
Set-VMMemory -VMName web01 -MaximumBytes 24GB          # Dynamic Memory VM
```

## Verify
`Get-VM app01 | Select MemoryAssigned, MemoryStartup`; inside the guest the new memory and adapter appear without a restart.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: hot add and removal of memory (Gen 1 and 2, Windows Server 2016 and Windows 10 guests), hot add and removal of network adapters (Gen 2), the Dynamic Memory runtime changes, the nested-guest restriction, and the Set-VMMemory StartupBytes and MaximumBytes parameters. Removed because no documentation page confirmed them: the rows on SCSI disk add, VHDX expansion, vCPU changes, Linux udev rule, MAC and VLAN of hot-added adapters, and application reconfiguration remarks.
Method: documentation only; no commands were run.
