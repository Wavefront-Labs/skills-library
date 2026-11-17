---
id: computing-software.systems-network-administration.virtualisation.hyper-v-nat-networking-for-labs
name: hyper-v-nat-networking-for-labs
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, hyper-v-nat, new-netnat, nat, internal-switch, port-forwarding, lab-network, windows-server]
level: practitioner
status: docs-checked
description: "Build a Hyper-V NAT network with an internal switch and New-NetNat, add static port mappings, and work around the one-NAT-per-host and no-DHCP limits."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/setup-nat-network
  - https://learn.microsoft.com/en-us/powershell/module/netnat/new-netnat
  - https://learn.microsoft.com/en-us/powershell/module/netnat/add-netnatstaticmapping
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hyper-V NAT networking for labs

**Goal:** give lab VMs outbound internet through the host's connection without touching the physical network.

## Build it
```powershell
New-VMSwitch -Name 'NATSwitch' -SwitchType Internal
New-NetIPAddress -IPAddress 192.168.100.1 -PrefixLength 24 -InterfaceAlias 'vEthernet (NATSwitch)'
New-NetNat -Name 'LabNAT' -InternalIPInterfaceAddressPrefix 192.168.100.0/24
Connect-VMNetworkAdapter -VMName lab01 -SwitchName 'NATSwitch'
```
Guests need an IP address in the NAT subnet with the NAT gateway address (192.168.100.1 here) as default gateway, and a DNS server.

## Inbound port forwarding
```powershell
Add-NetNatStaticMapping -NatName 'LabNAT' -Protocol TCP -ExternalIPAddress 0.0.0.0 `
  -ExternalPort 8080 -InternalIPAddress 192.168.100.10 -InternalPort 80
Get-NetNatStaticMapping
```

## Limits and fixes
- **One NAT network per host.** Windows NAT supports one internal NAT subnet prefix; creating several puts the system in an unknown state. List with `Get-NetNat`; applications such as Docker or Windows containers can create a NAT of their own, so share one prefix large enough for all (see the shared-NAT section of the setup page).
- Remove stray NATs with `Remove-NetNat`.

## Gotchas
- Static port mappings let several VMs host applications that need identical internal ports by mapping them to unique external ports.

## Verify
`Get-NetNat` shows a single NAT with the expected prefix, `Get-NetNatStaticMapping` lists the mapping, and the VM can reach external addresses.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: the internal-switch plus New-NetNat procedure, the one-NAT-per-host limit and the unknown-state warning, the shared-prefix guidance for Docker and containers, port mapping purpose, and the Add-NetNatStaticMapping parameters (NatName, Protocol, ExternalIPAddress, ExternalPort, InternalIPAddress, InternalPort), New-NetIPAddress -InterfaceAlias. Removed because no documentation page confirmed them: the no-DHCP statement, the overlap warning, the Default Switch remarks and the firewall remark.
Method: documentation only; no commands were run.
