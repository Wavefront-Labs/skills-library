---
id: computing-software.cloud-infrastructure-engineering.azure.gatewaysubnet-udr-for-on-prem-to-spoke-inspection
name: gatewaysubnet-udr-for-on-prem-to-spoke-inspection
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, routing, gatewaysubnet-udr, hub-spoke, azure-firewall, expressroute, vpn-gateway]
level: advanced
status: docs-checked
description: "Inspect on-prem to spoke traffic: UDRs on the GatewaySubnet pointing spoke prefixes at the firewall, symmetric spoke routes, and what is unsupported on GatewaySubnet."
sources: ["https://learn.microsoft.com/azure/vpn-gateway/vpn-gateway-about-vpn-gateway-settings#gwsub", "https://learn.microsoft.com/azure/architecture/networking/architecture/hub-spoke", "https://learn.microsoft.com/azure/firewall/firewall-faq"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UDRs on the GatewaySubnet

**Goal:** traffic from on-premises (VPN/ExpressRoute) to spokes passes through the hub firewall in both directions.

## Inbound from on-prem: route table on GatewaySubnet
```bash
az network route-table create -g rg-hub -n rt-gatewaysubnet --disable-bgp-route-propagation false
az network route-table route create -g rg-hub --route-table-name rt-gatewaysubnet -n to-spoke1 \
  --address-prefix 10.20.0.0/22 --next-hop-type VirtualAppliance --next-hop-ip-address 10.0.1.4
az network vnet subnet update -g rg-hub --vnet-name vnet-hub -n GatewaySubnet --route-table rt-gatewaysubnet
```
One route per spoke prefix (or a summarised prefix covering all spokes), next hop = firewall private IP.

## Return path: spoke route tables
Spoke subnets: `0.0.0.0/0 -> firewall` (or on-prem prefixes -> firewall) and **gateway route propagation
disabled** on the spoke route table so BGP-learned on-prem routes don't send replies straight to the gateway
(asymmetric routing = firewall drops the return flow).

## Rules on GatewaySubnet
- **Keep gateway route propagation enabled** on the GatewaySubnet route table - with it disabled the gateway won't function.
- Don't put a `0.0.0.0/0` UDR on the GatewaySubnet (unsupported).
- Don't associate an NSG with the GatewaySubnet (unsupported).
- UDRs that cover the GatewaySubnet address space with next hop None, or with an NVA that drops the traffic, are unsupported and block gateway creation; a UDR overlapping the gateway subnet or gateway public IP range can affect diagnostics, data path and control path. Route specific spoke prefixes.

## Hub VNet traffic
Traffic from on-prem to resources **in the hub** (not spokes) can also be inspected by routing those subnet
prefixes to the firewall from the GatewaySubnet route table.

## Gotchas
- New spokes need a GatewaySubnet route - automate via AVNM or IaC alongside peering.
- Virtual WAN hubs are Microsoft-managed; these rules apply to customer-managed hubs.
- Firewall must have rules for on-prem source ranges; by default Azure Firewall doesn't SNAT network-rule traffic to RFC 1918 or RFC 6598 ranges.

## Verify
- [ ] `az network watcher show-next-hop` from a spoke VM to an on-prem IP returns the firewall; firewall logs show both directions of a test flow.

## Checked

2026-10-31. Confirmed against the VPN Gateway settings page (gateway subnet considerations: no 0.0.0.0/0 UDR, no NSG, BGP route propagation must stay enabled, overlapping UDRs), the user-defined routes page (route propagation note, AVNM routing configuration for on-premises traffic through a firewall), the hub-spoke architecture, the Azure Firewall FAQ and SNAT private range pages. Removed: the whole-hub-prefix rationale (replaced by the documented overlap warning) and the routing-intent remark. Commands were checked with check_commands.py.

Method: documentation only; no commands were run.
