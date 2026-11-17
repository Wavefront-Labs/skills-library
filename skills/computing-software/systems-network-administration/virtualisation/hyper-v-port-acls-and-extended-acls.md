---
id: computing-software.systems-network-administration.virtualisation.hyper-v-port-acls-and-extended-acls
name: hyper-v-port-acls-and-extended-acls
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmnetworkadapteracl, extended-port-acl, hyper-v, firewall, networking]
level: advanced
status: docs-checked
description: "Filter VM traffic at the Hyper-V switch port with basic and extended port ACLs: IP/MAC rules, stateful port rules, weights, metering and limits."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/add-vmnetworkadapteracl
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/create-security-policies-extended-port-access-control-lists
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/add-vmnetworkadapterextendedacl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Port ACLs and extended port ACLs

**Goal:** enforce network isolation at the virtual switch, independent of the guest firewall.

## Basic port ACLs (IP or MAC, no ports)
```powershell
Add-VMNetworkAdapterAcl -VMName web01 -RemoteIPAddress 10.20.0.0/16 -Direction Both -Action Deny
Add-VMNetworkAdapterAcl -VMName web01 -RemoteIPAddress 10.20.5.10 -Direction Both -Action Allow
Add-VMNetworkAdapterAcl -VMName web01 -RemoteIPAddress 0.0.0.0/0 -Direction Both -Action Meter
Get-VMNetworkAdapterAcl -VMName web01
```
The longest-matching address entry decides which rule applies to a packet. `Meter` ACLs must be IP-based and count traffic.

## Extended port ACLs (ports, protocols, stateful)
```powershell
# Allow inbound HTTPS, stateful so replies are allowed
Add-VMNetworkAdapterExtendedAcl -VMName web01 -Action Allow -Direction Inbound -LocalPort 443 -Protocol TCP -Weight 100 -Stateful $true
# Allow outbound DNS
Add-VMNetworkAdapterExtendedAcl -VMName web01 -Action Allow -Direction Outbound -RemotePort 53 -Protocol UDP -Weight 90
# Deny everything else
Add-VMNetworkAdapterExtendedAcl -VMName web01 -Action Deny -Direction Inbound -Weight 1
Add-VMNetworkAdapterExtendedAcl -VMName web01 -Action Deny -Direction Outbound -Weight 1
Get-VMNetworkAdapterExtendedAcl -VMName web01 | Sort Weight -Descending
```
Rules with a higher **weight** are processed first. A stateful rule filters on source and destination IP, protocol and source and destination port (`-Stateful`, `-IdleSessionTimeout`). Extended ACLs were introduced in Windows Server 2016; a `-VMNetworkAdapterName` limits a rule to one adapter, otherwise it applies to all of the VM's adapters.

## Gotchas
- Allow the infrastructure flows the VM needs (for example DHCP on UDP 67 and 68, DNS) before the catch-all deny; the extended-ACL page shows DHCP rules for this.
- A rule created without `-VMNetworkAdapterName` is added to every adapter of the named VM.

## Verify
Test from allowed and denied sources (`Test-NetConnection web01 -Port 443`); list effective rules sorted by weight.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: Allow/Deny/Meter actions, longest-match rule for IP ACLs, metering ACLs being IP-based, extended-ACL parameters (Weight, Stateful, IdleSessionTimeout, Protocol, ports), weight ordering, and per-adapter scoping. Removed because no documentation page confirmed them: the claims that ACLs move with live migration, the SDN Network Controller interaction, and the multi-NIC remark.
Method: documentation only; no commands were run.
