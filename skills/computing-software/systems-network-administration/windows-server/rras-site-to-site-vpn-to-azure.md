---
id: computing-software.systems-network-administration.windows-server.rras-site-to-site-vpn-to-azure
name: rras-site-to-site-vpn-to-azure
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, remote-access, rras, site-to-site-vpn, azure-vpn-gateway, azure-network-adapter, add-vpns2sinterface, ikev2, local-network-gateway, hybrid-networking]
level: practitioner
status: docs-checked
description: "Connect on-prem to Azure with RRAS site-to-site IKEv2 (Add-VpnS2SInterface), the Azure VPN gateway side, and the single-server Azure Network Adapter option."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/remoteaccess/add-vpns2sinterface
  - https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpn-devices
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/azure/use-azure-network-adapter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RRAS site-to-site VPN to Azure

Good for labs, small branches or temporary migration links; production sites usually use a
firewall/router or ExpressRoute.

## Azure side
- VNet with a `GatewaySubnet`, a **route-based VPN gateway** (Microsoft's device list shows Windows Server 2012 RRAS as supported
  for route-based and not compatible for policy-based), a **local network gateway** with the RRAS server's public IP and on-prem
  address prefixes, and a **connection** with a shared key. New gateways need a Standard SKU public IP.

## RRAS side
```powershell
Install-WindowsFeature RemoteAccess -IncludeManagementTools
Install-RemoteAccess -VpnType VpnS2S
Add-VpnS2SInterface -Name 'Azure' -Destination <AZURE_GATEWAY_PUBLIC_IP> -Protocol IKEv2 `
  -AuthenticationMethod PSKOnly -SharedSecret '<SHARED_KEY>' `
  -IPv4Subnet '10.100.0.0/16:100' -Persistent
Connect-VpnS2SInterface -Name 'Azure'
Get-VpnS2SInterface | Select Name,ConnectionState
```
- `IPv4Subnet 'prefix:metric'` adds routes to Azure VNets over the tunnel.
- With a pre-shared key there can be only one active S2S interface per destination IP address.
- The local network gateway needs the RRAS server's public IP; IKE uses UDP 500 and 4500, which must not be blocked.
- Other on-prem hosts need a route to Azure prefixes via the RRAS server (or the RRAS server is their gateway).
- Match IPsec/IKE policy on both sides if you set custom policies (`Set-VpnS2SInterface -CustomPolicy ...` and an Azure connection IPsec policy).

## Azure Network Adapter (single server)
Windows Admin Center can create a **point-to-site** VPN connection from one server to a VNet; it automates configuring the virtual
network gateway and the on-premises VPN client. Use it when only a few servers need Azure access instead of a full site-to-site link.

## Verify
- [ ] Azure portal connection status "Connected"; `Get-VpnS2SInterface` Connected.
- [ ] `Test-NetConnection 10.100.1.4 -Port 3389` from on-prem reaches an Azure VM.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main, windows-powershell-docs (winserver2025-ps RemoteAccess, NetNat, NetTCPIP), azure-docs vpn-gateway articles, SupportArticles-docs (troubleshoot-always-on-vpn, ms.date 2026-02-12).
Confirmed from the Add-VpnS2SInterface reference (parameter is -Persistent, not -PersistentConnection; -Protocol IKEv2, -AuthenticationMethod PSKOnly, -IPv4Subnet prefix:metric, one PSK interface per destination),
Set-VpnS2SInterface -CustomPolicy, Azure vpn-gateway-about-vpn-devices (RRAS row), vpn-gateway-vpn-faq (Standard SKU public IP), and WAC use-azure-network-adapter (point-to-site automation).
Fixed the invalid -PersistentConnection parameter and removed the Routing feature name and the NAT-forwarding sentence.
Method: documentation only; no commands were run.
