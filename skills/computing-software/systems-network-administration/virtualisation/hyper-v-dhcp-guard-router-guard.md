---
id: computing-software.systems-network-administration.virtualisation.hyper-v-dhcp-guard-router-guard
name: hyper-v-dhcp-guard-router-guard
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [dhcp-guard, router-guard, mac-address-spoofing, hyper-v-switch, network-security, hyper-v]
level: practitioner
status: docs-checked
description: "Protect Hyper-V tenant networks with DHCP guard, router guard and MAC spoofing settings per VM NIC: what each drops, which VMs need exceptions, and auditing them."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmnetworkadapter
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/virtual-switch
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/enable-nested-virtualization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCP guard, router guard and MAC spoofing

Per-VM network adapter security on the Hyper-V switch (VM Settings → Network Adapter →
Advanced Features).

| Setting | Drops | Turn on for | Leave off for |
|---|---|---|---|
| **DHCP guard** | DHCP messages from a VM claiming to be a DHCP server | every VM that is not an authorised DHCP server | DHCP servers |
| **Router guard** | Router Advertisement and Redirection messages from unauthorised VMs | every VM that is not a router | virtual routers |
| **MAC address spoofing** | when Off, the VM may use only its assigned MAC address | leave Off | nested Hyper-V (MAC spoofing On is the documented nested-networking option) |

## Apply and audit
```powershell
Get-VM | Get-VMNetworkAdapter | Set-VMNetworkAdapter -DhcpGuard On -RouterGuard On
Get-VMNetworkAdapter -VMName fw01 | Set-VMNetworkAdapter -DhcpGuard Off -RouterGuard Off -MacAddressSpoofing On

Get-VM | Get-VMNetworkAdapter | Select VMName, Name, DhcpGuard, RouterGuard, MacAddressSpoofing |
  Where { $_.DhcpGuard -eq 'Off' -or $_.RouterGuard -eq 'Off' -or $_.MacAddressSpoofing -eq 'On' }
```

## Related options
- `-AllowTeaming On`: allow the vNIC to be teamed with other adapters connected to the same virtual switch.
- `-PortMirroring Source|Destination|None`: copies a source adapter's traffic to a destination adapter on the same switch.
- `-IeeePriorityTag On|Off`: trust or reset 802.1p priority values.
- `-StormLimit <n>`: broadcast, multicast and unknown-unicast packets per second the VM may send (0 means no limit).
- Extended port ACLs (`Add-VMNetworkAdapterExtendedAcl`) for per-protocol and stateful filtering.

## Gotchas
- DHCP guard and router guard act on messages sent from the VM's own adapter, so they must be On for the VM that might misbehave; that is why the rule is On everywhere except known servers and routers.
- Router guard drops Redirection messages as well as Router Advertisements.
- Nested virtualization needs MAC spoofing On for the nested VMs' traffic to cross two virtual switches.

## Verify
The audit query above returns only the documented exceptions.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: the semantics and allowed values of DhcpGuard, RouterGuard, MacAddressSpoofing, AllowTeaming, PortMirroring, IeeePriorityTag and StormLimit, and MAC spoofing for nested virtualization. Removed because no documentation page confirmed them: the list of workloads that need MAC spoofing (NLB, containers), the Datacenter edition remark for StormLimit, SCVMM port classifications, and the dnsmasq lab test.
Method: documentation only; no commands were run.
