---
id: computing-software.systems-network-administration.network-design.cloud-hybrid-connectivity-vpn-direct-connect-expressroute
name: cloud-hybrid-connectivity-vpn-direct-connect-expressroute
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, cloud-networking, direct-connect, expressroute, site-to-site-vpn, hybrid-cloud, bgp, transit-gateway]
level: practitioner
status: docs-checked
description: "Connect on-prem to AWS/Azure: site-to-site VPN vs Direct Connect/ExpressRoute, BGP design, redundancy models, VPN backup over private circuits, and MTU."
sources:
  - https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html
  - https://aws.amazon.com/directconnect/resiliency-recommendation/
  - https://learn.microsoft.com/en-us/azure/expressroute/expressroute-introduction
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hybrid connectivity: VPN, Direct Connect, ExpressRoute

| | Site-to-site IPsec VPN | AWS Direct Connect / Azure ExpressRoute |
|---|---|---|
| Path | internet | private circuit via a colo/partner |
| Bandwidth | per-tunnel limits apply (see the vendor quota page) | chosen port or circuit size |
| Latency/jitter | variable | consistent |
| Cost | see vendor pricing pages | see vendor pricing pages |

## Design
- **BGP everywhere:** both services use BGP; advertise summarised on-prem prefixes, receive
  VPC/VNet CIDRs. Set your ASN, MD5 (AWS DX), BFD where supported.
- **Hubs:** use the provider's transit hub service rather than many point-to-point links.
- **Redundancy:** AWS recommends separate connections on separate devices in more than one location for
  maximum resilience, and at least two connections on different devices at one location for high
  resiliency. Azure ExpressRoute has built-in redundancy in each peering location (a BGP session
  to each of two Microsoft edge routers), so add a circuit in a second location for site resilience.
- **VPN as backup** of the private circuit: same prefixes over both, private circuit preferred
  (set on-prem local-pref or AS-path so the private circuit wins).

## Gotchas
- MTU: Direct Connect supports link-layer frame sizes of 1522 or 9023 bytes; VPN tunnels carry
  less because of IPsec overhead; mismatched MTU on failover breaks large transfers. Clamp MSS.
- Route limits: each service caps the prefixes you may advertise (see the vendor quota pages);
  summarise.
- Asymmetric return paths through different firewalls when both VPN and DX are active.

## Verify
- [ ] BGP up on all links; failover test (shut DX) moves traffic to VPN within the BGP timers; large-packet test passes on both paths.

## Checked

- Date: 2026-10-28
- Confirmed: Direct Connect needs BGP and BGP MD5 with optional BFD; AWS resiliency recommendation (separate connections and devices, more than one location); ExpressRoute built-in redundancy and dual BGP to each MSEE; DX frame sizes 1522 or 9023 bytes.
- Removed: tunnel and circuit bandwidth figures, lead times, encryption row, cost row, hub product names, private vs Microsoft peering line, jumbo 9001/8500 and 1436-byte MTU figures, the 100-prefix limit, the claim that AWS prefers DX over VPN.

Method: documentation only; no commands were run.
