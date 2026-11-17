---
id: computing-software.cloud-infrastructure-engineering.azure.subnet-level-peering
name: subnet-level-peering
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vnet-peering, subnet-level-peering, peer-complete-vnets, overlapping-address-space, segmentation]
level: advanced
status: docs-checked
description: "Peer specific subnets instead of whole VNets: when it helps (partial overlaps, least exposure), CLI parameters, subscription allowlisting and documented limits."
sources: ["https://learn.microsoft.com/azure/virtual-network/how-to-configure-subnet-peering", "https://learn.microsoft.com/azure/virtual-network/virtual-network-peering-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subnet-level peering

**Goal:** connect only the subnets that need to talk, e.g. when two VNets share an address space elsewhere or when
a partner VNet should reach one subnet, not your whole address space.

## How it differs
Regular peering connects entire address spaces and subnets. Subnet peering links only the subnets you list on each
side, so you can reuse address space across subnets that don't need to connect and avoid advertising the whole VNet
address space through gateways to on-premises.

## Before you start
- The subscription must be registered (allowlisted) through the form linked from the Learn page.
- Available in all regions, but configurable only through Terraform, PowerShell, API, CLI and ARM template (not the portal).
- Azure CLI 2.31.0 or later.

## Configure (CLI)
```bash
az network vnet peering create -g rg-a --vnet-name vnet-a -n a-to-b \
  --remote-vnet /subscriptions/<sub>/resourceGroups/rg-b/providers/Microsoft.Network/virtualNetworks/vnet-b \
  --peer-complete-vnets false \
  --local-subnet-names snet-app \
  --remote-subnet-names snet-api \
  --allow-vnet-access true
# and the reverse peering from vnet-b with local/remote swapped
```
`--peer-complete-vnets` defaults to true; `--enable-only-ipv6` peers dual-stack subnets over IPv6 only. To add or
remove subnets, update the same peering with `az network vnet peering update ... --local-subnet-names ...` and then
run `az network vnet peering sync` on both sides.

## Limits from the docs
- Participating subnets must be unique and belong to unique address spaces across all peering links.
- Only one peering link between two VNets; you can't convert a peering between full-VNet and subnet type - delete and recreate.
- Up to 200 subnets per side of one peering link, and no more than 1,000 peered subnets across all links of a VNet.
- Non-peered subnets can still hold a route to the peered subnets (packets are dropped); apply NSGs on participating subnets to allow only the peered subnets and address spaces.
- Routes for certain delegated subnet types can be over-advertised into the effective routes of VMs in peered subnets.

## Gotchas
- Forgetting the reverse side leaves the peering `Initiated`.
- Gateway transit, Virtual WAN and Virtual Network Manager interaction is not covered on the page - check before combining.

## Verify
- [ ] Traffic between the selected subnets works; NSGs block everything else you don't want.

## Checked
2026-10-31. Confirmed against Learn "How to configure subnet peering" and the `az network vnet peering` CLI reference:
allowlisting, tooling limits, CLI 2.31.0, parameters and defaults, 200 and 1,000 subnet limits, one link per VNet pair,
type change needs recreate, non-peered-subnet route behaviour. Removed: claim that effective routes list only the
selected prefixes (the page says otherwise), the M&A example, and unconfirmed IPv6 and service-compatibility statements.
Method: documentation only; no commands were run.
