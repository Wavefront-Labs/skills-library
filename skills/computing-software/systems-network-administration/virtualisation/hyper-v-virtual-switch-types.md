---
id: computing-software.systems-network-administration.virtualisation.hyper-v-virtual-switch-types
name: hyper-v-virtual-switch-types
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, hyper-v-switch, external-switch, internal-switch, private-switch, new-vmswitch, allowmanagementos, vswitch, windows-server]
level: practitioner
status: docs-checked
description: "Create Hyper-V external, internal and private virtual switches with New-VMSwitch, decide when the host shares the NIC, and avoid cutting off remote management."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/get-started/create-a-virtual-switch-for-hyper-v-virtual-machines
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/plan-hyper-v-networking-in-windows-server
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/new-vmswitch
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmswitch
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V external, internal and private switches

**Goal:** give VMs the right reach: physical network, host-only, or VM-only.

| Type | Reaches | Use |
|---|---|---|
| External | A wired physical network, by binding to a physical network adapter | VM traffic to the physical network |
| Internal | VMs on the host and between the host and the VMs | Labs, NAT, host-to-VM tools |
| Private | VMs on the host only; no networking between host and VMs | Isolated test segments |

## Create
```powershell
# External: -NetAdapterName (or -NetAdapterInterfaceDescription) implies the External type
New-VMSwitch -Name 'VM-External' -NetAdapterName 'NIC2' -AllowManagementOS $false   # host does not share the NIC
New-VMSwitch -Name 'VM-Shared' -NetAdapterName 'NIC1' -AllowManagementOS $true      # host shares the NIC
New-VMSwitch -Name 'Lab-Internal' -SwitchType Internal
New-VMSwitch -Name 'Isolated' -SwitchType Private
Connect-VMNetworkAdapter -VMName web01 -SwitchName 'VM-External'
```

## Converting between types
```powershell
Set-VMSwitch -Name 'Lab-Internal' -NetAdapterName 'NIC3'      # internal -> external
Set-VMSwitch -Name 'VM-External' -SwitchType Private           # external -> private
```

## Gotchas
- Creating an external switch can disrupt network connectivity (Hyper-V Manager warns about this); `AllowManagementOS` controls whether the management OS can use the bound NIC.
- `-SwitchType` on `New-VMSwitch` accepts only Internal or Private; the External type comes from specifying a physical adapter.
- For a teamed uplink, `New-VMSwitch -NetAdapterName NIC1,NIC2 -EnableEmbeddedTeaming $true` enables Switch Embedded Teaming.

## Verify
`Get-VMSwitch | Format-Table Name, SwitchType, NetAdapterInterfaceDescription, AllowManagementOS` and test connectivity from a VM on each external switch.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: the external, internal and private definitions, how New-VMSwitch infers the type, the Internal/Private values of -SwitchType, Set-VMSwitch conversion values (Private, Internal, External), AllowManagementOS and EnableEmbeddedTeaming parameters. Removed because no documentation page confirmed them: the host-IP-move and static-IP claims, the LBFO comparison, and the cluster switch-name rule.
Method: documentation only; no commands were run.
