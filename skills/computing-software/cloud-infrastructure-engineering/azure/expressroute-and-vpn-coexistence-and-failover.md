---
id: computing-software.cloud-infrastructure-engineering.azure.expressroute-and-vpn-coexistence-and-failover
name: expressroute-and-vpn-coexistence-and-failover
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, expressroute, coexistence, vpn-failover, site-to-site, bgp-path-selection]
level: advanced
status: docs-checked
description: "Run ExpressRoute and site-to-site VPN gateways side by side in one VNet so VPN backs up ER, with BGP route preference, prefix design and failover testing."
sources: ["https://learn.microsoft.com/azure/expressroute/expressroute-howto-coexist-resource-manager", "https://learn.microsoft.com/azure/expressroute/use-s2s-vpn-as-backup-for-expressroute-privatepeering", "https://learn.microsoft.com/azure/expressroute/expressroute-routing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ExpressRoute and S2S VPN coexistence

**Goal:** keep on-premises connectivity alive when an ExpressRoute circuit fails by falling back to IPsec VPN.

## Build
- One `GatewaySubnet` of **/27 or larger** holds both the ExpressRoute gateway and the VPN gateway.
- The VPN gateway must be **route-based**.
- ExpressRoute-VPN gateway coexistence is not supported with the Basic SKU VPN gateway.

## Route preference
Azure prefers ExpressRoute over VPN for the same prefix when both are learned. On premises you must do the same:
- On your edge, prefer ER-learned routes by setting a higher local preference for routes received via ExpressRoute, to avoid asymmetric routing.

## Failover test
1. Baseline: `az network nic show-effective-route-table` on a test VM shows routes learned over ExpressRoute.
2. Disable the ER connection (or shut the BGP session on your router).
3. Watch routes converge to the VPN path; record how long convergence takes.
4. Re-enable ER; confirm traffic moves back.

## Gotchas
- Asymmetric routing: if on-prem returns traffic via the other path, stateful firewalls drop it. Align preferences on both sides.
- VPN bandwidth is far below ER; test that critical flows fit, or shed non-critical traffic.

## Verify
- [ ] Both gateways `Succeeded`; `az network vnet-gateway list-learned-routes` shows on-prem prefixes from both ER and VPN peers.
- [ ] Documented failover drill result with timings.

## Checked
2026-10-28. Confirmed on the coexistence, VPN-as-backup and routing pages: gateway subnet /27 or shorter prefix, route-based VPN gateway only, coexistence not supported with Basic SKU VPN gateway, Azure prefers ExpressRoute when a route is advertised over both, set a higher local preference on ExpressRoute-learned routes. CLI commands passed the CLI reference check.
Removed (not confirmed): BGP-on-VPN requirement, creation-order claim, AS-path prepend and more-specific-prefix guidance, convergence time, next-hop name, FastPath and Virtual WAN gotchas.

Method: documentation only; no commands were run.
