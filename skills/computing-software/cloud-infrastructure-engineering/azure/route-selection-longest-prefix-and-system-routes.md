---
id: computing-software.cloud-infrastructure-engineering.azure.route-selection-longest-prefix-and-system-routes
name: route-selection-longest-prefix-and-system-routes
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, routing, longest-prefix-match, system-routes, route-precedence, service-endpoint-routes, effective-routes]
level: practitioner
status: docs-checked
description: "Predict Azure routing: longest prefix match, UDR vs BGP vs system precedence, default system routes and optional ones, and service endpoint routes that bypass a 0/0 UDR."
sources: ["https://learn.microsoft.com/azure/virtual-network/virtual-networks-udr-overview", "https://learn.microsoft.com/azure/virtual-network/diagnose-network-routing-problem", "https://learn.microsoft.com/azure/azure-resource-manager/management/azure-subscription-service-limits#networking-limits"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route selection in Azure

**Goal:** know exactly which next hop a packet will take before you change a route table.

## Selection rules
1. **Longest prefix match** wins: a /24 UDR beats a /16 system route, regardless of source.
2. Same prefix length from different sources: **UDR > BGP > system route**.
3. System routes for the VNet, VNet peering and service endpoints are preferred even when a BGP route is more specific, and a route with a `VirtualNetworkServiceEndpoint` next hop can't be overridden by a route table. A UDR with the same prefix as a default route turns that default route Invalid.

## Default system routes
| Prefix | Next hop |
|---|---|
| VNet address space(s) | Virtual network |
| 0.0.0.0/0 | Internet |
| 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 100.64.0.0/10 (also 127.0.0.0/8 and a few other reserved ranges) | None (dropped) |
Adding a 0.0.0.0/0 UDR to a subnet removes the 10.0.0.0/8, 192.168.0.0/16 and 100.64.0.0/10 default routes from that subnet's route table.
Optional system routes appear with features: **VNet peering** (peer prefixes), **virtual network gateway** (on-prem
prefixes, BGP-learned), **service endpoints** (public prefixes of the service, next hop VirtualNetworkServiceEndpoint).

## The service endpoint trap
Enabling a service endpoint for Storage on a subnet adds routes for Storage's public prefixes. They're more
specific than your `0.0.0.0/0 -> firewall` UDR, so **storage traffic bypasses the firewall**. If inspection is
required, use private endpoints (and route them deliberately) instead of service endpoints.

## Check before and after
```bash
az network nic show-effective-route-table -g rg -n vm01-nic -o table
az network watcher show-next-hop -g rg --vm vm01 --source-ip 10.1.1.4 --dest-ip 52.239.0.1
```
Effective routes show State Active/Invalid: an Invalid default route has been overridden by a UDR with the same prefix.

## Limits
A route table holds up to 400 UDRs by default (up to 1,000 with an AVNM routing configuration); check the Azure limits page for current values. Each subnet has zero or one route table, and a route table can be associated with zero or more subnets.

## Gotchas
- A private endpoint's /32 route wins by longest prefix match; enable network policies for user-defined routes on the PE subnet and use a UDR prefix at least as specific as the VNet address space (a 0.0.0.0/0 UDR doesn't override it).
- BGP-learned 0.0.0.0/0 (forced tunnelling from on-prem) beats the system Internet route but loses to a UDR 0/0.

## Verify
- [ ] Next hop checks for each critical destination match design; no unexpected Invalid routes in effective tables.

## Checked

2026-10-31. Confirmed against the Learn user-defined routes overview (longest prefix match, UDR over BGP over system route, default None routes, route removal when a 0.0.0.0/0 UDR is added, service endpoint routes not overridable, 400 and 1,000 UDR limits, one route table per subnet, Active/Invalid state) and the private endpoint network policy page. Removed: the equal-or-longer-prefix override claim, the "unless inside the VNet" qualifier and the same-region-and-subscription association rule (not in the docs). Commands were checked with check_commands.py.

Method: documentation only; no commands were run.
