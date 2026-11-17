---
id: computing-software.cloud-infrastructure-engineering.azure.vpn-gateway-nat-rules-for-overlapping-ranges
name: vpn-gateway-nat-rules-for-overlapping-ranges
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vpn-gateway, vpn-nat, nat-rules-vpn, overlapping-address-space, ingress-snat, egress-snat, static-nat, dynamic-nat, bgp-translation, site-to-site]
level: advanced
status: docs-checked
description: "Connect on-prem sites whose address space overlaps Azure (or each other) using VPN Gateway static NAT rules, ingress/egress SNAT and BGP route translation."
sources: ["https://learn.microsoft.com/en-us/azure/vpn-gateway/nat-overview", "https://learn.microsoft.com/en-us/azure/vpn-gateway/nat-howto", "https://learn.microsoft.com/en-us/azure/virtual-wan/nat-rules-vpn-gateway", "https://learn.microsoft.com/en-us/cli/azure/network/vnet-gateway/nat-rule", "https://learn.microsoft.com/en-us/cli/azure/network/vpn-connection"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VPN Gateway NAT rules for overlapping address ranges

**Goal:** connect two or more on-premises networks (and the VNet) that use the same prefix through one VPN gateway, each seen under a unique translated prefix.

## 1. Model
- **IngressSnat** maps an on-premises address space to a translated space. A single SNAT rule handles both directions for that network, so no DNAT rules are needed.
- **EgressSnat** maps the Azure VNet address space to a translated space for the connections that use it.
- Internal Mapping is the pre-NAT space; External Mapping is the post-NAT space. External mappings must not overlap each other or networks connected without NAT; any suitable range works, public or private.
- **Static** rules are a fixed 1:1 mapping and the two prefixes must be the same length. **Dynamic** rules translate to varying addresses and ports (NAPT); traffic is then unidirectional and must start from the Internal Mapping side. Use Dynamic only when the target pool is smaller than the original. Largest Dynamic external mapping is /26.
- Port mappings: Static type only, single ports (no ranges), TCP and UDP.
- Each rule holds one prefix: a network with two prefixes needs two rules of matching lengths, and both must be linked to the connection or the unlinked prefix is not translated.

## 2. Limits
- SKUs VpnGw2-5 and VpnGw2AZ-5AZ.
- IPsec/IKE cross-premises connections only; not VNet-to-VNet or P2S.
- Route-based only; not on policy-based VPNs or connections with Use Policy Based Traffic Selectors enabled.
- Up to 500 rules (ingress and egress combined); no `/` in a rule name.
- NAT works on active-active and active-standby gateways; each rule applies to one gateway instance, chosen with the IP configuration ID (`--ip-config-id` in the CLI), so active-active needs a rule per instance.

## 3. Configure (order matters)
Create and save the rules on the gateway first, then create each connection with its rules linked in the same step. The how-to page warns that a connection created without the rules fails when the VNet and branches share the same space. Saving rules in the portal can take up to 10 minutes.
```bash
az network vnet-gateway nat-rule add -g rg-hub --gateway-name vgw-hub -n Branch1 --type Static --mode IngressSnat   --internal-mappings 10.0.1.0/24 --external-mappings 192.168.2.0/24
az network vnet-gateway nat-rule add -g rg-hub --gateway-name vgw-hub -n VNet --type Static --mode EgressSnat   --internal-mappings 10.0.1.0/24 --external-mappings 192.168.1.0/24
az network vnet-gateway nat-rule list -g rg-hub --gateway-name vgw-hub
az network vpn-connection create -g rg-hub -n VNet-Branch1 --vnet-gateway1 vgw-hub --local-gateway2 lgw-branch1 --shared-key <key>   --ingress-nat-rule <Branch1-rule-resource-id> --egress-nat-rule <VNet-rule-resource-id>
```
`nat-rule add/list/remove` and the connection `--ingress-nat-rule`/`--egress-nat-rule` flags are marked Preview in the CLI reference. Rule resource IDs look like `.../virtualNetworkGateways/<gw>/natRules/<name>`. The how-to page itself uses the portal: gateway, NAT Rules, then Add connection with Ingress and Egress NAT rules selected.

Worked example from the overview (VNet and two branches all 10.0.1.0/24): VNet egress to 192.168.1.0/24, Branch 1 ingress to 192.168.2.0/24, Branch 2 ingress to 192.168.3.0/24; each connection gets its branch's ingress rule plus the VNet egress rule.

## 4. Routing and BGP
- With BGP, enable **BGP Route Translation** in the gateway's NAT rules page. Learned routes on connections with IngressSnat rules are translated to the External Mapping; the gateway advertises the External Mapping of EgressSnat rules. Connections without NAT rules are not converted. The on-premises BGP routers must advertise exactly the prefixes in the IngressSnat rules.
- NAT is not supported with BGP APIPA addresses. If the on-premises BGP peer IP is a normal address that collides with other space, translate it with the IngressSnat rule and put the post-NAT address in the BGP peer IP field of the local network gateway.
- You need both an ingress and an egress rule on a connection when the on-premises space overlaps the VNet space. If the VNet space is unique, ingress rules alone avoid overlap among branches.
- Reuse an ingress rule across connections only when they go to the same on-premises network (for redundancy).
- Virtual WAN is separate: set rules on the hub's VPN (Site to site) NAT rules page and link them to VPN site link connections. There Static rules apply to both gateway instances, and for statically routed sites the External Mapping is added to the VPN site's Private Address Space.

## Gotchas
- A rule not linked to a connection does nothing; NAT applies only to connections that have rules.
- Internet breakout and NAT64 are not supported.

## Verify
- [ ] `az network vnet-gateway nat-rule list -g rg-hub --gateway-name vgw-hub` shows each rule.
- [ ] Connection status is Connected.
- [ ] With BGP, `az network vnet-gateway list-learned-routes` shows the translated (External Mapping) prefixes for NAT'ed branches.

## Checked

2026-11-07. Read in full: About NAT on Azure VPN Gateway (including FAQ), How to configure NAT for Azure VPN Gateway, and the Virtual WAN NAT rules page (read for the points listed above only, not every example). The `az network vnet-gateway nat-rule` CLI page was read for the add syntax and parameters; the `vpn-connection` and `vnet-gateway` references are large, so I searched them for the NAT flags and `list-learned-routes`, not read end to end.
Corrected or removed: the local network gateway "must list external prefixes" claim, the 100.64.x example values (now the documented 192.168.x), the `vpn-connection update --set ingressNatRules` command (not documented; replaced with `create --ingress-nat-rule`), the `enableBgpRouteTranslationForNat` property name, app and DNS caveats, ping-based verify, NSG/UDR statement, and `--type` wording. Added documented limits, FAQ points and Virtual WAN differences.

Method: documentation only; no commands were run.
