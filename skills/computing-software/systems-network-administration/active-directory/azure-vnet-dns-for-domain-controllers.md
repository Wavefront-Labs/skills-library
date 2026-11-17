---
id: computing-software.systems-network-administration.active-directory.azure-vnet-dns-for-domain-controllers
name: azure-vnet-dns-for-domain-controllers
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, azure-domain-controller, azure-vnet-dns-dcs, azure-virtual-network, dns]
level: practitioner
status: docs-checked
description: "Point Azure VNet custom DNS at Azure-hosted DCs safely: ordering, the DCs' own NIC settings, forwarders to 168.63.129.16 and restart requirements."
sources:
  - https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-name-resolution-for-vms-and-role-instances
  - https://learn.microsoft.com/en-us/azure/architecture/example-scenario/identity/adds-extend-domain
  - https://learn.microsoft.com/en-us/azure/virtual-network/manage-virtual-network
  - https://learn.microsoft.com/en-us/powershell/module/dnsserver/set-dnsserverforwarder
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure VNet DNS settings for domain controllers

Domain-joined Azure VMs must resolve AD SRV records, so the VNet must hand out the DCs as DNS servers, not
Azure-provided DNS.

## Order of operations
1. Deploy the DC VMs with **static private IPs** (set on the NIC in Azure, never inside the guest).
2. Promote them while the VNet still uses whichever DNS reaches existing DCs (on-premises DCs over VPN, or
   Azure DNS for the first DC in a new forest).
3. Set VNet custom DNS to the Azure DCs, then on-premises DCs as later entries if wanted:
```powershell
$vnet = Get-AzVirtualNetwork -Name vnet-hub -ResourceGroupName rg-net
$vnet.DhcpOptions.DnsServers = @('10.10.1.4','10.10.1.5')
$vnet | Set-AzVirtualNetwork
```
4. After changing VNet DNS settings, renew the DHCP lease on affected VMs (`ipconfig /renew` on Windows); plan this in a maintenance window.

## The DCs themselves
- Do not edit DNS settings inside the VM (service healing can erase them); set them on the NIC or VNet in Azure.
- A DC that points only to itself, or to itself first, can have a start-up delay: use the loopback address only as
  secondary or tertiary, with another DC (Azure or on-premises) first.
- On each DC's DNS server set a **forwarder to 168.63.129.16** so Azure private DNS zones (Private Link) and Azure
  internal names resolve:
```powershell
Set-DnsServerForwarder -IPAddress 168.63.129.16
```
- If the DCs forward to Azure DNS, raise the Windows DNS forwarding timeout above 4 seconds; otherwise Private DNS zone
  records can resolve to public IPs. Use conditional forwarding to send other virtual networks' suffixes to the right place.

## Gotchas
- If a VPN gateway is used with custom DNS servers on the VNet, Azure's 168.63.129.16 must be in the DNS list to keep
  service undisrupted. A custom DNS setting needs at least one server or Azure-provided DNS is used.
- Apply the custom DNS setting to the DC VNet and to peered VNets whose VMs must resolve the AD domain.
- DNS changes on a VNet with many VMs: update in a maintenance window, then roll restarts.

## Verify
- [ ] From a spoke VM: `nslookup -type=SRV _ldap._tcp.dc._msdcs.corp.example.com` returns the Azure DCs.
- [ ] `Resolve-DnsName <account>.privatelink.blob.core.windows.net` returns a private IP.

## Checked
2026-10-27, against the Learn pages "Name resolution for resources in Azure virtual networks" and "Extend on-premises Active Directory to Azure", "Manage virtual networks" (DhcpOptions.DnsServers) and the Set-DnsServerForwarder cmdlet page. Confirmed: static private IP on the NIC; custom DNS servers at VNet level including peered networks; 168.63.129.16 as the Azure DNS address and forwarder target; VPN gateway caveat; DHCP lease renew after DNS changes; forwarding timeout above four seconds; loopback only as secondary or tertiary; PowerShell DhcpOptions.DnsServers with Set-AzVirtualNetwork; Set-DnsServerForwarder -IPAddress. Removed as unconfirmed: the random-pick claim, restart requirement, and the privatelink conditional-forwarder example. Corrected: 168.63.129.16 may need to stay in the VNet DNS list when a VPN gateway is used.

Method: documentation only; no commands were run.
