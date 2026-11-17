---
id: computing-software.cloud-infrastructure-engineering.azure.add-vnet-address-space-with-peering-sync-and-subnet-resize
name: add-vnet-address-space-with-peering-sync-and-subnet-resize
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, virtual-network, add-address-space, resync-peering, subnet-resize, ip-exhaustion]
level: practitioner
status: docs-checked
description: "Grow a VNet without downtime: add address prefixes to peered VNets, resync peerings, when a subnet range can be changed, and what to do when a subnet runs out of IPs."
sources: ["https://learn.microsoft.com/azure/virtual-network/update-virtual-network-peering-address-space", "https://learn.microsoft.com/azure/virtual-network/virtual-network-manage-subnet", "https://learn.microsoft.com/cli/azure/network/vnet/peering#az-network-vnet-peering-sync"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Add VNet address space and resize subnets

**Goal:** more IPs for a spoke without tearing down peerings.

## Add an address prefix (peered VNet)
Changing the address space of a peered VNet causes no downtime, but each remote peer must be synced afterwards.
```bash
az network vnet update -g rg-spoke -n vnet-spoke1 --address-prefixes 10.20.0.0/22 10.20.8.0/22
az network vnet peering sync -g rg-hub --vnet-name vnet-hub -n hub-to-spoke1
az network vnet peering sync -g rg-spoke --vnet-name vnet-spoke1 -n spoke1-to-hub
```
- Syncing is required after modifying a range, adding a range, or deleting a range. Run the sync after each resize
  operation rather than batching several resizes first.
- The new range must not overlap any address space of the peered VNets.
- Gateway transit advertises the hub address space and peered VNet address spaces to on-premises by default, so
  on-prem routes change too; also update firewall rules, NSG rules with literal prefixes and IPAM records.

## Resize a subnet
- You can change a subnet's address range only if no resources are deployed in it; otherwise move or delete the
  resources first.
- Delegations cannot be added or removed while resources of that service are in the subnet.
```bash
az network vnet subnet update -g rg-spoke --vnet-name vnet-spoke1 -n snet-app --address-prefixes 10.20.1.0/24
```
- Before an address range can be deleted from the VNet it must be empty: remove any resources using it first.

## When a subnet is full
Add a new subnet in a new prefix and place new resources there, or move resources out so the range can be changed.

## Verify
- [ ] After the sync, the peered VNet's Address space page lists the new range, and a VM in the new prefix reaches the hub.

## Checked
2026-10-31. Confirmed against Learn "Update the address space for a peered virtual network", "Add, change, or delete a
virtual network subnet", the peering overview and the `az network vnet peering sync` reference: no downtime, sync
after modify/add/delete, no overlap, subnet range change needs an empty subnet, delegation rule, empty range before
delete, gateway transit advertising. Removed: `peeringSyncLevel` values and the `FullyInSync` check, specific
per-service resize claims, AKS CNI Overlay, App Service integration and IPAM pool advice, NVA behaviour claims.
Method: documentation only; no commands were run.
