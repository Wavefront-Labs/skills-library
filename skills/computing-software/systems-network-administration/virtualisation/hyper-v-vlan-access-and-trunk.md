---
id: computing-software.systems-network-administration.virtualisation.hyper-v-vlan-access-and-trunk
name: hyper-v-vlan-access-and-trunk
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, hyper-v-vlan, set-vmnetworkadaptervlan, vlan, trunk-mode, access-mode, 802-1q, windows-server]
level: practitioner
status: docs-checked
description: "Tag Hyper-V VM and host vNIC traffic with Set-VMNetworkAdapterVlan in access, trunk or untagged mode, and match it to the physical switch port configuration."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmnetworkadaptervlan
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/deploy/configure-virtual-local-area-networks-for-hyper-v
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hyper-V VLAN access and trunk modes

**Goal:** put each VM (and host vNIC) on the right 802.1Q VLAN without guest-side tagging, or pass a trunk to a guest router/firewall.

## Physical prerequisite
Hyper-V needs a physical adapter, driver and switch that support 802.1q VLAN tagging, and the physical switch port must carry the VLAN IDs you use.

## Access mode (most VMs)
```powershell
Set-VMNetworkAdapterVlan -VMName web01 -Access -VlanId 20
```
Access mode configures an untagged virtual port with the VLAN ID (port-based VLAN); the guest sees untagged frames.

## Trunk mode (guest firewalls, routers, nested hosts)
```powershell
Set-VMNetworkAdapterVlan -VMName fw01 -VMNetworkAdapterName 'LAN' -Trunk -AllowedVlanIdList '10,20,30-39' -NativeVlanId 10
```
Trunk mode passes all allowed VLAN tags to the VM adapter; traffic on the native VLAN ID is passed untagged. `-AllowedVlanIdList` and `-NativeVlanId` must be given with `-Trunk`.

## Host management vNIC
```powershell
Add-VMNetworkAdapter -ManagementOS -Name 'Mgmt' -SwitchName 'SETswitch'
Set-VMNetworkAdapterVlan -ManagementOS -VMNetworkAdapterName 'Mgmt' -Access -VlanId 10
```

## Reset and audit
```powershell
Set-VMNetworkAdapterVlan -VMName web01 -Untagged
Get-VMNetworkAdapterVlan -VMName *
Get-VMNetworkAdapterVlan -ManagementOS
```

## Gotchas
- For a VM that needs more than one VLAN, either add more virtual network adapters with their own VLAN IDs or use trunk mode.
- `-ManagementOS` configures host virtual adapters; `-Untagged` removes VLAN tagging.

## Verify
From the VM, reach the VLAN gateway; `Get-VMNetworkAdapterVlan -VMName <name>` shows the configured mode.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: Access, Trunk and Untagged semantics, the AllowedVlanIdList and NativeVlanId requirement to be used with Trunk, the 802.1q prerequisites, and the add-adapters-or-use-trunk guidance. Removed because no documentation page confirmed them: the double-tagging claim, the physical-NIC advanced-property advice, the live-migration VLAN rule, and the switch MAC-table check.
Method: documentation only; no commands were run.
