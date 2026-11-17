---
id: computing-software.systems-network-administration.virtualisation.hyper-v-virtual-fibre-channel
name: hyper-v-virtual-fibre-channel
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [virtual-fibre-channel, hyper-v, npiv, san, storage]
level: advanced
status: docs-checked
description: "Give Hyper-V VMs direct Fibre Channel SAN access with virtual FC: NPIV prerequisites, virtual SANs, WWPN set A and B zoning for live migration, and limits."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/virtual-fibre-channel-for-hyper-v
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/add-vmfibrechannelhba
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/new-vmsan
  - https://learn.microsoft.com/en-us/powershell/module/storage/get-initiatorport
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Virtual Fibre Channel

**Goal:** guest clusters and applications that need native FC LUN access inside VMs.

## Prerequisites
- FC HBAs and fabric switches that support **NPIV**, enabled on the HBA and switch ports.
- An HBA driver that supports virtual Fibre Channel, with ports that support NPIV, a maximum transfer size of at least 0.5 MB and data transfers of at least 128 physical pages; guest VMs running Windows Server 2012 or later.
- Virtual Fibre Channel LUNs cannot be used as boot media.

## Create a virtual SAN (per fabric, per host)
```powershell
Get-InitiatorPort | Where ConnectionType -eq 'Fibre Channel' | Select NodeAddress, PortAddress
New-VMSan -Name 'Fabric-A' -HostBusAdapter (Get-InitiatorPort -NodeAddress <wwnn-a>)
New-VMSan -Name 'Fabric-B' -HostBusAdapter (Get-InitiatorPort -NodeAddress <wwnn-b>)
```

## Add vHBAs to the VM
```powershell
Add-VMFibreChannelHba -VMName sqlc1 -SanName 'Fabric-A'
Add-VMFibreChannelHba -VMName sqlc1 -SanName 'Fabric-B'
Get-VMFibreChannelHba -VMName sqlc1 | Select SanName, WorldWidePortNameSetA, WorldWidePortNameSetB
```
Each vHBA has **two WWN sets**. Hyper-V alternates between set A and set B during live migration so Fibre Channel connectivity is kept. Configure zoning and LUN masking for both sets.

## In the guest
Use MPIO inside the VM with a separate copy of MPIO (and the array's DSM) when using several vHBAs. Live migration where the guest uses MPIO does not support ALUA.

## Limits
- Up to four virtual Fibre Channel adapters per VM, each associated with a virtual SAN.
- Boot from virtual Fibre Channel is not supported; keep the OS on a virtual hard disk.

## Verify
The guest's `Get-InitiatorPort` shows the WWPNs; LUNs appear with the expected number of paths; a live migration completes and paths come back on the destination.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: NPIV and HBA requirements, up to four virtual FC adapters per VM, two WWN sets (A and B) alternating during live migration, MPIO inside the VM and the ALUA limitation, FC LUNs cannot be boot media, guest OS Windows Server 2012 or later; New-VMSan -HostBusAdapter, Add-VMFibreChannelHba -VMName -SanName, Get-InitiatorPort -NodeAddress and -ConnectionType. Removed as unconfirmed: host edition requirement, same SAN name on all hosts, powered-off requirement, and checkpoint, backup and Replica limits.

Method: documentation only; no commands were run.
