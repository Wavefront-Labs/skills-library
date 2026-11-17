---
id: computing-software.cloud-infrastructure-engineering.azure.vnet-peering-create-local-global-and-verify
name: vnet-peering-create-local-global-and-verify
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vnet-peering, peering-create, global-peering, peering-state, cross-subscription-peering, subnet-peering]
level: practitioner
status: docs-checked
description: "Create VNet peerings (same region, global, cross-subscription/tenant), choose forwarding and gateway flags, sync address space changes and verify peering state."
sources: ["https://learn.microsoft.com/azure/virtual-network/virtual-network-peering-overview", "https://learn.microsoft.com/azure/virtual-network/virtual-network-manage-peering", "https://learn.microsoft.com/azure/virtual-network/create-peering-different-subscriptions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create VNet peering and verify

**Goal:** two VNets connected with the right flags on each side, in a state you can prove.

## Create both directions
```bash
az network vnet peering create -g rg-hub -n hub-to-spoke1 --vnet-name vnet-hub \
  --remote-vnet /subscriptions/<sub2>/resourceGroups/rg-spoke1/providers/Microsoft.Network/virtualNetworks/vnet-spoke1 \
  --allow-vnet-access true --allow-forwarded-traffic true --allow-gateway-transit true
az network vnet peering create -g rg-spoke1 -n spoke1-to-hub --vnet-name vnet-spoke1 \
  --remote-vnet <hub-vnet-id> --allow-vnet-access true --allow-forwarded-traffic true --use-remote-gateways true
```
- Permissions: *Network Contributor*, or a custom role with `Microsoft.Network/virtualNetworks/virtualNetworkPeerings/write`, `read` and `delete`; removing the remote side's peering needs read and delete on the remote VNet.
- Cross-tenant: add each tenant's user as a guest in the opposite tenant with *Network Contributor* on the VNet; the guest invitation must be accepted.
- Global peering (different regions) works the same. Ingress and egress over a peering is charged; see the Azure Virtual Network pricing page.

## Flags
| Flag | Meaning |
|---|---|
| allowVirtualNetworkAccess | Address spaces become reachable (VirtualNetwork tag includes remote) |
| allowForwardedTraffic | Accept traffic not originating in the remote VNet (from NVA/firewall) |
| allowGatewayTransit / useRemoteGateways | Share the hub's VPN/ER gateway or Route Server |

## States
`Initiated` (first side created) → `Connected` (second side created; the peering isn't established until both sides show Connected).
After you resize the address space of a peered VNet, the peers must be synced; run sync after each resize rather than batching several:
```bash
az network vnet peering sync -g rg-hub --vnet-name vnet-hub -n hub-to-spoke1
```

## Subnet-level peering (newer)
Peer only selected subnets (`--peer-complete-vnets false --local-subnet-names ... --remote-subnet-names ...`) instead of the whole address space and all subnets.

## Verify
```bash
az network vnet peering list -g rg-hub --vnet-name vnet-hub -o table
az network nic show-effective-route-table -g rg-spoke1 -n nic-vm1 -o table   # VNetPeering routes present
```

## Gotchas
- Peered VNets must have nonoverlapping address spaces.
- Peering isn't transitive: spoke1 ↔ hub ↔ spoke2 needs a firewall/NVA or AVNM mesh.
- A VNet that uses a remote gateway can't have its own gateway (a VNet can have only one gateway).
- You can't move a VNet while it is peered: delete the peering, move the VNet, then recreate the peering.

## Verify (checklist)
- [ ] Both sides show `Connected`.
- [ ] Spoke VM effective routes include the hub prefix with next hop VNetPeering.

## Checked

2026-10-31. Confirmed against the Learn virtual network peering overview, manage-peering and cross-subscription/tenant pages (Initiated and Connected states, non-transitive peering, nonoverlapping address spaces, Network Contributor and the peering write/read/delete actions, guest users across tenants, gateway transit and remote gateway rules, subnet peering, address space resize needing a sync, peering charges) and the az network vnet peering CLI reference (including the plural --peer-complete-vnets flag, corrected here). Removed: the Disconnected, LocalNotInSync, RemoteNotInSync and FullyInSync state names, the peer/action permission, the global-rate billing wording, the overlapping-address workaround claim and the peeringSyncLevel query (none confirmed).

Method: documentation only; no commands were run.
