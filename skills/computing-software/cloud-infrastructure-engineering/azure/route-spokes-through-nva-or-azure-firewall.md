---
id: computing-software.cloud-infrastructure-engineering.azure.route-spokes-through-nva-or-azure-firewall
name: route-spokes-through-nva-or-azure-firewall
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, udr, nva-routing, virtual-appliance-next-hop, route-tables, hub-and-spoke, azure-firewall, ip-forwarding]
level: advanced
status: docs-checked
description: "Steer spoke traffic through a hub firewall or NVA with UDRs: route tables for spokes and GatewaySubnet, IP forwarding, symmetric routing and HA NVA patterns."
sources: ["https://learn.microsoft.com/azure/virtual-network/virtual-networks-udr-overview", "https://learn.microsoft.com/azure/firewall/tutorial-hybrid-portal", "https://learn.microsoft.com/azure/architecture/networking/guide/network-virtual-appliance-high-availability", "https://learn.microsoft.com/azure/architecture/networking/architecture/hub-spoke"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route spokes through an NVA or Azure Firewall

**Goal:** all spoke egress, spoke-to-spoke and on-prem-to-spoke traffic passes the hub firewall,
symmetrically, without breaking platform traffic.

## Route tables
**Spoke subnets** (`rt-spoke`):
| Prefix | Next hop |
|---|---|
| 0.0.0.0/0 | VirtualAppliance → firewall private IP (e.g. 10.0.0.4) |
| 10.0.0.0/8 (other spokes/on-prem) | VirtualAppliance → 10.0.0.4 |
Disable gateway route propagation on spoke route tables so on-prem BGP routes don't bypass the firewall.

**GatewaySubnet** (`rt-gateway`) — for on-prem → spoke inspection:
| Prefix | Next hop |
|---|---|
| 10.20.0.0/16 (each spoke) | VirtualAppliance → 10.0.0.4 |
Keep propagation **enabled** here; never put 0.0.0.0/0 on GatewaySubnet.

**AzureFirewallSubnet**: the firewall needs direct Internet connectivity; if the subnet learns a default route from on-premises via BGP, override it with a 0.0.0.0/0 UDR with next hop type Internet (forced tunnelling is a separate supported setup).

```bash
az network route-table create -g rg-net -n rt-spoke --disable-bgp-route-propagation true
az network route-table route create -g rg-net --route-table-name rt-spoke -n default --address-prefix 0.0.0.0/0 \
  --next-hop-type VirtualAppliance --next-hop-ip-address 10.0.0.4
az network vnet subnet update -g rg-net --vnet-name vnet-spoke1 -n snet-app --route-table rt-spoke
```

## Third-party NVA specifics
- Enable **IP forwarding** on the NVA NICs (`az network nic update --ip-forwarding true`) and in the guest OS.
- HA: at least two NVAs behind an **internal Standard LB with HA ports**; UDR next hop = LB frontend IP. For active/standby, the health probe port should answer only on the active instance.
- Return traffic must hit the same NVA instance: when both directions of a flow traverse the same internal load balancer it picks the same NVA, but a dual-NIC design with a load balancer per direction needs SNAT on the NVA to stay symmetric.
- Deploy the NVA in a different subnet from the resources that route through it; the same subnet can cause routing loops.

## Symmetric routing checks
- On-prem → spoke via GatewaySubnet UDR → firewall → spoke; spoke → on-prem via spoke UDR → firewall → gateway. Both legs through the same firewall = symmetric.
- Spoke-to-spoke: both spokes' UDRs send the other's prefix to the firewall.
- Things that break: a spoke route table without the 10/8 route (peering route wins: direct spoke-hub traffic bypasses), or the hub's own subnets lacking routes.

## Gotchas
- Longest prefix wins: a VNet's own address space system route (more specific) beats your 10.0.0.0/8 UDR for intra-VNet traffic. To inspect between subnets use a UDR on the VNet address range plus a route per subnet with next hop type Virtual network for same-subnet traffic (Azure Firewall FAQ); NSGs are the recommended method for internal segmentation.
- Private endpoints add a /32 route that beats broader UDRs; enable network policies for user-defined routes on the PE subnet and use a UDR prefix at least as specific as the VNet address space (a 0.0.0.0/0 UDR doesn't override it).
- GatewaySubnet is special: no 0.0.0.0/0 UDR, no NSG, and route propagation stays enabled.

## Verify
- [ ] Network Watcher next hop from a spoke VM to 8.8.8.8 and to another spoke = VirtualAppliance 10.0.0.4.
- [ ] Firewall logs show flows in both directions for a spoke-to-on-prem test.

## Checked

2026-10-31. Confirmed against the Learn pages on user-defined routes (virtual appliance next hop, IP forwarding, route propagation, GatewaySubnet restrictions, routing-loop warning, longest prefix match), NVA high availability (internal load balancer with HA ports, health probe port, SNAT for dual-NIC symmetry), the hub-spoke architecture, the Azure Firewall FAQ (subnet routing, forced tunnelling) and private endpoint network policies. Removed: the AKS outboundType line, the App Gateway, Bastion and APIM line, the session-affinity wording and the AzureFirewallSubnet self-route remark (none confirmed). Commands were checked against the az CLI reference with check_commands.py.

Method: documentation only; no commands were run.
