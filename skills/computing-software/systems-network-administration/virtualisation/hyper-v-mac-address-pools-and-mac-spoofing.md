---
id: computing-software.systems-network-administration.virtualisation.hyper-v-mac-address-pools-and-mac-spoofing
name: hyper-v-mac-address-pools-and-mac-spoofing
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v-mac-address-pool, mac-spoofing, hyper-v, networking]
level: practitioner
status: docs-checked
description: "Prevent duplicate MAC addresses across Hyper-V hosts by setting MAC pools, use static MACs where needed, and enable MAC spoofing only for NLB, nesting or containers."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmhost
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmnetworkadapter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MAC address pools and MAC spoofing

**Goal:** no MAC collisions between hosts, and spoofing allowed only where a workload requires it.

## The default pool problem
Each host has a range of MAC addresses it can assign to VMs that use dynamic MAC addresses (`Set-VMHost -MacAddressMinimum/-MacAddressMaximum` set that range). If two hosts end up with overlapping ranges they can hand out the same address, giving duplicate MACs on the network.

## Set unique pools
```powershell
Get-VMHost | Select Name, MacAddressMinimum, MacAddressMaximum
Set-VMHost -MacAddressMinimum 00155D1E0100 -MacAddressMaximum 00155D1E01FF    # hv01
Set-VMHost -MacAddressMinimum 00155D1E0200 -MacAddressMaximum 00155D1E02FF    # hv02
```
Keep a register of ranges per host.

## Dynamic vs static MAC
- Dynamic MACs come from the host's range; keep ranges that never overlap between hosts.
- Use static MACs for licensing-bound software, DHCP reservations and appliances:
```powershell
Set-VMNetworkAdapter -VMName lic01 -StaticMacAddress 00155D1EAA01
```

## MAC spoofing
Off by default: with `Off` a VM may use only the MAC address assigned to it, with `On` it may change the source MAC in outgoing packets. Turn it on only for VMs that must send frames with other MACs (for example NLB in unicast mode, nested virtualization or network appliances).
```powershell
Set-VMNetworkAdapter -VMName nested01 -MacAddressSpoofing On
Get-VMNetworkAdapter -VMName * | Where MacAddressSpoofing -eq 'On' | Select VMName, Name
```

## Verify
`Get-VMNetworkAdapter -All | Group MacAddress | Where Count -gt 1` returns nothing across all hosts (run it per host with `-ComputerName`, then compare the results).

## Checked

Checked 2026-10-26 against the Windows Server 2025 Hyper-V cmdlet references (`Set-VMHost -MacAddressMinimum/-MacAddressMaximum`, `Set-VMNetworkAdapter -StaticMacAddress/-MacAddressSpoofing`, with its documented On/Off meaning). Removed as undocumented: the 00-15-5D-XX-YY derivation from the host IP address, the claim that dynamic MACs persist until restart and can be reissued, and the SCVMM global pool remark. The nested virtualization, NLB and appliance examples are conventional uses of spoofing rather than quoted from the cmdlet page.

Method: documentation only; no commands were run.
