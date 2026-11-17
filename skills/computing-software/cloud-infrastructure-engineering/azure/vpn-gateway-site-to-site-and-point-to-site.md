---
id: computing-software.cloud-infrastructure-engineering.azure.vpn-gateway-site-to-site-and-point-to-site
name: vpn-gateway-site-to-site-and-point-to-site
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vpn-gateway, site-to-site, point-to-site, ikev2, ipsec-policy, bgp, active-active, gateway-sku, local-network-gateway, openvpn, entra-authentication, gateway-transit, vpn-diagnostics]
level: practitioner
status: docs-checked
description: "VPN Gateway basics: SKUs and limits, S2S with BGP and custom IPsec policy, P2S with OpenVPN and Entra ID, gateway transit, BGP rules, diagnostic logs and metrics."
sources: ["https://learn.microsoft.com/en-us/azure/vpn-gateway/about-gateway-skus", "https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-vpn-faq", "https://learn.microsoft.com/en-us/azure/vpn-gateway/ipsec-ike-policy-howto", "https://learn.microsoft.com/en-us/azure/vpn-gateway/openvpn-azure-ad-tenant", "https://learn.microsoft.com/en-us/azure/vpn-gateway/monitor-vpn-gateway-reference", "https://learn.microsoft.com/en-us/cli/azure/network/vnet-gateway", "https://learn.microsoft.com/en-us/cli/azure/network/local-gateway", "https://learn.microsoft.com/en-us/cli/azure/network/vpn-connection"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VPN Gateway: S2S with BGP, P2S with Entra ID, limits and diagnostics

**Goal:** hybrid connectivity with the right SKU, BGP-learned routes and a diagnosable P2S/S2S setup.

## 1. Gateway
- Gateway subnet must be named `GatewaySubnet`; no VMs or anything else in it. /29 is the minimum, /27 or larger is recommended.
- A new gateway must use a Standard SKU public IP (static). Active-active has two instances, each with its own public IP.
```bash
az network vnet-gateway create -g rg-hub -n vgw-hub --vnet vnet-hub --gateway-type Vpn --vpn-type RouteBased --sku VpnGw2AZ \
  --vpn-gateway-generation Generation2 --public-ip-addresses pip-vpn-1 pip-vpn-2 --asn 65515 --no-wait
```
- SKU page: use the AZ (zone-redundant) SKUs for new gateways; non-AZ VpnGw1-5 are slated for migration and shouldn't be used for new ones; Standard and HighPerformance are legacy. Basic is for dev-test only: 10 S2S tunnels, no BGP, no RADIUS, no IKEv2 or OpenVPN for P2S, no IPv6.
- Limits (non-Basic): S2S/VNet-to-VNet tunnels 30 (VpnGw4/5 up to 100; for more than 100 use Virtual WAN); P2S SSTP 128 on every SKU, separate from IKEv2/OpenVPN limits of 250 (VpnGw1AZ), 500 (2AZ), 1000 (3AZ), 5000 (4AZ), 10000 (5AZ). Aggregate throughput benchmarks run from 650 Mbps (Gen1 VpnGw1AZ) to 10 Gbps (Gen2 VpnGw5AZ), vary by generation and aren't guaranteed. Many P2S connections can hurt S2S.
- Custom IPsec/IKE policy, BGP, active-active and ExpressRoute/VPN coexistence are available on all SKUs except Basic.
- The default ASN is 65515 whether or not BGP is enabled. Azure-reserved ASNs: public 8074, 8075, 12076; private 65515, 65517, 65518, 65519, 65520.

## 2. Site-to-site with BGP
```bash
az network local-gateway create -g rg-hub -n lng-dc1 --gateway-ip-address 198.51.100.10 --asn 65010 --bgp-peering-address 10.255.0.1
az network vpn-connection create -g rg-hub -n cn-dc1 --vnet-gateway1 vgw-hub --local-gateway2 lng-dc1 --shared-key <key> --enable-bgp
az network vpn-connection ipsec-policy add -g rg-hub --connection-name cn-dc1 --ike-encryption AES256 --ike-integrity SHA384 --dh-group DHGroup14 \
  --ipsec-encryption GCMAES256 --ipsec-integrity GCMAES256 --pfs-group PFS2048 --sa-lifetime 27000 --sa-max-size 102400000
az network vnet-gateway list-bgp-peer-status -g rg-hub -n vgw-hub
az network vnet-gateway list-learned-routes -g rg-hub -n vgw-hub
az network vnet-gateway list-advertised-routes -g rg-hub -n vgw-hub --peer <bgp-peer-ip>
```
The 10.255.0.1 peer IP is a placeholder. For custom policy rules see the on-premises device skill. Without BGP, give the local gateway `--local-address-prefixes`.
- BGP rules (FAQ): the on-premises BGP peer address can't be the VPN device's public IP or in the gateway VNet address space; use another address such as a loopback. If it's an APIPA address (169.254.x.x) you must also specify one or more Azure APIPA BGP addresses on the gateway and the local network gateway. Azure adds a host route to the peer over the tunnel, so don't put a /32 for it in the local network gateway address space.
- Azure advertises: VNet prefixes, each local network gateway's prefixes, and routes learned from other BGP sessions (not the default route or routes overlapping a VNet prefix). Up to 4,000 prefixes can be advertised to Azure; the BGP session drops above that.
- Advertising 0.0.0.0/0 to Azure forces all VNet egress to on-premises (and stops direct internet-initiated RDP/SSH to VMs).
- With gateway transit enabled you can't advertise exact VNet (or peered VNet) prefixes, only a superset (10.0.0.0/8 for a 10.0.0.0/16 VNet).
- Active-active: each instance has its own tunnel; flows may be asymmetric and Azure doesn't guarantee symmetric routing. If your device needs symmetry, adjust routing or use active-standby.
- Overlapping on-premises and VNet ranges are not allowed; use the NAT skill.

## 3. Spokes
For P2S traffic to reach a peered VNet: the VNet with the gateway needs Allow gateway transit and the peered VNet without a gateway needs Use remote gateways (FAQ, P2S section). The peering troubleshooting skill covers peering states.

## 4. Point-to-site (Entra ID, OpenVPN)
```bash
az network vnet-gateway update -g rg-hub -n vgw-hub --address-prefixes 172.16.201.0/24 --client-protocol OpenVPN \
  --aad-tenant https://login.microsoftonline.com/<tenant-id> --aad-audience <audience> --aad-issuer https://sts.windows.net/<tenant-id>/
```
- Entra ID authentication is OpenVPN only and needs the Azure VPN Client; not on Basic SKU. In the portal use Point-to-site configuration, then Download VPN client for the zip containing `azurevpnconfig.xml`.
- Tenant value has no trailing backslash; Issuer must keep the trailing slash or the connection may fail.
- The Audience for the manually registered Azure VPN app in the Azure public cloud is `41b23e61-6c1e-4545-b367-cd054e0ed4b4` (admin consent by a Cloud Application Administrator first). Manually registered clients retire on 31 March 2028 in the public cloud (2029 in Government and 21Vianet); the page recommends the Microsoft-registered configuration article instead, which was not read.
- Protocols: SSTP and OpenVPN use TCP 443; IKEv2 uses outbound UDP 500 and 4500 plus IP protocol 50 and may not pass firewalls. P2S isn't supported on static-routing or policy-based gateways; DDNS isn't supported.
- If the client's local LAN range falls inside the VNet range or the client address pool, traffic stays local. After changing VNet DNS servers, generate and install a new client package.
- The Azure VPN client allows only one connection at a time.

## 5. Troubleshooting
- Resource logs: `TunnelDiagnosticLog` (tunnel state changes with a reason), `IKEDiagnosticLog` (IKE messages), `RouteDiagnosticLog` (static route and BGP changes), `GatewayDiagnosticLog` (configuration, failover and maintenance), `P2SDiagnosticLog`.
- Metrics: `TunnelAverageBandwidth`, `TunnelIngressPacketDropTSMismatch` and `TunnelEgressPacketDropTSMismatch` (traffic selector mismatch), `BgpPeerStatus`, `BgpRoutesLearned`, `BgpRoutesAdvertised`, `P2SConnectionCount`.
- `az network vnet-gateway reset` resets the gateway; for active-active add `--gateway-vip` to target one instance. `az network vpn-connection shared-key reset` resets the shared key.
- Compare the on-premises device proposals with the connection's custom policy parameters; a mismatch stops the tunnel.

## Gotchas
- NSGs on the gateway subnet aren't supported and can stop the gateway working.
- APIPA BGP addresses for Azure must be in 169.254.21.0 to 169.254.22.255 and unique across devices and gateways; with APIPA the on-premises device must initiate the BGP session.
- Custom VNet DNS must forward to Azure DNS (168.63.129.16), or the gateway can't reach the Azure control plane. A linked `privatelink.blob.core.windows.net` private DNS zone can return NXDOMAIN for gateway storage lookups: enable Fallback to internet on that zone's link.
- You can't change a connection's IKEv1/IKEv2 type after creation; delete and recreate it.

## Verify
- [ ] Connection status shows Connected in the portal; `list-bgp-peer-status` shows the peer connected and `list-learned-routes` shows on-premises prefixes.
- [ ] `BgpPeerStatus` and `TunnelAverageBandwidth` metrics show activity on each tunnel.
- [ ] P2S: the Azure VPN Client connects with Entra credentials and `P2SConnectionCount` rises.

## Checked

2026-11-07. Read in full: About gateway SKUs, Configure P2S for Entra ID (manually registered app), Azure VPN Gateway monitoring data reference, and the IPsec/IKE policy page (see the device skill). The VPN Gateway FAQ (about 77 KB) was searched and read in the sections on gateway subnet, public IPs, active-active, P2S, BGP and IKE, not end to end. CLI references for `vnet-gateway`, `local-gateway` and `vpn-connection` were searched for the flags used, not read end to end. The Entra steps were not run.
Corrected: `az network local-network-gateway create` does not exist; the command is `az network local-gateway create`. Removed: "Standard and High Performance retired" (the page says legacy), the ECMP and four-tunnel mesh claims, `az network vnet-gateway vpn-client generate` (not read), UDR claims on GatewaySubnet, firewall steering via UDR, resize and recreate behaviour, forced-tunnelling prefixes, the BGP communities claim, `az network watcher troubleshooting start`, `connectionStatus` queries, private-endpoint DNS resolver advice and P2S certificate rotation notes. Added FAQ BGP rules and DNS gotchas.

Method: documentation only; no commands were run.
