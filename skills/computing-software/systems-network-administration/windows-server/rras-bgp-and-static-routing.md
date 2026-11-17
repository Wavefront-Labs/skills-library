---
id: computing-software.systems-network-administration.windows-server.rras-bgp-and-static-routing
name: rras-bgp-and-static-routing
category: computing-software
field: systems-network-administration
product: windows-server
tags: [remote-access, rras, rras-bgp, lan-routing, new-netroute]
level: advanced
status: docs-checked
description: "Configure RRAS BGP peering and static routes: Add-BgpRouter, peers, advertised prefixes, route filters and when Windows routing is the wrong tool."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/remoteaccess/add-bgprouter
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-access/bgp/border-gateway-protocol-bgp
  - https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-bgp-overview
  - https://learn.microsoft.com/en-us/powershell/module/nettcpip/new-netroute
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RRAS BGP and static routes

RRAS can run BGP (documented for Windows Server 2016 RAS Gateways) for site-to-site VPN with Azure VPN Gateway or for SDN gateways.
It is a small BGP speaker: fine for a handful of peers and prefixes, not a core router.

## Install
```powershell
Install-WindowsFeature RemoteAccess -IncludeManagementTools
Install-RemoteAccess -VpnType RoutingOnly
```

## BGP router and peers
```powershell
Add-BgpRouter -BgpIdentifier 10.0.0.4 -LocalASN 65010
Add-BgpPeer -Name AzureGW -LocalIPAddress 10.0.0.4 -PeerIPAddress 10.200.255.30 -PeerASN 65515 -OperationMode Mixed -PeeringMode Automatic
Add-BgpCustomRoute -Network 10.0.0.0/16          # advertise
Get-BgpPeer; Get-BgpRouteInformation
```
For Azure: peer IP = the gateway's BGP peer address (shown in the gateway's configuration), and the on-premises ASN must differ from
Azure's (Azure assigns ASN 65515 to a VPN gateway by default and reserves it). Azure only needs a minimum prefix over the tunnel, as small as the /32
of the BGP peer IP, so add a host route to the peer via the demand-dial interface:
```powershell
Add-VpnS2SInterface -Name Azure -Destination <gw-public-ip> -Protocol IKEv2 -AuthenticationMethod PSKOnly -SharedSecret <psk> -IPv4Subnet 10.200.255.30/32:100
```

## Filters
```powershell
Add-BgpRoutingPolicy -Name DenyDefault -PolicyType Deny -MatchPrefix 0.0.0.0/0
Add-BgpRoutingPolicyForPeer -PeerName AzureGW -PolicyName DenyDefault -Direction Ingress
```
Policy types are `Allow`, `Deny` and `ModifyAttribute`; direction is `Ingress` or `Egress`. Never accept a default route from Azure on a server that is also your internet path.

## Static routes (no BGP)
```powershell
New-NetRoute -DestinationPrefix 192.168.50.0/24 -InterfaceAlias 'LAN2' -NextHop 10.0.1.1 -RouteMetric 10
```
`New-NetRoute` saves the route in both the ActiveStore and the PersistentStore by default. For demand-dial interfaces use `Add-VpnS2SInterface -IPv4Subnet '<prefix>:<metric>'`.

## Verify
- [ ] `Get-BgpPeer` State Connected; `Get-BgpRouteInformation` shows learned prefixes; traceroute takes the tunnel.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main, windows-powershell-docs (winserver2025-ps RemoteAccess, NetNat, NetTCPIP), azure-docs vpn-gateway articles, SupportArticles-docs (troubleshoot-always-on-vpn, ms.date 2026-02-12).
Confirmed from the winserver2025-ps RemoteAccess reference (Add-BgpRouter, Add-BgpPeer with OperationMode Mixed/Server and PeeringMode Automatic/Manual, Add-BgpCustomRoute -Network, Add-BgpRoutingPolicy PolicyType and MatchPrefix,
Add-BgpRoutingPolicyForPeer -Direction Ingress/Egress, Add-VpnS2SInterface -IPv4Subnet prefix:metric, Install-RemoteAccess -VpnType RoutingOnly), the anycast DNS page (Install-WindowsFeature RemoteAccess plus the BGP cmdlet sequence),
Azure configure-bgp and vpn-gateway-bgp-overview (ASN 65515 reserved, /32 peer prefix) and the New-NetRoute PolicyStore text.
Replaced the unconfirmed '2012 R2+' version claim.
Method: documentation only; no commands were run.
