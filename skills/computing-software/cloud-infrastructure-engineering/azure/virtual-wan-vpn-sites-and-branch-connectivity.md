---
id: computing-software.cloud-infrastructure-engineering.azure.virtual-wan-vpn-sites-and-branch-connectivity
name: virtual-wan-vpn-sites-and-branch-connectivity
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, virtual-wan, vwan, vpn-sites, vwan-branches, vwan-vpn, site-to-site, branch-to-branch, sd-wan, scale-units, bgp, vpn-site-links, hub-vpn-gateway]
level: practitioner
status: docs-checked
description: "Connect branches to Azure Virtual WAN: hub VPN gateway scale units, VPN sites with links and BGP, connections, branch-to-branch, SD-WAN partner automation and config download."
sources: ["https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-site-to-site-portal", "https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-faq", "https://learn.microsoft.com/en-us/azure/virtual-wan/virtual-wan-about", "https://learn.microsoft.com/en-us/cli/azure/network/vpn-site", "https://learn.microsoft.com/en-us/cli/azure/network/vpn-gateway/connection"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual WAN VPN sites and branch connectivity

**Goal:** dozens to hundreds of branches connected to a Virtual WAN hub over IPsec, with
dual links, BGP, branch-to-branch through Microsoft's backbone, and configuration that
partners' SD-WAN controllers can push automatically.

## 1. Hub and gateway
```bash
az network vwan create -g rg-wan -n vwan-prod --type Standard --branch-to-branch-traffic true
az network vhub create -g rg-wan -n vhub-uks --vwan vwan-prod --address-prefix 10.100.0.0/23 -l uksouth
az network vpn-gateway create -g rg-wan -n vpngw-uks --vhub vhub-uks --scale-unit 2 -l uksouth   # 1 SU = 500 Mbps aggregate, gateway is active-active
```
- **Standard** vWAN supports ExpressRoute, point-to-site and site-to-site VPN, inter-hub and VNet-to-VNet transit, Azure Firewall and NVAs in the hub; Basic can be upgraded to Standard but not back.
- Scale units size *aggregate* throughput of the active-active gateway; a single tunnel is still
  limited — see the Virtual WAN FAQ throughput table and use multiple links/tunnels for fat sites.

## 2. Sites, links, connections
```bash
az network vpn-site create -g rg-wan -n site-leeds --virtual-wan vwan-prod -l uksouth \
  --device-vendor Fortinet --device-model FG-100F --link-speed 200 \
  --ip-address 198.51.100.10 --asn 65101 --bgp-peering-address 169.254.21.1     # or --address-prefixes when no BGP
az network vpn-site link add ...                                                # second ISP link (a VPN connection supports up to 4 link connections)
az network vpn-gateway connection create -g rg-wan --gateway-name vpngw-uks -n cn-leeds \
  --remote-vpn-site <site-id> --shared-key "$PSK" --enable-bgp true --protocol-type IKEv2
az network vpn-site download -g rg-wan --vwan-name vwan-prod --request @download.json   # JSON: the site ids and a blob SAS URL to write the config to
```
- Each site **link** = one ISP circuit with its own public IP/BGP address; the gateway
  builds tunnels from both gateway instances to each link (4 tunnels for 2 links).
- BGP: Azure hub ASN is 65515; custom BGP IPs on the gateway use APIPA ranges 169.254.21.* and 169.254.22.*; custom IPsec policy per connection if the device can't do defaults.
- Virtual WAN partner SD-WAN/CPE solutions can automate site creation and config download — prefer this over hand-built sites at scale.

## 3. Routing
- Branches learn hub VNets and other branches automatically (default route table); isolate
  with custom route tables/labels or **routing intent** to send branch traffic through a hub firewall.
- With an Internet routing policy on the hub, `0.0.0.0/0` reaches a branch only if the connection has *Propagate Default Route* / *Enable Internet Security* set to true; the default route isn't advertised across hubs.
- Branch-to-branch is enabled by default and traverses Virtual WAN.

## Gotchas
- On-premises ranges must not overlap the virtual networks you connect, and the hub address range can't overlap connected VNets.
- Store PSKs in Key Vault; `az network vpn-gateway connection create` takes `--shared-key` (check the update options before scripting rotation).

## Checked
2026-10-28. Confirmed on Microsoft Learn (Virtual WAN FAQ, About, site-to-site portal) and the `az network vpn-site` / `vpn-gateway connection` references: 1 VPN scale unit = 500 Mbps, active-active gateway, up to 4 link connections each with two tunnels, ASN 65515, APIPA ranges 169.254.21.*/22.*, Standard vs Basic features, branch-to-branch default, default-route propagation setting, overlap rules, command flags. Corrected: `vpn-site download` takes `--request`; `vpn-gateway connection update` has no `--shared-key`. Removed: per-tunnel Gbps figure, SD-WAN partner names, NAT-rule, scale-unit reset and config-download-scope claims.
Method: documentation only; no commands were run.

## Verify
- [ ] `az network vpn-gateway connection show ... --query connectionStatus` and portal *VPN sites* show each link `Connected`.
- [ ] Hub *Effective routes* include branch prefixes; a VM in a connected VNet reaches a host in each branch.
- [ ] Branch-to-branch traceroute goes via the hub (or via the firewall if routing intent is on).
