---
id: computing-software.cloud-infrastructure-engineering.azure.avnm-connectivity-configurations-mesh-and-hub-spoke
name: avnm-connectivity-configurations-mesh-and-hub-spoke
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, virtual-network-manager, connectivity-configuration, mesh-topology, avnm-connectivity, connected-group, hub-and-spoke]
level: advanced
status: docs-checked
description: "Use Virtual Network Manager connectivity configurations to build hub-and-spoke and mesh topologies at scale: network groups, direct connectivity, global mesh and deployment."
sources: ["https://learn.microsoft.com/azure/virtual-network-manager/concept-connectivity-configuration", "https://learn.microsoft.com/azure/virtual-network-manager/how-to-create-mesh-network", "https://learn.microsoft.com/azure/virtual-network-manager/how-to-create-hub-and-spoke"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AVNM connectivity configurations (mesh and hub-spoke)

**Goal:** peerings for hundreds of VNets created and maintained from group membership, with
optional any-to-any connectivity inside a group — no per-VNet peering code.

## Topologies
- **Hub and spoke**: AVNM creates peerings between hub and each member of the spoke network groups; options *use hub as gateway* (gateway transit) and **direct connectivity** (spokes in the same group reach each other without the hub, via a *connected group*).
- **Mesh**: every VNet in the group reaches every other via a connected group (not individual peerings); mesh is regional by default and **global mesh** allows cross-region.

## Create
```bash
az network manager connect-config create -g rg-netmgmt --network-manager-name avnm-contoso -n cc-prod-hubspoke \
  --connectivity-topology HubAndSpoke \
  --hubs resource-id=<hub-vnet-id> resource-type=Microsoft.Network/virtualNetworks \
  --applies-to-groups network-group-id=<ng-prod-spokes> group-connectivity=DirectlyConnected use-hub-gateway=true is-global=false \
  --delete-existing-peering true
az network manager post-commit -g rg-netmgmt --network-manager-name avnm-contoso --commit-type Connectivity \
  --target-locations westeurope --configuration-ids <cc-id>
```
`--delete-existing-peering true` removes any peerings that don't match the connectivity configuration, even ones created manually after deployment, so use it with care on brownfield estates.

## Connected groups
Implemented by the platform, not as visible peerings (no entry under the VNet's Peerings); effective routes show next hop type
`ConnectedGroup`. A VNet can be in up to two connected groups. Address spaces may overlap by default, but traffic between overlapping subnets is dropped; set `ConnectedGroupAddressOverlap` to `Disallowed` to stop overlapping VNets joining a mesh. A connected group can hold up to 3,000 VNets once the `AllowHighScaleConnectedGroup` preview feature is registered and approved, and the high-scale private endpoint option supports up to 20,000 private endpoints.

## When to use mesh / direct connectivity
- Trusted environments where east-west inspection isn't required (e.g. all dev spokes).
- Combine with **security admin rules** to restrict which ports are allowed inside the mesh.
- Production with inspection needs: hub-spoke without direct connectivity + firewall UDRs.

## Gotchas
- Deployment is goal-state per region: committing a set of configurations to a region without this one removes it there. After changing any connectivity configuration, redeploy every connectivity configuration you want in effect in that region.
- Dynamic group membership via Azure Policy means a newly matching VNet receives the deployed configuration without a redeploy; guard against overlap with IPAM pools or `ConnectedGroupAddressOverlap`.
- *Use hub as gateway* needs a gateway in the hub: without one, creating the spoke-to-hub peering fails (the hub-to-spoke peering is still created).

## Verify
- [ ] `az network manager list-active-connectivity-config -g rg-netmgmt --network-manager-name avnm-contoso --regions westeurope`.
- [ ] Spoke NIC effective routes show `ConnectedGroup` (mesh or direct spoke-to-spoke) or `VNetPeering`/`GlobalVNetPeering` (hub) entries.

## Checked

2026-10-31. Confirmed against the Learn pages on connectivity configurations (topologies, connected groups, ConnectedGroup and VNetPeering next hops, two connected groups per VNet, 3,000 VNet and 20,000 private endpoint options, ConnectedGroupAddressOverlap, delete-existing-peerings, use hub as gateway), on configuration deployments (goal-state model, regional deployment) and on Azure Policy network groups, plus the az network manager CLI reference (via check_commands.py). Removed: the claim that spokes with their own gateways can't use a hub gateway (the docs say it only for VPN-tunnel spoke connections) and the unsourced "hundreds of VNets" figure.

Method: documentation only; no commands were run.
